"""Build command implementation"""
import os
import sys
import time
import click
import yaml
import logging
import json
from ..utils import common_debug_option, setup_logging
from ..config import load_config
from ..config.constants import LOCAL_CONFIG
from ..client import JenkinsClient

@click.command()
@click.option('--watch', is_flag=True, help='Watch console output')
@common_debug_option
@click.argument('params', nargs=-1)
def build(watch, debug, params):
    """Build the Jenkins job"""
    setup_logging(debug)
    if not os.path.exists(LOCAL_CONFIG):
        click.echo("Jenkins job not initialized. Run 'jnks init' first.")
        sys.exit(1)

    with open(LOCAL_CONFIG) as f:
        config = yaml.safe_load(f)

    job_name = config['name']
    required_params = config.get('parameters', {})
    build_params = {}
    
    # First, populate with default values from config
    for param_name, param_value in required_params.items():
        if not isinstance(param_value, str) or not param_value.startswith('$'):
            build_params[param_name] = param_value
            logging.debug(f"Using default value for {param_name} = {param_value}")
    
    # Then override with provided parameters
    for param in params:
        if '=' not in param:
            continue
        key, value = param.split('=', 1)
        key = key.lstrip('-')  # Remove leading dashes for both formats (--param=value or param=value)
        build_params[key] = value
        logging.debug(f"Parameter provided: {key} = {value} (overriding default if any)")

    # If no parameters were provided, validate required ones
    if not params:
        missing_params = []
        for param_name, param_value in required_params.items():
            if isinstance(param_value, str) and param_value.startswith('$'):
                missing_params.append(param_name)
                
        if missing_params:
            click.echo("Error: No parameters provided. Required parameters:")
            for param in missing_params:
                click.echo(f"  {param}: {required_params[param]}")
            click.echo("\nExample usage:")
            example_params = ' '.join(f"{p}=value" for p in missing_params)
            click.echo(f"  jnks build {example_params}")
            sys.exit(1)

    # Log all parameters that will be used
    logging.debug("Build parameters:")
    for key, value in build_params.items():
        if key in required_params:
            default_value = required_params[key]
            if value == default_value:
                logging.debug(f"  {key} = {value} (using default)")
            else:
                logging.debug(f"  {key} = {value} (provided, overriding default: {default_value})")
        else:
            logging.debug(f"  {key} = {value} (extra parameter)")

    try:
        jenkins_config = load_config()
        client = JenkinsClient(jenkins_config['host'], jenkins_config['user'], jenkins_config['token'])
        
        logging.debug(f"Triggering build for job {job_name} with parameters: {json.dumps(build_params, indent=2)}")
        queue_item = client.client.build_job(job_name, parameters=build_params)
        
        while True:
            build_info = client.client.get_queue_item(queue_item)
            if 'executable' in build_info:
                build_number = build_info['executable']['number']
                break
            logging.debug("Waiting for build to start...")
            time.sleep(1)

        # Show build number immediately
        click.echo(f"Build #{build_number} started")
        
        # Only watch if explicitly requested
        if watch:
            logging.debug("Watching console output")
            while True:
                console_output = client.client.get_build_console_output(job_name, build_number)
                click.clear()
                click.echo(console_output)
                if not client.client.get_build_info(job_name, build_number)['building']:
                    break
                time.sleep(2)
                
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        logging.debug(f"Jenkins error: {str(e)}")
        sys.exit(1)