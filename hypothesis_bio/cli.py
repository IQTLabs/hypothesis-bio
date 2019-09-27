# -*- coding: utf-8 -*-

"""Console script for hypothesis_bio."""
import click


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
def main(args=None):
    """Console script for hypothesis_bio."""
    click.echo("Replace this message by putting your code into "
               "hypothesis_bio.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    main()
