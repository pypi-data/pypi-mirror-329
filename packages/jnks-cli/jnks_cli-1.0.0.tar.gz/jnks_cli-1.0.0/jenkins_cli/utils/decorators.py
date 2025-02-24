"""Common utilities and decorators"""
import click
import logging

def setup_logging(debug):
    """Configure logging based on debug flag"""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def common_debug_option(f):
    """Common debug option decorator for CLI commands"""
    return click.option('--debug', is_flag=True, help='Enable debug logging')(f)