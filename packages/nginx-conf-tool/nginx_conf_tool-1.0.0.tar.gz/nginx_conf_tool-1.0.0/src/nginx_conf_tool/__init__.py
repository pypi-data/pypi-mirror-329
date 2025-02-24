import click

from . import tree


@click.group()
@click.pass_context
def main(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


main.add_command(tree.tree)
