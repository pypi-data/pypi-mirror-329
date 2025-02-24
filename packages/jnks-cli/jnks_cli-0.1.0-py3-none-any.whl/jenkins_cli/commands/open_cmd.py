"""Open command implementation"""
import os
import sys
import click
import yaml
import logging
import webbrowser
from ..utils import common_debug_option, setup_logging
from ..config import load_config
from ..config.constants import LOCAL_CONFIG
from ..client import JenkinsClient

@click.command(name='open')
@click.option('--build', type=int, help='Build number to open (opens job page if not specified)')
@common_debug_option
def open_cmd(build, debug):
    """Open Jenkins job or build in browser"""
    setup_logging(debug)
    if not os.path.exists(LOCAL_CONFIG):
        click.echo("Jenkins job not initialized. Run 'jnks init' first.")
        sys.exit(1)

    try:
        with open(LOCAL_CONFIG) as f:
            config = yaml.safe_load(f)

        jenkins_config = load_config()
        client = JenkinsClient(jenkins_config['host'], jenkins_config['user'], jenkins_config['token'])
        
        job_info = client.client.get_job_info(config['name'])
        job_url = job_info['url'].rstrip('/')
        
        if build:
            url = f"{job_url}/{build}"
            logging.debug(f"Opening build #{build} in browser: {url}")
        else:
            url = job_url
            logging.debug(f"Opening job in browser: {url}")
            
        webbrowser.open(url)
        click.echo(f"Opening {url} in browser")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        logging.debug(f"Unexpected error: {str(e)}")
        sys.exit(1)