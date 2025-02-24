"""Config management utilities"""
import os
import sys
import yaml
import click
import logging
from urllib.parse import urlparse
from ..client import JenkinsClient
from .constants import CONFIG_DIR, CONFIG_FILE, LOCAL_CONFIG

def load_config():
    """Load Jenkins configuration from config file"""
    if not os.path.exists(CONFIG_FILE):
        click.echo("Jenkins configuration not found. Please run 'jnks config' first.")
        sys.exit(1)
    with open(CONFIG_FILE) as f:
        return yaml.safe_load(f)

def validate_jenkins_url(url):
    """Validate Jenkins URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except Exception:
        return False

def ensure_config_exists():
    """Ensure Jenkins configuration exists and is valid"""
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
            client = JenkinsClient(config['host'], config['user'], config['token'])
            if client.test_connection():
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