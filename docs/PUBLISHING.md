# Publishing Guide

This document explains how to publish `awesome-copilot-agents` to PyPI using GitHub Actions.

## Overview

The project uses **Trusted Publishing** with GitHub Actions to automatically publish to PyPI when you push version tags. This is more secure than using API tokens.

## Initial Setup (One-Time)

### Step 1: Create PyPI Account

1. Go to https://pypi.org
2. Create an account
3. Enable 2FA (required for trusted publishing)

### Step 2: Create PyPI Project

1. Go to https://pypi.org/manage/account/publishing/
2. Click "Add a new project"
3. Enter:
   - **Project name**: `awesome-copilot-agents`
   - **Owner**: Your PyPI username
   - Leave other fields blank for now

### Step 3: Configure Trusted Publishing

1. Go to https://pypi.org/manage/account/publishing/
2. Find "awesome-copilot-agents" in your projects list
3. Click the project name
4. Click "Add a new publisher"
5. Fill in the form:
   ```
   PyPI Project Name: awesome-copilot-agents
   Owner: your-username
   Repository name: awesome-skills
   Workflow name: publish.yml
   Environment name: pypi
   ```
6. Click "Add"

### Step 4: Verify GitHub Repository

Make sure your GitHub repository has:
- **Owner**: Your GitHub username
- **Repository name**: `awesome-skills`
- **Workflow**: `.github/workflows/publish.yml` exists

## Publishing a Release

### Option 1: Using Tags (Recommended)

```bash
# 1. Update version in pyproject.toml
# Change version = "0.1.0" to version = "0.2.0"

# 2. Commit the change
git add pyproject.toml
git commit -m "Bump version to 0.2.0"

# 3. Create and push tag
git tag v0.2.0
git push origin v0.2.0

# 4. GitHub Actions will automatically:
#    - Build the package
#    - Run tests
#    - Publish to PyPI
#    - Create GitHub Release with assets
```

### Option 2: Manual Publishing

If GitHub Actions fails or you need to publish manually:

```bash
# Build the package
python -m build

# Upload to PyPI (requires twine and API token)
twine upload dist/*
```

## Version Tag Format

Tags must follow semantic versioning with a `v` prefix:

- `v0.1.0` - Initial release
- `v0.1.1` - Patch release (bug fixes)
- `v0.2.0` - Minor release (new features, backward compatible)
- `v1.0.0` - Major release (breaking changes)

## What Happens on Tag Push

1. **Build Job**:
   - Checks out code
   - Sets up Python 3.12
   - Builds source distribution and wheel
   - Validates package with `twine check`

2. **Publish Job**:
   - Downloads built artifacts
   - Publishes to PyPI using trusted publishing
   - No API tokens needed!

3. **Release Job**:
   - Creates GitHub Release with auto-generated notes
   - Attaches distribution files as release assets

## CI Workflow

The CI workflow runs on every push to `master`/`main` and on all pull requests:

- Tests package builds on Python 3.11, 3.12, 3.13
- Validates agent file structure
- Checks CLI functionality

## Troubleshooting

### Publisher not found

If you get "Publisher not found" error:
- Verify PyPI project name matches exactly: `awesome-copilot-agents`
- Verify GitHub repository name matches
- Verify workflow name is `publish.yml`
- Re-check the trusted publishing configuration

### Workflow fails to authenticate

If authentication fails:
- Ensure 2FA is enabled on PyPI
- Verify the environment name is `pypi`
- Check that the workflow has `id-token: write` permission

### Build fails

If the build fails:
- Check the "Build distribution" job logs
- Ensure all tests pass locally first
- Verify `pyproject.toml` is valid

## Updating Agent Files

Agent files are bundled with the package. To update agents:

1. Modify files in `agents/` directory
2. Commit changes
3. Bump version in `pyproject.toml`
4. Tag and push

Users update with:
```bash
pip install --upgrade awesome-copilot-agents
awesome-copilot install
```

## Resources

- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions for Python](https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
- [Semantic Versioning](https://semver.org/)
