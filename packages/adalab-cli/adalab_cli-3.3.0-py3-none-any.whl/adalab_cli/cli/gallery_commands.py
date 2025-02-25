"""Gallery command group for the adalib CLI.

This submodule encompasses commands related to Gallery functionalities
in the adalib CLI. It uses Typer for command line interface implementation,
providing functionalities like viewing card contents, managing cards, etc.

Functions:
- list_cards: Lists all available cards in the gallery.
- get-card: Displays contents of a specific card.
- approve-card: Approves a card in Gallery
- expose-card: Exposes a card in Gallery
- hide-card: Hides a card in Gallery
"""

import sys

import typer
from adalib.cards import expose_card, get_card_contents, get_cards, hide_card, toggle_card_review
from loguru import logger
from prompt_toolkit.completion import NestedCompleter
from rich import print as rich_print
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from typing_extensions import Annotated

from .completion_tree import completion_tree
from .factory import check_authentication
from .interactive import interactive_mode

gallery_app = typer.Typer()


@gallery_app.command("list-cards", no_args_is_help=True)
def gallery_list_cards(
    card_type: Annotated[
        str,
        typer.Argument(
            help="The type of cards to list. " "Choose from [all, notebook, voila, url, group].",
        ),
    ] = "all",
    head: Annotated[int | None, typer.Option(help="Number of cards to display.")] = None,
    url_subtype: Annotated[
        str,
        typer.Option(
            help="The URL subtype to filter by.",
        ),
    ] = "all",
    search_phrase: Annotated[str, typer.Option(help="Search phrase to filter cards by.")] = None,
    group_category: Annotated[str, typer.Option(help="Group category to filter by.")] = None,
    only_hidden: Annotated[bool, typer.Option(help="Show only hidden cards.")] = False,
    only_exposed: Annotated[bool, typer.Option(help="Show only exposed cards.")] = False,
):
    """
    Prints all cards from the Gallery with the type CARD_TYPE. Optionally filter by URL_SUBTYPE
    for URL cards.
    """
    try:
        with Progress(
            SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True
        ) as progress:
            progress.add_task(description="Fetching data...", total=None)
            cards = get_cards(
                card_type=card_type,
                url_subtype=url_subtype,
                head=head,
                search_phrase=search_phrase,
                group_category=group_category,
                only_hidden=only_hidden,
                only_exposed=only_exposed,
            )
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit()

    rich_print(f"Card type: {card_type} ({len(cards)})")

    cols = (
        [("Card id", 0), ("Card type", 1)]
        + ([("URL type", 2)] if card_type == "url" else [])
        + [("Reviewed", 3), ("Exposed", 4), ("Card name", 5)]
        + ([("Cards in Group", 6)] if card_type == "group" else [])
        + [("Card author", 7)]
    )
    table = Table(
        *[x[0] for x in cols],
        title="Cards",
    )
    for card in cards:
        table.add_row(
            *[
                (
                    str(card[ind])
                    if _cname not in ["Reviewed", "Exposed"]
                    else ("✅" if card[ind] else "❌")
                )
                for _cname, ind in cols
            ]
        )
    console = Console()
    console.print(table)


@gallery_app.command("get-card", no_args_is_help=True)
def gallery_get_card(
    card_id: Annotated[
        int,
        typer.Argument(
            help="The ID of the card you want to retrieve.",
        ),
    ],
    incl_content: Annotated[
        bool, typer.Option(help="Include card content in the output.")
    ] = False,
):
    """
    Gets the contents of a card identified by CARD_ID.
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Fetching data...", total=None)
            card = get_card_contents(card_id=card_id, incl_content=incl_content)
    except Exception:
        rich_print(f"Card {card_id} [bold red]failed[/bold red] to retrieve.")
        sys.exit(1)

    console = Console()

    table = Table(title="Card Details")
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    for key, value in card.items():
        if isinstance(value, bool):
            value = "✅" if value else "❌"
        table.add_row(key, str(value) if value != [] else "[dim]Empty List[/dim]")

    console.print(table)


@gallery_app.command("expose-card", no_args_is_help=True)
def gallery_expose_card(
    card_id: Annotated[
        int,
        typer.Argument(
            help="The ID of the card you want to retrieve.",
        ),
    ],
):
    """
    Exposes a card in gallery identify with CARD_ID.
    """
    try:
        expose_card(card_id=card_id)
    except Exception:
        rich_print(f"Card {card_id} [bold red]failed[/bold red] to expose.")
        sys.exit(1)
    rich_print(f"Card {card_id} [bold green]exposed[/bold green] successfully.")


@gallery_app.command("hide-card")
def gallery_hide_card(
    card_id: Annotated[
        int,
        typer.Argument(
            help="The ID of the card you want to retrieve.",
        ),
    ],
):
    """
    Hides a card in gallery identify with CARD_ID.
    """
    try:
        hide_card(card_id=card_id)
    except Exception:
        rich_print(f"Card {card_id} [bold red]failed[/bold red] to hide.")
        sys.exit(1)
    rich_print(f"Card {card_id} [bold green]hidden[/bold green] successfully.")


@gallery_app.command("toggle-review")
def gallery_toggle_card_review(
    card_id: Annotated[
        int,
        typer.Argument(
            help="The ID of the card whose review status you want to toggle.",
        ),
    ],
):
    """
    Toggles the review status of a card in Gallery.
    """
    try:
        toggle_card_review(card_id=card_id)
    except Exception:
        rich_print(f"Review status update of card {card_id} [bold red]failed[/bold red].")
        sys.exit(1)
    rich_print(f"Card {card_id} review status [bold green]updated[/bold green] successfully.")


@gallery_app.callback(invoke_without_command=True)
def main(
    interactive: bool = typer.Option(
        False, "-i", "--interactive", help="Activate interactive mode"
    )
):
    if interactive:
        interactive_mode(
            this_app=gallery_app,
            title="cards",
            color="maroon",
            completion=NestedCompleter.from_nested_dict(completion_tree["cards"]),
        )
    else:
        check_authentication()
