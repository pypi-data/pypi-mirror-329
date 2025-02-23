from functools import lru_cache
from typing import Optional
from mcp import ErrorData, McpError
from wikibase_rest_api_client.utilities.fluent import FluentWikibaseClient
from wikibase_rest_api_client import Client
from .constants import USER_AGENT
from mediawikiapi import MediaWikiAPI
from mediawikiapi.config import Config
from mcp.types import (
    INTERNAL_ERROR,
)


WIKIDATA_API_URL = "https://www.wikidata.org/w/api.php"
WIKIDATA_REST_API_URL = "https://www.wikidata.org/w/rest.php/wikibase/v1/"


@lru_cache
def wikibase_client_cache(lang: str) -> FluentWikibaseClient:
    client = Client(
        timeout=60,
        base_url=WIKIDATA_REST_API_URL,
        headers={"User-Agent": USER_AGENT},
    )
    c = FluentWikibaseClient(client, lang=lang, supported_props=DEFAULT_PROPERTIES)
    return c


def _item_to_document(fluent_client: FluentWikibaseClient, qid: str) -> Optional[str]:
    resp = fluent_client.get_item(qid)

    if not resp:
        return None

    doc_lines = []
    if resp.label:
        doc_lines.append(f"Label: {resp.label}")
    if resp.description:
        doc_lines.append(f"Description: {resp.description}")
    if resp.aliases:
        doc_lines.append(f"Aliases: {', '.join(resp.aliases)}")
    for prop, values in resp.statements.items():
        if values:
            doc_lines.append(
                f"{prop.label}: {', '.join([v.value or 'unknown' for v in values])}"
            )
    return "\n".join(doc_lines)


def wikidata_fetch(search_term: str, lang: str = "en") -> list[str]:
    mw = MediaWikiAPI(Config(user_agent=USER_AGENT, mediawiki_url=WIKIDATA_API_URL))

    c = wikibase_client_cache(lang)
    search_results = mw.search(search_term, results=3)
    if not search_results:
        raise McpError(ErrorData(code=INTERNAL_ERROR, message="No results found"))

    docs = [_item_to_document(c, r) for r in search_results]
    filtered_docs = [d for d in docs if d]
    if not filtered_docs:
        raise McpError(ErrorData(code=INTERNAL_ERROR, message="No document found"))

    return filtered_docs


DEFAULT_PROPERTIES = [
    "P31",
    "P279",
    "P27",
    "P361",
    "P527",
    "P495",
    "P17",
    "P585",
    "P131",
    "P106",
    "P21",
    "P569",
    "P570",
    "P577",
    "P50",
    "P571",
    "P641",
    "P625",
    "P19",
    "P69",
    "P108",
    "P136",
    "P39",
    "P161",
    "P20",
    "P101",
    "P179",
    "P175",
    "P7937",
    "P57",
    "P607",
    "P509",
    "P800",
    "P449",
    "P580",
    "P582",
    "P276",
    "P69",
    "P112",
    "P740",
    "P159",
    "P452",
    "P102",
    "P1142",
    "P1387",
    "P1576",
    "P140",
    "P178",
    "P287",
    "P25",
    "P22",
    "P40",
    "P185",
    "P802",
    "P1416",
]
