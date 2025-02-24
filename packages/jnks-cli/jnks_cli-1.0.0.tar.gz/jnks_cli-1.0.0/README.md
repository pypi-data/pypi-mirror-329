# Jenkins CLI Tool (jnks)

[![Release](https://github.com/iamvinit/jenkins-cli/actions/workflows/release.yml/badge.svg)](https://github.com/iamvinit/jenkins-cli/actions/workflows/release.yml)

A command-line interface for managing Jenkins jobs. Simple, fast, and easy to use.

## Installation

```bash
pip install jnks-cli
```

## Quick Start

1. Configure Jenkins connection:
```bash
$ jnks config
Jenkins server host (e.g., https://jenkins.example.com): https://jenkins.company.com
Jenkins API token: your-api-token
Jenkins username: your-username
Testing connection...
Connection successful! Configuration saved to ~/.jenkins/config.yaml
```

2. Initialize a job (in your project directory):
```bash
$ jnks init
Initialized job configuration in .jenkins.yaml
Found 3 parameters:
  BRANCH: $BRANCH
  ENV: staging
  DEBUG: true
```

## Commands

### Build (`build`)
Trigger a Jenkins job build.

```bash
# Basic build with parameters
$ jnks build BRANCH=main ENV=prod
Build #123 started

# Watch console output
$ jnks build --watch BRANCH=main
Build #124 started
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /workspace/my-job
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Checkout)
[Pipeline] checkout
...

# With debug logging
$ jnks build --debug BRANCH=main
2024-02-22 17:27:24 - DEBUG - Connecting to Jenkins server at https://jenkins.company.com
2024-02-22 17:27:24 - DEBUG - Build parameters: {"BRANCH": "main", "ENV": "staging"}
Build #125 started
```

Parameters in `.jenkins.yaml` marked with `$` are required:
```yaml
name: my-job
parameters:
  BRANCH: $BRANCH     # Required
  ENV: staging        # Optional with default
  DEBUG: true        # Optional with default
```

### Console Output (`console`)
View build console output.

```bash
# View latest build
$ jnks console
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /workspace/my-job
...

# View specific build with watch
$ jnks console --watch --build 123
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /workspace/my-job
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Build)
...
```

### Status (`status`)
View recent builds status.

```bash
$ jnks status
┌───────┬───────────────┬────────────┬─────────────────────┬──────────┐
│ Build │ Name          │ Status     │ Started             │ Duration │
├───────┼───────────────┼────────────┼─────────────────────┼──────────┤
│ 125   │ my-job        │ SUCCESS    │ 2024-02-22 17:27:24 │ 45.2s    │
│ 124   │ my-job        │ FAILURE    │ 2024-02-22 17:25:10 │ 32.8s    │
│ 123   │ my-job        │ SUCCESS    │ 2024-02-22 17:20:05 │ 38.5s    │
│ 122   │ my-job        │ SUCCESS    │ 2024-02-22 17:15:30 │ 41.1s    │
│ 121   │ my-job        │ ABORTED    │ 2024-02-22 17:10:15 │ 12.3s    │
└───────┴───────────────┴────────────┴─────────────────────┴──────────┘
```

### Open in Browser (`open`)
Open Jenkins job or build in your default browser.

```bash
# Open job page
$ jnks open
Opening https://jenkins.company.com/job/my-job in browser

# Open specific build
$ jnks open --build 123
Opening https://jenkins.company.com/job/my-job/123 in browser
```

## Global Options

- `--debug`: Enable debug logging (available for all commands)

Example debug output:
```bash
$ jnks status --debug
2024-02-22 17:27:24 - DEBUG - Connecting to Jenkins server at https://jenkins.company.com
2024-02-22 17:27:24 - DEBUG - SSL verification warnings disabled for HTTPS connection
2024-02-22 17:27:25 - DEBUG - Getting status for job my-job
2024-02-22 17:27:25 - DEBUG - Retrieved info for build #125
...
```

## Configuration

The tool stores configuration in two locations:
- Global: `~/.jenkins/config.yaml` (Jenkins connection details)
```yaml
host: https://jenkins.company.com
token: your-api-token
user: your-username
```

- Local: `.jenkins.yaml` (Job-specific settings)
```yaml
name: my-job
parameters:
  BRANCH: $BRANCH
  ENV: staging
  DEBUG: true
```

## Error Handling

Common error messages and solutions:

1. "Jenkins job not initialized":
   ```bash
   $ jnks build
   Jenkins job not initialized. Run 'jnks init' first.
   
   $ jnks init
   Initialized job configuration in .jenkins.yaml
   ```

2. "Multiple builds are running":
   ```bash
   $ jnks console
   Multiple builds are running. Please select a build number:
   Build #125
   Build #124
   
   $ jnks console --build 125
   [Pipeline] Start of Pipeline...
   ```

3. "No parameters provided":
   ```bash
   $ jnks build
   Error: No parameters provided. Required parameters:
     BRANCH: $BRANCH
   
   Example usage:
     jnks build BRANCH=main
   ```

## License

MIT License - see [LICENSE](LICENSE) for details.