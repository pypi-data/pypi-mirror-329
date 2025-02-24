"""Console command implementation"""
import os
import sys
import time
import click
import yaml
import logging
from ..utils import common_debug_option, setup_logging
from ..config import load_config
from ..config.constants import LOCAL_CONFIG
from ..client import JenkinsClient

@click.command()
@click.option('--build', type=int, help='Build number to show console output for')
@click.option('--watch', is_flag=True, help='Watch console output')
@common_debug_option
def console(build, watch, debug):
    """Show build console output"""
    setup_logging(debug)
    if not os.path.exists(LOCAL_CONFIG):
        click.echo("Jenkins job not initialized. Run 'jnks init' first.")
        sys.exit(1)

    with open(LOCAL_CONFIG) as f:
        config = yaml.safe_load(f)

    try:
        jenkins_config = load_config()
        client = JenkinsClient(jenkins_config['host'], jenkins_config['user'], jenkins_config['token'])
        
        job_info = client.client.get_job_info(config['name'])
        logging.debug(f"Getting console output for job {config['name']}")

        if not build:
            builds = [b for b in job_info['builds'] if client.client.get_build_info(config['name'], b['number'])['building']]
            if len(builds) > 1:
                click.echo("Multiple builds are running. Please select a build number:")
                for b in builds:
                    click.echo(f"Build #{b['number']}")
                return
            build = job_info['lastBuild']['number']
            logging.debug(f"No build specified, using last build #{build}")

        logging.debug(f"Retrieving information for build #{build}")
        
        if watch:
            # Watch mode
            while True:
                console_output = client.client.get_build_console_output(config['name'], build)
                click.clear()
                click.echo(console_output)
                
                if not client.client.get_build_info(config['name'], build)['building']:
                    break
                time.sleep(2)
        else:
            # Single view mode
            console_output = client.client.get_build_console_output(config['name'], build)
            click.echo(console_output)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        logging.debug(f"Unexpected error: {str(e)}")
        sys.exit(1)