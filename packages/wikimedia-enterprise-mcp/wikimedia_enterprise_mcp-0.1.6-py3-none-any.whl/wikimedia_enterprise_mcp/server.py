from dotenv import load_dotenv
import httpx
from mcp import McpError
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool, INVALID_PARAMS, INTERNAL_ERROR, ErrorData

from typing import Annotated
from pydantic import BaseModel, Field
from wme.on_demand import Filter, EnterpriseAPIResponse, InfoboxPart
import wiki2md
from wikimedia_enterprise_mcp.constants import USER_AGENT
from wikimedia_enterprise_mcp.util import exception_to_string
from wikimedia_enterprise_mcp.wikidata import wikidata_fetch
from wikimedia_enterprise_mcp.wme import WmeClientProvider
from mediawikiapi import MediaWikiAPI
from mediawikiapi.config import Config
import logging
import asyncer


def make_httpx_client():
    headers = {"User-Agent": USER_AGENT}
    return httpx.AsyncClient(headers=headers)


class WmeFetch(BaseModel):
    """
    Parameters for fetching the content of a Wikipedia article
    """

    title: Annotated[str, Field(description="The title of the article to fetch")]
    lang: Annotated[
        str, Field(default="en", description="The language of the article to fetch")
    ]


class WikidataFetch(BaseModel):
    """
    Parameters for fetching the content of a Wikidata item
    """

    search_term: Annotated[
        str,
        Field(description="Term to search wikidata with (or the QID if you know it)"),
    ]
    lang: Annotated[
        str, Field(default="en", description="The language of the item to fetch")
    ]


load_dotenv()

wme = WmeClientProvider(make_httpx_client)
server = Server("wikimedia-enterprise-mcp")


async def search_wikipedia(query: str, language: str, limit: int = 1) -> list[str]:
    conf = Config(user_agent=USER_AGENT, language=language)
    api = MediaWikiAPI(config=conf)
    search_results = await asyncer.asyncify(api.search)(query, results=limit)
    return search_results


@server.list_tools()
async def list_prompts() -> list[Tool]:
    return [
        Tool(
            name="fetch",
            description="Fetch the content of a Wikipedia article",
            inputSchema=WmeFetch.model_json_schema(),
        ),
        Tool(
            name="fetch_wikidata",
            description="Fetch the content of a Wikidata item",
            inputSchema=WikidataFetch.model_json_schema(),
        ),
    ]


def infobox_to_fields(infobox: list[InfoboxPart]) -> list[str]:
    if not infobox:
        return []
    if isinstance(infobox[0], dict):
        # parse it as an infobox part
        infobox = [InfoboxPart(**part) for part in infobox]

    fields = []
    for part in infobox:
        if part.value:
            fields.append(f"{part.name}: {part.value}")
        elif part.values:
            fields.append(f"{part.name}: {', '.join(part.values)}")
        elif part.has_parts:
            if part.name:
                fields.append(part.name)
            fields.extend(infobox_to_fields(part.has_parts))
    return fields


def wme_response_to_text_content(resp: EnterpriseAPIResponse) -> TextContent:
    content: list[str] = [
        f"Information about '{resp.name}'",
    ]
    if resp.description:
        content.append(f"Description: {resp.description}")

    if resp.date_modified:
        content.append(f"Last modified: {resp.date_modified}")

    if resp.infobox:
        data = infobox_to_fields(resp.infobox)
        if data:
            content.append("Infobox: ")
            content.extend(data)

    if resp.article_sections:
        content.append("Text: ")
        for section, text in resp.iter_sections():
            if text:
                content.append(f"Section: {section}")
                content.append(text)
    else:
        content.append("Text: \n" + resp.article_body.wikitext)

    return TextContent(type="text", text="\n".join(content))


async def call_fetch_wikidata(arguments: dict) -> list[TextContent]:
    try:
        args = WikidataFetch(**arguments)
    except ValueError as e:
        raise McpError(ErrorData(code=INVALID_PARAMS, message=exception_to_string(e)))
    docs = await asyncer.asyncify(wikidata_fetch)(args.search_term, args.lang)
    return [TextContent(type="text", text=res) for res in docs]


async def call_fetch(arguments: dict) -> list[TextContent]:
    try:
        args = WmeFetch(**arguments)
    except ValueError as e:
        raise McpError(ErrorData(code=INVALID_PARAMS, message=exception_to_string(e)))

    client = make_httpx_client()
    try:
        res = await wiki2md.wiki_to_markdown(args.title, args.lang, client)
        content = f"Information about '{args.title}'\n\n{res}"
        return [TextContent(type="text", text=content)]
    except Exception as e:
        raise McpError(
            ErrorData(
                code=INTERNAL_ERROR,
                message=f"Failed to fetch article: {exception_to_string(e)}",
            )
        )


async def call_fetch_wme(arguments: dict) -> list[TextContent]:
    try:
        args = WmeFetch(**arguments)
    except ValueError as e:
        raise McpError(ErrorData(code=INVALID_PARAMS, message=exception_to_string(e)))

    client = await wme.get_on_demand_client()

    if args.lang == "en":
        res = await client.lookup_enwiki_structured(args.title)

        if not res:
            res = await search_wikipedia(args.title, args.lang, 1)
            if not res:
                raise McpError(
                    ErrorData(code=INTERNAL_ERROR, message="No results found")
                )
            res = await client.lookup_enwiki_structured(res[0])
            if not res:
                raise McpError(
                    ErrorData(code=INTERNAL_ERROR, message="No results found")
                )
        return [wme_response_to_text_content(res)]
    else:
        res = await client.lookup_structured(
            args.title, limit=1, filters=[Filter.for_site(args.lang + "wiki")]
        )
        if not res:
            res = await search_wikipedia(args.title, args.lang, 1)
            if not res:
                raise McpError(
                    ErrorData(code=INTERNAL_ERROR, message="No results found")
                )
            res = await client.lookup_structured(
                res[0], limit=1, filters=[Filter.for_site(args.lang + "wiki")]
            )
            if not res:
                raise McpError(
                    ErrorData(code=INTERNAL_ERROR, message="No results found")
                )

        return [wme_response_to_text_content(r) for r in res]


@server.call_tool()
async def call_tool(name, arguments: dict) -> list[TextContent]:
    if name == "fetch":
        if wme:
            return await call_fetch_wme(arguments)
        else:
            return await call_fetch(arguments)
    elif name == "fetch_wikidata":
        return await call_fetch_wikidata(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def run():
    global wme
    logging.info("Starting Wikimedia Enterprise MCP server")
    try:
        await wme.login()
    except httpx.HTTPStatusError as e:
        logging.error(f"Failed to login wme: {e}")
        logging.error(e.response.text)
        logging.error("Falling back to non-WME mode")
        wme = None
    try:
        options = server.create_initialization_options()
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, options, raise_exceptions=False)
    finally:
        if wme:
            await wme.logout()


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
