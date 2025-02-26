import os
import sys
from typing import Optional
import click
from . import __version__
from .core import SSOConfigGenerator

@click.command()
@click.version_option(version=__version__)
@click.option('--create-directories/--no-create-directories', default=True, 
              help='Create a directory for each account')
@click.option('--use-ou-structure/--no-use-ou-structure', default=True, 
              help='Create directories for each OU')
@click.option('--developer-role-name', default="AdministratorAccess", 
              help='Role name to use for .envrc files')
@click.option('--rebuild-cache', is_flag=True, 
              help='Force rebuild of OU structure cache')
@click.option('--sso-name', 
              help='Use specified SSO name instead of extracting from SSO start URL')
@click.option('--create-repos-md', is_flag=True, 
              help='Create repos.md files in each account directory')
@click.option('--skip-sso-name', is_flag=True, 
              help='Do not create a directory for the SSO name')
@click.option('--unified-root', 
              help='Directory where account directories are created (default: current directory). '
                   'If current directory is named "environment", SSO name is automatically skipped.')
@click.option('--validate', is_flag=True,
              help='Validate current AWS SSO configuration instead of generating')
def cli(create_directories: bool, use_ou_structure: bool, developer_role_name: str,
        sso_name: Optional[str], create_repos_md: bool, skip_sso_name: bool, unified_root: Optional[str],
        rebuild_cache: bool, validate: bool):
    """SSO Config Generator - Generate AWS SSO configuration and directory structures.
    
    This tool will:
    1. Generate AWS CLI config file with SSO profiles for each account/role
    2. Create directory structure using OU hierarchy (if --use-ou-structure)
    3. Set up environment files (.envrc) for direnv with the specified role
    
    The tool uses a cache file in the same directory as your AWS config file to store the OU structure and account information.
    Use --rebuild-cache to force a refresh of the cache.
    
    Example usage:
        # Basic usage (uses defaults)
        sso-config-generator
        
        # Force rebuild of OU cache
        sso-config-generator --rebuild-cache
        
        # Use different role for .envrc files
        sso-config-generator --developer-role-name ReadOnlyAccess
        
        # Disable OU structure (flat account directories)
        sso-config-generator --no-use-ou-structure
        
        # Specify custom root directory
        sso-config-generator --unified-root ~/aws-environments
        
        # Skip creating the SSO name directory
        sso-config-generator --skip-sso-name
        
        # Validate existing configuration
        sso-config-generator --validate
    """
    try:
        if validate:
            # Run validation
            generator = SSOConfigGenerator()
            if not generator.validate():
                sys.exit(1)
        else:
            # Remove cache if rebuild requested
            if rebuild_cache:
                # Get the AWS config path from environment or default
                aws_config_path = os.environ.get('AWS_CONFIG_FILE', os.path.expanduser("~/.aws/config"))
                # Store cache in the same directory as the config file
                config_dir = os.path.dirname(aws_config_path)
                cache_path = os.path.join(config_dir, ".ou")
                
                if os.path.exists(cache_path):
                    os.remove(cache_path)
                    print(f"Removed existing OU cache at {cache_path}")
            
            # Generate configuration
            generator = SSOConfigGenerator(
                create_directories=create_directories,
                use_ou_structure=use_ou_structure,
                developer_role_name=developer_role_name,
                sso_name=sso_name,
                create_repos_md=create_repos_md,
                skip_sso_name=skip_sso_name,
                unified_root=unified_root
            )
            
            if not generator.generate():
                sys.exit(1)
                
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    cli()
