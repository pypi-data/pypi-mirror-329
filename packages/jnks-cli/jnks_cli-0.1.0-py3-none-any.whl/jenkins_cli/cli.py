import os
import sys
import time
import click
import yaml
import jenkins
import logging
import json
import urllib3
import requests
from urllib.parse import urlparse
from pathlib import Path
from tabulate import tabulate
from urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import ConnectionError, SSLError, Timeout

CONFIG_DIR = os.path.expanduser("~/.jenkins")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.yaml")
LOCAL_CONFIG = ".jenkins.yaml"

def setup_logging(debug):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def load_config():
    if not os.path.exists(CONFIG_FILE):
        click.echo("Jenkins configuration not found. Please run 'jnks config' first.")
        sys.exit(1)
    with open(CONFIG_FILE) as f:
        return yaml.safe_load(f)

def get_jenkins_client():
    config = load_config()
    logging.debug(f"Connecting to Jenkins server at {config['host']}")
    
    if config['host'].startswith('https://'):
        urllib3.disable_warnings(InsecureRequestWarning)
        logging.debug("SSL verification warnings disabled for HTTPS connection")
        
        # Monkey patch the requests verify parameter
        old_request = requests.Session.request
        def new_request(self, method, url, **kwargs):
            kwargs['verify'] = False
            return old_request(self, method, url, **kwargs)
        requests.Session.request = new_request
    
    try:
        return jenkins.Jenkins(
            config['host'],
            username=config['user'],
            password=config['token'],
            timeout=30
        )
    except Exception as e:
        click.echo(f"Error connecting to Jenkins: {str(e)}")
        logging.debug(f"Unexpected error: {str(e)}")
        sys.exit(1)

def validate_jenkins_url(url):
    """Validate Jenkins URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except Exception:
        return False

def test_jenkins_connection(host, user, token):
    """Test Jenkins connection with given credentials"""
    if not validate_jenkins_url(host):
        logging.debug(f"Invalid URL format: {host}")
        return False
    
    if host.startswith('https://'):
        # Apply the same SSL verification disabling for test connection
        urllib3.disable_warnings(InsecureRequestWarning)
        old_request = requests.Session.request
        def new_request(self, method, url, **kwargs):
            kwargs['verify'] = False
            return old_request(self, method, url, **kwargs)
        requests.Session.request = new_request
    
    try:
        client = jenkins.Jenkins(
            host,
            username=user,
            password=token,
            timeout=30
        )
        # Try to get user information to verify credentials
        user = client.get_whoami()
        logging.debug(f"Successfully connected as user: {user['fullName']}")
        return True
    except jenkins.JenkinsException as e:
        logging.debug(f"Jenkins error: {str(e)}")
        return False
    except (ConnectionError, SSLError) as e:
        logging.debug(f"Connection error: {str(e)}")
        return False
    except Timeout:
        logging.debug("Connection timed out")
        return False
    except Exception as e:
        logging.debug(f"Unexpected error: {str(e)}")
        return False

def ensure_config_exists():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    if not os.path.exists(CONFIG_FILE):
        while True:
            host = input('Jenkins server host (e.g., https://jenkins.example.com): ').strip()
            if not validate_jenkins_url(host):
                click.echo("Invalid URL format. Please enter a valid URL (e.g., https://jenkins.example.com)")
                continue
                
            config = {
                'host': host,
                'token': input('Jenkins API token: ').strip(),
                'user': input('Jenkins username: ').strip()
            }
            
            click.echo("Testing connection...")
            if test_jenkins_connection(config['host'], config['user'], config['token']):
                with open(CONFIG_FILE, 'w') as f:
                    yaml.dump(config, f)
                click.echo(f"Connection successful! Configuration saved to {CONFIG_FILE}")
                break
            else:
                click.echo("Failed to connect to Jenkins. Please verify:")
                click.echo("1. The Jenkins URL is correct and accessible")
                click.echo("2. Your username is correct")
                click.echo("3. Your API token is valid")
                if not click.confirm('Would you like to try again?'):
                    sys.exit(1)

def common_debug_option(f):
    return click.option('--debug', is_flag=True, help='Enable debug logging')(f)

"""Main CLI entry point"""
import click
from .commands import (
    config,
    init,
    build,
    status,
    console,
    open_cmd
)

@click.group()
def cli():
    """Jenkins CLI tool for managing Jenkins jobs"""
    pass

# Register commands
cli.add_command(config)
cli.add_command(init)
cli.add_command(build)
cli.add_command(status)
cli.add_command(console)
cli.add_command(open_cmd)  # Let the command use its own name from decorator

if __name__ == '__main__':
    cli()