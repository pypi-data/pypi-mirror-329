"""Config command implementation"""
import click
import logging
from ..config import ensure_config_exists
from ..utils.decorators import common_debug_option, setup_logging

@click.command()
@common_debug_option
def config(debug):
    """Configure Jenkins connection settings"""
    setup_logging(debug)
    logging.debug("Running config command")
    ensure_config_exists()