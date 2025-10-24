# SonarCloud Quick Start Guide

## Current Issue
The SonarQube workflow is failing because `SONAR_TOKEN` is not configured.

## Steps to Fix (5 minutes)

### 1. Set up SonarCloud Project

1. Go to https://sonarcloud.io/
2. Click "Log in" and choose "GitHub"
3. Click the "+" button (top right) and select "Analyze new project"
4. Select `Bernardi-sh/pygraham` from the list
5. Click "Set Up"

### 2. Configure the Project

1. Choose "With GitHub Actions" as the analysis method
2. SonarCloud will show you need to create a token

### 3. Generate Token

1. Click on your profile icon (top right) → "My Account"
2. Go to the "Security" tab
3. Under "Generate Tokens":
   - Name: `GitHub Actions - pygraham`
   - Type: `Global Analysis Token` or `Project Analysis Token`
   - Expiration: Choose "No expiration" or set as needed
4. Click "Generate"
5. **Copy the token immediately** (you won't be able to see it again!)

### 4. Add Token to GitHub

1. Go to https://github.com/Bernardi-sh/pygraham/settings/secrets/actions
2. Click "New repository secret"
3. Name: `SONAR_TOKEN`
4. Value: Paste the token you copied from SonarCloud
5. Click "Add secret"

### 5. Update Project Key (if needed)

Check your SonarCloud project key:
1. In SonarCloud, go to your project
2. Look at the URL: `https://sonarcloud.io/dashboard?id=YOUR_PROJECT_KEY`
3. Or go to Project Settings → General Settings

If your project key is different from `bernardi-sh_pygraham`, update `sonar-project.properties`:
```properties
sonar.projectKey=YOUR_ACTUAL_PROJECT_KEY
sonar.organization=YOUR_ORGANIZATION_KEY
```

### 6. Trigger a New Build

After adding the token, trigger a new build:
- Push a new commit, or
- Go to Actions → Select "SonarQube Analysis" → "Run workflow"

### 7. View Results

Once the analysis completes:
1. Go to https://sonarcloud.io/
2. Find your project `pygraham`
3. View the dashboard with:
   - Quality Gate status
   - Code coverage percentage
   - Bugs, vulnerabilities, code smells
   - Technical debt

## Expected Results

After setup, you should see:
- ✅ SonarQube Analysis workflow passing
- 📊 Coverage percentage in SonarCloud
- 🎯 Quality gate status
- 🐛 Code quality metrics

## Troubleshooting

**Token not working?**
- Make sure you copied the entire token
- Check token hasn't expired
- Verify token type is "Global Analysis Token" or "Project Analysis Token"

**Wrong project key?**
- Check the project key in SonarCloud matches `sonar-project.properties`
- Organization must match your SonarCloud organization

**Still failing?**
- Check GitHub Actions logs for specific errors
- Verify `SONAR_TOKEN` secret is set correctly
- Make sure SonarCloud project is active
