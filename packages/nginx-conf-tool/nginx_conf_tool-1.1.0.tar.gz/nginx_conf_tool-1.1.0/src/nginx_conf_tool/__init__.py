import click

from . import tree


@click.group()
@click.pass_context
@click.version_option()
def main(ctx: click.Context) -> None:
    ctx.ensure_object(dict)


main.add_command(tree.tree)
