import click

from . import parser


def _print_directive(name, prefix, is_last, is_context: bool = False):
    connector = "└── " if is_last else "├── "
    click.echo(f"{prefix}{connector}", nl=False)
    click.echo(click.style(name, fg="cyan") if is_context else name, color=True)


def print_tree(
    nodes: list, directory_only: bool = False, level: int = -1, prefix: str = ""
):
    if level == 0:
        return

    for node in nodes:
        is_last = node is nodes[-1]

        name = node["directive"]
        children = node.get("block")
        if children:
            _print_directive(name, prefix, is_last, is_context=True)
            print_tree(
                nodes=children,
                directory_only=directory_only,
                level=-1 if level == -1 else level - 1,
                prefix=prefix + ("    " if is_last else "│   "),
            )
        elif not directory_only:
            _print_directive(name, prefix, is_last)


@click.command()
@click.pass_context
@click.argument("file")
@click.option(
    "-d",
    "--directory",
    is_flag=True,
    help="List only those directives with children (AKA) context",
)
@click.option(
    "-L", "--level", type=int, default=-1, metavar="N", help="Limit to N levels deep"
)
def tree(ctx: click.Context, file, directory, level):
    try:
        parsed_list = parser.parse(file)
    except parser.ParseError as error:
        ctx.exit(error)

    for parsed in parsed_list:
        print_tree(parsed, directory_only=directory, level=level)
        click.echo()
