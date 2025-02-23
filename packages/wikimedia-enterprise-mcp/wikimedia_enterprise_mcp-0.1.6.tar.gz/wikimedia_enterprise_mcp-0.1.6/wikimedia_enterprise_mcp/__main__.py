import argparse
import os
import asyncio


def main():
    parser = argparse.ArgumentParser(
        description="Run the Wikimedia Enterprise MCP server"
    )
    parser.add_argument(
        "--username", help="WME username (overrides WME_USERNAME env var)"
    )
    parser.add_argument(
        "--password", help="WME password (overrides WME_PASSWORD env var)"
    )

    args = parser.parse_args()

    if args.username:
        os.environ["WME_USERNAME"] = args.username
    if args.password:
        os.environ["WME_PASSWORD"] = args.password

    from .server import run

    asyncio.run(run())


if __name__ == "__main__":
    main()
