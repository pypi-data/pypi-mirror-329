import sys

import click


class CheckFailedException(Exception):
    pass


def check_failed(message: str, will_fix: bool):
    if will_fix:
        click.secho(message, fg="yellow", err=True)
        raise CheckFailedException()
    else:
        click.secho(message, fg="red", err=True)
        sys.exit(1)
