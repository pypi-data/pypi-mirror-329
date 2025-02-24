"""Init command implementation"""
import os
import sys
import click
import yaml
import logging
import json
from ..utils.decorators import common_debug_option, setup_logging
from ..config import load_config, LOCAL_CONFIG
from ..client import JenkinsClient

@click.command()
@click.option('--name', help='Job name (optional, defaults to current directory name)')
@common_debug_option
def init(name, debug):
    """Initialize Jenkins job configuration"""
    setup_logging(debug)
    logging.debug(f"Initializing job configuration with name: {name or 'current directory name'}")
    
    try:
        config = load_config()
        client = JenkinsClient(config['host'], config['user'], config['token'])
        
        if not name:
            name = os.path.basename(os.getcwd())
            logging.debug(f"No name provided, using current directory name: {name}")
        
        try:
            # Get job info with actions and parameters
            job_info = client.client.get_job_info(name, depth=2)
            logging.debug(f"Retrieved job info for {name}")
            logging.debug(f"Job info structure: {json.dumps(job_info, indent=2)}")
            
            parameters = {}
            
            def extract_params_from_definitions(param_defs):
                for param in param_defs:
                    param_name = param.get('name')
                    if param_name:
                        param_type = param.get('type', '')
                        default_value = None
                        
                        if 'defaultValue' in param:
                            default_value = param['defaultValue']
                        elif 'default' in param:
                            default_value = param['default']
                        elif 'value' in param:
                            default_value = param['value']
                        
                        if param_type == 'BooleanParameterDefinition':
                            default_value = bool(default_value) if default_value is not None else False
                        elif param_type == 'ChoiceParameterDefinition' and 'choices' in param:
                            choices = param['choices']
                            if isinstance(choices, list) and choices:
                                default_value = choices[0]
                            elif isinstance(choices, dict) and 'choices' in choices:
                                default_value = choices['choices'][0] if choices['choices'] else None
                        
                        if default_value is None or default_value == '':
                            parameters[param_name] = f"${param_name}"
                        else:
                            parameters[param_name] = default_value
                        
                        logging.debug(f"Found parameter: {param_name} = {parameters[param_name]} (type: {param_type})")

            # Check in actions
            if 'actions' in job_info:
                for action in job_info['actions']:
                    if isinstance(action, dict):
                        if 'parameterDefinitions' in action:
                            logging.debug("Found parameters in actions.parameterDefinitions")
                            extract_params_from_definitions(action['parameterDefinitions'])
                        elif 'parameters' in action:
                            logging.debug("Found parameters in actions.parameters")
                            extract_params_from_definitions(action['parameters'])

            # Check in property
            if not parameters and 'property' in job_info:
                for prop in job_info.get('property', []):
                    if isinstance(prop, dict):
                        if 'parameterDefinitions' in prop:
                            logging.debug("Found parameters in property.parameterDefinitions")
                            extract_params_from_definitions(prop['parameterDefinitions'])
                        elif 'parameters' in prop:
                            logging.debug("Found parameters in property.parameters")
                            extract_params_from_definitions(prop['parameters'])

            config = {
                'name': name,
                'parameters': parameters
            }

            with open(LOCAL_CONFIG, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            
            click.echo(f"Initialized job configuration in {LOCAL_CONFIG}")
            
            if not parameters:
                click.echo("Note: No build parameters were found for this job.")
            else:
                click.echo(f"Found {len(parameters)} parameters:")
                for param_name, param_value in parameters.items():
                    click.echo(f"  {param_name}: {param_value}")
                
        except Exception as e:
            if '404' in str(e):
                click.echo(f"Job '{name}' not found")
            elif '403' in str(e):
                click.echo(f"Permission denied to access job '{name}'. Please check your credentials.")
            else:
                click.echo(f"Error accessing job '{name}': {str(e)}")
            logging.debug(f"Full error: {str(e)}")
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        logging.debug(f"Unexpected error: {str(e)}")
        sys.exit(1)