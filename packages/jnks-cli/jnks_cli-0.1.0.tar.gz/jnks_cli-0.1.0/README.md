# Jenkins CLI Tool

A command-line interface for managing Jenkins jobs.

## Installation

### Install from source
```bash
pip install .
```

### Install in development mode
```bash
pip install -e .
```

## Uninstallation

To remove the tool:
```bash
pip uninstall jnks-cli
```

## Usage

Each command supports its own `--debug` flag for detailed logging.

### Available Commands:

1. First time setup:
```bash
jnks config --debug
```

2. Initialize a Jenkins job:
```bash
jnks init --debug [--name JOB_NAME]
```

3. Build a job:
```bash
# Basic build command
jnks build

# Watch console output
jnks build --watch

# Passing parameters (two equivalent ways):
jnks build --param1=value1 --param2=value2
jnks build param1=value1 param2=value2

# Example with debug and watch:
jnks build --debug --watch param1=value1 param2=value2
```

Note: Parameters marked with $ in .jenkins.yaml are required and must be provided during build.
Example .jenkins.yaml:
```yaml
name: my-job
parameters:
  BRANCH: $BRANCH           # Required parameter, must be provided
  ENV: staging             # Optional parameter with default value
  DEBUG: true             # Optional parameter with default value
```

To build with the above configuration:
```bash
jnks build BRANCH=main          # ENV and DEBUG use default values
jnks build BRANCH=main ENV=prod # Override default ENV value
```

4. View recent builds:
```bash
jnks status --debug
```

5. View console output:
```bash
# Basic console output
jnks console [--build BUILD_NUMBER]

# Watch console output in real-time
jnks console --watch [--build BUILD_NUMBER]

# With debug logging
jnks console --debug --watch [--build BUILD_NUMBER]
```

6. Open in browser:
```bash
# Open job in browser
jnks open

# Open specific build in browser
jnks open --build BUILD_NUMBER

# With debug logging
jnks open --debug [--build BUILD_NUMBER]
```

Note: When using --watch, the command will continue to show updates until the build completes.

## Debug Mode

Add `--debug` to any command to see detailed logs about:
- API calls to Jenkins server
- Parameter processing
- Build status updates
- Configuration loading
- Error details