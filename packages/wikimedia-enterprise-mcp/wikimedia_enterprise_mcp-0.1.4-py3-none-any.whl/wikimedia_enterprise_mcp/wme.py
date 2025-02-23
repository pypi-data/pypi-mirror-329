from datetime import datetime, timedelta
import logging
import os
from typing import TypedDict
from wme.on_demand import OnDemand
from wme.auth import refresh_token, revoke_token, login


class AuthState(TypedDict):
    refreshing_token: str | None
    access_token: str | None
    token_expired_at: datetime


WME_TOKEN_REFRESH_BUFFER_SEC = 60 * 60  # 1 hour buffer for token refresh

_log = logging.getLogger(__name__)


class WmeClientProvider:
    def __init__(self, make_httpx_client):
        self.http_client = make_httpx_client()
        self.auth_state: dict = {
            "refreshing_token": None,
            "access_token": None,
        }
        self.wme_username = os.getenv("WME_USERNAME")
        self.wme_password = os.getenv("WME_PASSWORD")

    async def login(self):
        creds = await login(self.wme_username, self.wme_password, self.http_client)

        expired_at = datetime.now() + timedelta(
            seconds=creds.expires_in - WME_TOKEN_REFRESH_BUFFER_SEC
        )
        self.auth_state["refreshing_token"] = creds.refresh_token
        self.auth_state["access_token"] = creds.access_token
        self.auth_state["token_expired_at"] = expired_at
        _log.info(f"Logged in to WME next token refresh at {expired_at}")

    async def get_wme_token(self) -> str:
        expires_at = self.auth_state["token_expired_at"]
        if expires_at < datetime.now():
            token_response = await refresh_token(
                self.wme_username, self.auth_state["refreshing_token"]
            )
            self.auth_state["access_token"] = token_response.access_token
            self.auth_state["token_expired_at"] = datetime.now() + timedelta(
                token_response.expires_in - WME_TOKEN_REFRESH_BUFFER_SEC
            )
            _log.info(
                f"Refreshed WME token, next refresh at {self.auth_state['token_expired_at']}"
            )
            return token_response.access_token
        else:
            return self.auth_state["access_token"]

    async def get_on_demand_client(self) -> OnDemand:
        token = await self.get_wme_token()
        return OnDemand(token, self.http_client)

    async def logout(self):
        await revoke_token(self.auth_state["refreshing_token"], self.http_client)
        self.auth_state = {"refreshing_token": None, "access_token": None}
        _log.info("Logged out of WME")
