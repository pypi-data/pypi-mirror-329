import decimal
import json
import select
import sys
from pathlib import Path
from urllib.parse import urlparse

import httpx
import typer
from click import ClickException
from fake_useragent import UserAgent
from js2py import PyJsException
from rich.console import Console
from rich.syntax import Syntax

from gronpy.__version__ import version_callback
from gronpy.gron import gron
from gronpy.ungron import ungron

app = typer.Typer()
console = Console()
err_console = Console(stderr=True)


class InputType:
    STDIN = "stdin"
    FILE = "file"
    HTTP = "http"


class ExitCodes:
    NO_STDIN_DATA = 10
    HTTP_GET_ERROR = 11
    FILE_READ_ERROR = 12
    JSON_UNPARSEABLE = 13
    GRON_FILE_UNPARSEABLE = 14


class Error(ClickException):
    def __init__(self, message: str, exit_code=1) -> None:
        super().__init__(message)
        self.exit_code = exit_code


def type_of_input(input_path: str) -> Path:
    if not input_path:
        return InputType.STDIN

    try:
        parsed_url = urlparse(input_path)
    except Exception:
        return InputType.FILE

    if parsed_url.scheme:
        if parsed_url.scheme in ["http", "https"]:
            return InputType.HTTP
    else:
        return InputType.FILE


def has_data_on_stdin():
    return select.select([sys.stdin], [], [], 0.0)[0]


def get_stdin():
    if sys.stdin.isatty() or not has_data_on_stdin():
        raise Error("Error: No data on stdin. Please provide input.", ExitCodes.NO_STDIN_DATA)
    return sys.stdin.buffer.read().decode()


def get_http(url, user_agent=None, timeout=30):
    try:
        headers = {"User-Agent": user_agent} if user_agent else None
        return httpx.get(url, headers=headers, timeout=timeout).text
    except httpx.ConnectError:
        raise Error("Error: HTTP request failed", ExitCodes.HTTP_GET_ERROR)
    except httpx.TimeoutException:
        raise Error(f"Error: HTTP request timed out after {timeout} seconds", ExitCodes.HTTP_GET_ERROR)


def get_file(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        raise Error(f"Error: File '{path}' not found", ExitCodes.FILE_READ_ERROR)


@app.command()
def main(  # noqa: PLR0913
    input_path: str = typer.Argument(
        None, help="Input file path or URL. If not specified uses stdin.", show_default="stdin"
    ),
    gron_action: bool = typer.Option(True, "--gron/--ungron", help="Transform JSON into GRON or back again"),
    color: bool = typer.Option(True, help="Enable colouring in terminal."),
    user_agent: str = typer.Option(None, "--user-agent", "-u", help="Set custom User-Agent header for HTTP requests"),
    user_agent_random: bool = typer.Option(False, "--user-agent-random", help="Use a random User-Agent header"),
    timeout: int = typer.Option(30, "--timeout", "-t", help="Timeout in seconds for HTTP requests"),
    _: bool = typer.Option(None, "-v", "--version", callback=version_callback, is_eager=True),
):
    input_type = type_of_input(input_path)

    if user_agent and user_agent_random:
        raise Error("Error: Cannot use both --user-agent and --user-agent-random")

    if user_agent_random:
        ua = UserAgent()
        user_agent = ua.random

    if input_type == InputType.STDIN:
        data = get_stdin()
    elif input_type == InputType.HTTP:
        data = get_http(input_path, user_agent, timeout)
    elif input_type == InputType.FILE:
        data = get_file(input_path)

    if gron_action:
        try:
            json_data = json.loads(data, parse_float=decimal.Decimal)
        except json.JSONDecodeError:
            raise Error("Error: Unable to parse JSON", ExitCodes.JSON_UNPARSEABLE)
        gron_data = gron(json_data, "json")
        if console.is_terminal:
            if not color:
                print(gron_data)
            else:
                console.print(Syntax(gron_data, "javascript", background_color="default"))
        else:
            console.file.write(gron_data)
    else:
        try:
            ungron_data = ungron(data)
        except PyJsException:
            raise Error("Error: Unable to parse gron file", ExitCodes.GRON_FILE_UNPARSEABLE)
        if console.is_terminal:
            if not color:
                print(ungron_data)
            else:
                console.print_json(ungron_data)
        else:
            console.file.write(ungron_data)


if __name__ == "__main__":
    app()
