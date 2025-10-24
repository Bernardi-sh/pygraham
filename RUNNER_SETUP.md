# GitHub Actions Runner Setup

This project uses **self-hosted runners** for regular CI/CD operations and **GitHub-hosted runners** for scheduled daily builds.

## Runner Strategy

### Self-Hosted Runners (Push/PR Events)
- **Triggered by**: Push to main, Pull Requests
- **Workflows**:
  - `ci.yml` - Main CI/CD pipeline
  - `sonarqube.yml` - SonarQube analysis
- **Benefits**:
  - Faster execution (no queue time)
  - Cost savings
  - Control over environment
  - Access to local resources

### GitHub-Hosted Runners (Scheduled)
- **Triggered by**: Monthly on the 1st at 00:00 UTC (or manual dispatch)
- **Workflow**: `scheduled-ci.yml`
- **Benefits**:
  - Multi-platform testing (Ubuntu, macOS, Windows)
  - Validates against fresh environments
  - No maintenance required

## Setting Up Self-Hosted Runners

### Prerequisites
- Linux, macOS, or Windows machine
- Python 3.8+ installed
- Git installed
- Network access to GitHub

### Installation Steps

#### 1. Navigate to Runner Settings
1. Go to your repository: https://github.com/Bernardi-sh/pygraham
2. Click **Settings** → **Actions** → **Runners**
3. Click **New self-hosted runner**

#### 2. Download and Configure

**For Linux/macOS:**
```bash
# Create a folder
mkdir actions-runner && cd actions-runner

# Download the latest runner package
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz

# Extract the installer
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# Configure the runner
./config.sh --url https://github.com/Bernardi-sh/pygraham --token YOUR_TOKEN

# Install and start the service
sudo ./svc.sh install
sudo ./svc.sh start
```

**For Windows (PowerShell):**
```powershell
# Create a folder
mkdir actions-runner ; cd actions-runner

# Download the latest runner package
Invoke-WebRequest -Uri https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-win-x64-2.311.0.zip -OutFile actions-runner-win-x64-2.311.0.zip

# Extract the installer
Add-Type -AssemblyName System.IO.Compression.FileSystem ; [System.IO.Compression.ZipFile]::ExtractToDirectory("$PWD/actions-runner-win-x64-2.311.0.zip", "$PWD")

# Configure the runner
./config.cmd --url https://github.com/Bernardi-sh/pygraham --token YOUR_TOKEN

# Install and start the service
./svc.sh install
./svc.sh start
```

#### 3. Verify Installation

After setup, the runner should appear in your repository's **Settings** → **Actions** → **Runners** page with a green "Idle" status.

### Multiple Runners

You can set up multiple runners for:
- **Parallel execution**: Speed up builds
- **Different platforms**: Test on various OS
- **High availability**: Redundancy if one goes down

Each runner needs to be configured separately with its own token.

## Runner Requirements

### System Requirements
- **CPU**: 2+ cores recommended
- **RAM**: 4GB+ recommended
- **Disk**: 10GB+ free space
- **Network**: Stable internet connection

### Software Requirements
The runner needs:
- Python 3.8, 3.9, 3.10, 3.11, 3.12
- pip
- pytest, pytest-cov
- black, ruff, mypy
- build tools (for C++ extensions if needed)

### Installing Python Versions

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.8 python3.9 python3.10 python3.11 python3.12
sudo apt install python3-pip python3-venv
```

**macOS (using pyenv):**
```bash
brew install pyenv
pyenv install 3.8.18
pyenv install 3.9.18
pyenv install 3.10.13
pyenv install 3.11.7
pyenv install 3.12.1
pyenv global 3.11.7 3.10.13 3.9.18 3.8.18 3.12.1
```

**Windows:**
Download and install from https://www.python.org/downloads/

## Runner Maintenance

### Updating the Runner
```bash
cd actions-runner
sudo ./svc.sh stop
./config.sh remove --token YOUR_TOKEN
# Download new version and configure again
sudo ./svc.sh install
sudo ./svc.sh start
```

### Monitoring
- Check runner status: Settings → Actions → Runners
- View logs: `actions-runner/_diag/` directory
- Check service status: `sudo ./svc.sh status`

### Troubleshooting

**Runner offline:**
- Check if service is running: `sudo ./svc.sh status`
- Restart service: `sudo ./svc.sh restart`
- Check network connectivity to GitHub

**Build failures:**
- Verify Python versions are installed
- Check disk space: `df -h`
- Review workflow logs in GitHub Actions UI

**Permission issues:**
- Ensure runner user has proper permissions
- Check file ownership in workspace

## Security Considerations

### Best Practices
1. **Dedicated machine**: Use a separate machine for runners
2. **Regular updates**: Keep OS and dependencies updated
3. **Limited access**: Restrict who can modify workflows
4. **Secrets management**: Never log sensitive information
5. **Network security**: Use firewall rules appropriately

### GitHub Actions Security
- Runners have access to repository secrets
- Review workflow changes in PRs carefully
- Use branch protection rules
- Limit runner access to specific repositories

## Workflow Files

### ci.yml (Self-Hosted)
Main CI/CD pipeline using self-hosted runners:
- Runs on push to main
- Runs on pull requests
- Runs on releases
- Tests with Python 3.8-3.12
- Linting and type checking
- Builds wheels
- Publishes to PyPI (on release)

### sonarqube.yml (Self-Hosted)
Code quality analysis using self-hosted runners:
- Runs on push to main
- Runs on pull requests
- Generates coverage reports
- Performs SonarQube scan
- Checks quality gates

### scheduled-ci.yml (GitHub-Hosted)
Monthly comprehensive testing on GitHub infrastructure:
- Runs monthly on the 1st at 00:00 UTC
- Can be triggered manually
- Multi-platform testing (Ubuntu, macOS, Windows)
- Tests with Python 3.8-3.12
- Full CI/CD pipeline
- SonarQube analysis

## Manual Workflow Triggers

You can manually trigger the scheduled workflow:
1. Go to **Actions** tab
2. Select **Scheduled CI (GitHub Runners)**
3. Click **Run workflow**
4. Choose branch and click **Run workflow**

## Cost Comparison

### Self-Hosted Runners
- **Cost**: Infrastructure costs only (electricity, hardware)
- **Performance**: Typically faster (no queue)
- **Maintenance**: Requires setup and upkeep

### GitHub-Hosted Runners
- **Cost**: Free for public repos (within limits)
- **Performance**: May have queue times
- **Maintenance**: None required

## Support

For issues related to:
- **Workflow configuration**: Check GitHub Actions documentation
- **Runner setup**: See GitHub's self-hosted runner docs
- **Project-specific issues**: Open an issue in this repository

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners)
- [Runner application releases](https://github.com/actions/runner/releases)
