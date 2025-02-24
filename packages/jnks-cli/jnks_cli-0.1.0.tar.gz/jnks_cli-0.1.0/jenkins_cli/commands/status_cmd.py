"""Status command implementation"""
import os
import sys
import click
import yaml
import logging
from ..utils import common_debug_option, setup_logging, display_builds_table, format_build_info
from ..config import load_config
from ..config.constants import LOCAL_CONFIG
from ..client import JenkinsClient

@click.command()
@common_debug_option
def status(debug):
    """List recent builds"""
    setup_logging(debug)
    if not os.path.exists(LOCAL_CONFIG):
        click.echo("Jenkins job not initialized. Run 'jnks init' first.")
        sys.exit(1)

    with open(LOCAL_CONFIG) as f:
        config = yaml.safe_load(f)

    try:
        jenkins_config = load_config()
        client = JenkinsClient(jenkins_config['host'], jenkins_config['user'], jenkins_config['token'])
        
        logging.debug(f"Getting status for job {config['name']}")
        builds = client.client.get_job_info(config['name'])['builds'][:5]
        
        table_data = []
        for build in builds:
            info = client.client.get_build_info(config['name'], build['number'])
            logging.debug(f"Retrieved info for build #{build['number']}")
            table_data.append(format_build_info(info, config['name']))

        display_builds_table(table_data)
        
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        logging.debug(f"Unexpected error: {str(e)}")
        sys.exit(1)