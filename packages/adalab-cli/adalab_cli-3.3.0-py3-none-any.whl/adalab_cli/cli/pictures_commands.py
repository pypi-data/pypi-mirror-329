"""Pictures-related commands"""

import sys
from io import BytesIO
from typing import Annotated

import typer
from adalib.adaboard import request_adaboard
from adalib.pictures import get_picture, post_picture, post_picture_url
from ascii_magic import AsciiArt
from prompt_toolkit.completion import NestedCompleter
from rich import print as rich_print

from .completion_tree import completion_tree
from .factory import check_authentication
from .interactive import interactive_mode

pictures_app = typer.Typer()


@pictures_app.command("show", no_args_is_help=True)
def show_picture(picture_id: Annotated[int, typer.Argument(help="The ID of the picture to show")]):
    """Show the specific picture as an ASCII art"""
    try:
        data = BytesIO(request_adaboard(f"image/{picture_id}").content)
        AsciiArt.from_image(data).to_terminal()
    except Exception:
        rich_print(f"Could not show the picture with ID: {picture_id}")
        sys.exit(1)


@pictures_app.command("download", no_args_is_help=True)
def download_picture(
    picture_id: Annotated[int, typer.Argument(help="The ID of the picture to download")],
    output_path: Annotated[
        str | None, typer.Option(help="The path to save the picture to")
    ] = None,
):
    """Download the specific picture into a file."""
    if output_path is None:
        output_path = f"picture_{picture_id}"
    try:
        get_picture(picture_id=picture_id, output_file_path=output_path)
    except Exception:
        rich_print(f"Could not download the picture with ID: {picture_id}")
        sys.exit(1)


@pictures_app.command("create", no_args_is_help=True)
def create_new_picture(
    path: Annotated[str | None, typer.Option(help="The path to the picture file")] = None,
    url: Annotated[str | None, typer.Option(help="The URL of the picture")] = None,
):
    """Create a new picture from a file or URL."""
    if (path is not None and url is not None) or (path is None and url is None):
        rich_print("Please provide either a path or a URL to create a picture.")
        sys.exit(1)

    try:
        if path is not None:
            picture_id = post_picture(input_file_path=path)
        else:
            picture_id = post_picture_url(picture_url=url)

        rich_print(f"Picture created with ID: {picture_id}")
    except Exception:
        rich_print("Could not create the picture.")
        sys.exit(1)


@pictures_app.callback(invoke_without_command=True)
def main(
    interactive: bool = typer.Option(
        False, "-i", "--interactive", help="Activate interactive mode"
    )
):
    if interactive:
        interactive_mode(
            this_app=pictures_app,
            title="pictures",
            color="maroon",
            completion=NestedCompleter.from_nested_dict(completion_tree["pictures"]),
        )
    else:
        check_authentication()
