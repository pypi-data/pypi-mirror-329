# SSO Config Generator

A Python CLI tool for generating AWS SSO configuration and directory structures.

## Overview

SSO Config Generator is a standalone Python tool that simplifies AWS SSO configuration management by:

1. Generating properly configured AWS CLI config files
2. Creating directory structures that mirror your AWS Organization
3. Setting up environment files for easy role switching using `direnv`

## Installation

You can install SSO Config Generator using pip:

```bash
pip install sso-config-generator
```

### Prerequisites

- Python 3.8 or higher
- AWS CLI v2 configured with:
  - Default region set in `~/.aws/config` or via `AWS_DEFAULT_REGION` environment variable
  - AWS SSO configured via `aws configure sso`
- `direnv` (optional, for automatic profile switching)

### AWS Configuration

Before using the tool, ensure you have:

1. Set your AWS region:
   ```bash
   # Either in ~/.aws/config
   [default]
   region = eu-west-1

   # Or via environment variable
   export AWS_DEFAULT_REGION=eu-west-1
   ```

2. Configure AWS SSO:
   ```bash
   # Configure SSO
   aws configure sso
   # Follow the prompts to enter:
   # - SSO start URL (e.g., https://your-domain.awsapps.com/start)
   # - SSO Region
   # - SSO registration scopes (accept default)
   
   # Login to SSO to create credentials
   aws sso login
   ```

### Troubleshooting

1. "Error: You must specify a region"
   - Set AWS_DEFAULT_REGION environment variable
   - Or configure default region in ~/.aws/config

2. "Unable to locate credentials"
   - Run `aws sso login` to refresh your SSO credentials
   - Ensure you've completed AWS SSO configuration with `aws configure sso`
   - Check if your SSO session has expired (sessions typically last 8 hours)

3. "SSO session is expired"
   - Run `aws sso login` to start a new session

## Usage

### Basic Usage

Simply run:

```bash
uvx sso-config-generator
```

This will:
- Create/update your AWS CLI config file (`~/.aws/config`)
- Generate a directory structure in the current directory + sso-name
- Create `.envrc` files in each account directory with AdministratorAccess role
- Use OU structure for directory organization (cached for performance)

The tool caches OU structure information in the same directory as your AWS config file to improve performance. When the cache exists, it will be used automatically with a notification. To rebuild the cache:

```bash
uvx sso-config-generator --rebuild-cache
```

### Command Options

```
Usage: sso-config-generator [OPTIONS]

Options:
  --create-directories/--no-create-directories  Create a directory for each account (default: True)
  --use-ou-structure/--no-use-ou-structure     Create directories for each OU (default: True)
  --developer-role-name NAME                   Role name to use for .envrc files (default: AdministratorAccess)
  --rebuild-cache                              Force rebuild of OU structure cache
  --sso-name NAME                              Use specified SSO name instead of extracting from SSO start URL
  --create-repos-md                            Create repos.md files in each account directory
  --skip-sso-name                              Do not create a directory for the SSO name (default: False)
  --unified-root PATH                          Directory where account directories are created
                                               (default: current directory)
                                               If current directory is named "environment", SSO name is
                                               automatically skipped
  --validate                                   Validate current AWS SSO configuration instead of generating
  --help                                       Show this message and exit
  --version                                    Show the version and exit
```

### Examples

1. Basic config generation (uses defaults):
```bash
uvx sso-config-generator
```

2. Disable OU structure (flat account directories):
```bash
uvx sso-config-generator --no-use-ou-structure
```

3. Use different role for .envrc files:
```bash
uvx sso-config-generator --developer-role-name ReadOnlyAccess
```

4. Force rebuild of OU cache:
```bash
uvx sso-config-generator --rebuild-cache
```

5. Specify custom root directory:
```bash
uvx sso-config-generator --unified-root ~/aws-environments
```

6. Skip creating directories (config file only):
```bash
uvx sso-config-generator --no-create-directories
```

7. Working in an "environment" directory (automatic behavior):
```bash
# If your current directory is named 'environment'
cd environment
uvx sso-config-generator
# This will automatically skip creating the SSO name directory
```

8. Validate existing configuration:
```bash
uvx sso-config-generator --validate
```

## Development

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/easytocloud/sso-config-generator.git
cd sso-config-generator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e .
```

### Common Development Tasks

- Build the package: `pip install build && python -m build`
- Run the tool: `uvx sso-config-generator`
- Test changes: `./test_sso_config.sh`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
