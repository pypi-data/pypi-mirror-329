"""Display utilities for formatting output"""
import click
from tabulate import tabulate
import time

def display_builds_table(builds_data):
    """Display builds in a tabulated format"""
    click.echo(tabulate(
        builds_data,
        headers=['Build', 'Name', 'Status', 'Started', 'Duration'],
        tablefmt='grid'
    ))

def format_build_info(build_info, job_name):
    """Format build information for display"""
    return [
        build_info['number'],
        job_name,
        build_info['result'] or 'IN PROGRESS',
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(build_info['timestamp']/1000)),
        f"{build_info['duration']/1000:.1f}s"
    ]