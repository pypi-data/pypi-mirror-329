import argparse

from dlt.common import logger
from dlt.cli import SupportsCliCommand
from dlt_plus.common.cli import add_project_opts


class MCPCommand(SupportsCliCommand):
    command = "mcp"
    help_string = "Launch a dlt MCP server"
    description = (
        "The MCP server allows LLMs to interact with your dlt pipelines and your dlt+ projects."
    )

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser
        add_project_opts(parser)

        subparser = parser.add_subparsers(title="Available subcommands", dest="mcp_command")

        subparser.add_parser(
            "run", help="Launch MCP server from current environment and working directory"
        )

    def execute(self, args: argparse.Namespace) -> None:
        if args.mcp_command == "run":
            from mcp.server.fastmcp import FastMCP
            from dlt_plus.project.mcp_tools import GenericMCPTools

            logger.info("Starting MCP server")
            mcp_tools = GenericMCPTools()

            mcp = FastMCP("dlt+")
            mcp_tools.register_with(mcp)

            mcp.run(transport="stdio")
