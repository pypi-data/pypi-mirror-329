"""
ABSFUYU CLI
-----------
Config

Version: 1.0.0
Date updated: 14/04/2024 (dd/mm/yyyy)
"""

__all__ = ["config_group"]

import click

from absfuyu.cli.color import COLOR
from absfuyu.config import ABSFUYU_CONFIG


@click.command()
@click.option(
    "--setting",
    "-s",
    type=click.Choice(["luckgod", "install-extra"]),
    help="Toggle on/off selected setting",
)
def toggle(setting: str) -> None:
    """Toggle on/off setting"""

    # Dictionary
    trans = {
        "luckgod": "luckgod-mode",
        "install-extra": "auto-install-extra",
    }  # trans[setting]

    if setting is None:
        click.echo(f"{COLOR['red']}Invalid setting")  # type: ignore
    else:
        ABSFUYU_CONFIG.toggle_setting(trans[setting])
        out = ABSFUYU_CONFIG._get_setting(trans[setting])
        click.echo(f"{COLOR['red']}{out}")


@click.command()
def reset():
    """Reset config to default value"""
    ABSFUYU_CONFIG.reset_config()
    click.echo(f"{COLOR['green']}All settings have been reseted")


@click.group(name="config")
def config_group() -> None:
    """absfuyu configuration"""
    pass


config_group.add_command(toggle)
config_group.add_command(reset)
