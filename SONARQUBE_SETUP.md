# SonarQube Setup Guide

This project includes SonarQube integration for continuous code quality analysis.

## Features

SonarQube will analyze:
- **Code Quality**: Bugs, vulnerabilities, code smells
- **Test Coverage**: Line and branch coverage from pytest
- **Code Duplication**: Identifies duplicate code blocks
- **Security**: Security hotspots and vulnerabilities
- **Maintainability**: Technical debt and complexity metrics
- **Reliability**: Bug detection and reliability ratings

## Setup Instructions

### 1. Create a SonarQube Account

Choose one of the following options:

#### Option A: SonarCloud (Recommended for Open Source)
1. Go to [SonarCloud](https://sonarcloud.io/)
2. Sign up with your GitHub account
3. Create a new organization or use existing one
4. Import your repository

#### Option B: Self-Hosted SonarQube
1. Install SonarQube on your server
2. Create a new project
3. Generate a token

### 2. Configure GitHub Secrets

Add the following secrets to your GitHub repository:

1. Go to your repository on GitHub
2. Navigate to `Settings` > `Secrets and variables` > `Actions`
3. Add the following secret:

   **For SonarCloud (Default):**
   - `SONAR_TOKEN`: Your SonarCloud token

   Note: `SONAR_HOST_URL` is not needed for SonarCloud as it uses the default URL.

   **For Self-Hosted SonarQube:**
   - `SONAR_TOKEN`: Your SonarQube project token
   - `SONAR_HOST_URL`: Your SonarQube server URL (e.g., `https://sonarqube.example.com`)

   Note: If using self-hosted, you'll need to modify the GitHub Action workflow to include `SONAR_HOST_URL`.

### 3. Update sonar-project.properties

Edit the `sonar-project.properties` file to match your project:

```properties
# Update these values
sonar.projectKey=your-org_your-project
sonar.organization=your-org  # Only for SonarCloud
```

### 4. Generate Token

#### For SonarCloud:
1. Go to [SonarCloud](https://sonarcloud.io/)
2. Click on your profile (top right) > `My Account`
3. Go to `Security` tab
4. Generate a new token with a descriptive name (e.g., "GitHub Actions")
5. Copy the token and add it as `SONAR_TOKEN` secret in GitHub

#### For Self-Hosted:
1. Log in to your SonarQube instance
2. Go to `My Account` > `Security`
3. Generate a new token
4. Copy and add it as `SONAR_TOKEN` secret in GitHub

## Quality Gates

The default quality gate checks:
- **Coverage**: At least 80% code coverage
- **Duplications**: Less than 3% duplicated code
- **Maintainability**: A rating on new code
- **Reliability**: No new bugs
- **Security**: No new vulnerabilities

You can customize these thresholds in SonarCloud/SonarQube settings.

## Viewing Results

### On GitHub
- Quality gate status will be shown in pull request checks
- Failed quality gates will be marked as failed checks

### On SonarCloud/SonarQube
1. Go to your project dashboard
2. View detailed metrics:
   - **Overview**: Quality gate status, coverage, issues
   - **Issues**: All bugs, vulnerabilities, and code smells
   - **Measures**: Detailed metrics and history
   - **Code**: Browse code with inline issue annotations
   - **Activity**: Historical analysis data

## Local Analysis (Optional)

You can run SonarQube analysis locally:

### 1. Install SonarScanner

**macOS:**
```bash
brew install sonar-scanner
```

**Linux:**
```bash
# Download from https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/
wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-*.zip
unzip sonar-scanner-cli-*.zip
export PATH=$PATH:/path/to/sonar-scanner/bin
```

**Windows:**
Download from [SonarQube website](https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/)

### 2. Run Analysis

```bash
# Generate coverage report first
pytest tests/ --cov=pygraham --cov-report=xml

# Run SonarQube analysis
sonar-scanner \
  -Dsonar.projectKey=your-project-key \
  -Dsonar.organization=your-org \
  -Dsonar.sources=pygraham \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.login=your-token
```

## Badge

Once configured, add the SonarQube badge to your README:

**For SonarCloud:**
```markdown
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=your-org_your-project&metric=alert_status)](https://sonarcloud.io/dashboard?id=your-org_your-project)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=your-org_your-project&metric=coverage)](https://sonarcloud.io/dashboard?id=your-org_your-project)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=your-org_your-project&metric=bugs)](https://sonarcloud.io/dashboard?id=your-org_your-project)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=your-org_your-project&metric=code_smells)](https://sonarcloud.io/dashboard?id=your-org_your-project)
```

## Troubleshooting

### Analysis Fails
- Check that `SONAR_TOKEN` and `SONAR_HOST_URL` secrets are correctly set
- Verify the token has proper permissions
- Check SonarQube/SonarCloud server is accessible

### Coverage Not Showing
- Ensure `coverage.xml` is generated before SonarQube scan
- Check `sonar.python.coverage.reportPaths` points to correct file
- Verify coverage report format is XML

### Quality Gate Fails
- Review the specific issues in SonarCloud/SonarQube dashboard
- Fix critical bugs and vulnerabilities first
- Consider adjusting quality gate thresholds if too strict

## Resources

- [SonarCloud Documentation](https://docs.sonarcloud.io/)
- [SonarQube Documentation](https://docs.sonarqube.org/)
- [SonarQube GitHub Action](https://github.com/SonarSource/sonarqube-scan-action)
- [Python Analysis Parameters](https://docs.sonarqube.org/latest/analysis/languages/python/)

## Metrics Explained

- **Bugs**: Issues that represent wrong or unexpected behavior
- **Vulnerabilities**: Security-related issues
- **Code Smells**: Maintainability issues
- **Coverage**: Percentage of code covered by tests
- **Duplications**: Percentage of duplicated code
- **Complexity**: Cyclomatic complexity
- **Technical Debt**: Estimated time to fix all maintainability issues
