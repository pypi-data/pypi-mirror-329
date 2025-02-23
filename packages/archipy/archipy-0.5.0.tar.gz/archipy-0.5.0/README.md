# ArchiPy

[TOC]

------------

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.12.x
- Docker (optional)

## 🛠️ Installation

1. **Setup Project Prerequisites**
   ```bash
   sudo apt install make && make setup
   ```

2. **Install Dependencies**
   ```bash
   make install
   ```

3. **Install Development Dependencies** (Optional)
   ```bash
   make install-dev
   ```

## 🎯 Available Commands

Run `make help` to see all available commands:

```bash
make help
```

### Common Commands

- 🧹 **Clean Project**
  ```bash
  make clean
  ```

- ✨ **Format Code**
  ```bash
  make format
  ```

- 🔍 **Run Linters**
  ```bash
  make lint
  ```

- 🧪 **Run Tests**
  ```bash
  make behave
  ```

- 🏗️ **Build Project**
  ```bash
  make build
  ```

## 🔖 Version Management

We follow [Semantic Versioning](https://semver.org/) principles with support for Release Candidates (RC). Our versioning system provides flexible options for version management.

### Version Format

- Regular versions: `X.Y.Z` (e.g., `1.2.3`)
- Release Candidate versions: `X.Y.Zrc` (e.g., `1.2.3rc`)

Where:
- `X` = Major version (breaking changes)
- `Y` = Minor version (new features, backward-compatible)
- `Z` = Patch version (bug fixes, backward-compatible)
- `rc` = Release Candidate suffix (pre-release versions)

### Version Bumping Commands

#### Basic Version Bumping

- 🤏 **Patch Version** (Bug fixes)
  ```bash
  make bump-patch
  ```

- 🍾 **Minor Version** (New features)
  ```bash
  make bump-minor
  ```

- ⚠️ **Major Version** (Breaking changes)
  ```bash
  make bump-major
  ```

#### Release Candidate Versions

Add `rc=true` to create release candidate versions:

```bash
make bump-patch rc=true   # Creates a release candidate (e.g., 1.2.3rc)
make bump-minor rc=true   # Creates a release candidate (e.g., 1.3.0rc)
make bump-major rc=true   # Creates a release candidate (e.g., 2.0.0rc)
```

#### Custom Version Messages

Add a custom message to your version bump:

```bash
make bump-patch message="Your custom message"
```

Combine with RC flag:
```bash
make bump-patch rc=true message="Release candidate for bug fix"
```

#### Version Bumping Behavior

1. **Regular Version Bumping**:
   - From `1.2.3` to `1.2.4`: `make bump-patch`
   - From `1.2.3` to `1.3.0`: `make bump-minor`
   - From `1.2.3` to `2.0.0`: `make bump-major`

2. **RC Version Bumping**:
   - From `1.2.3` to `1.2.4rc`: `make bump-patch rc=true`
   - From `1.2.3rc` to `1.2.3`: `make bump-patch` (finalizes RC)
   - From `1.2.3rc` to `1.2.4rc`: `make bump-patch rc=true`

3. **Version Messages**:
   - Without message: Uses last git commit message
   - With message: Uses provided custom message

## 🐳 Docker Support

Build and run with Docker:

```bash
# Build Docker image
make docker-build

# Run Docker container
make docker-run
```

## 🔄 Pre-commit Hooks

1. **Install Pre-commit Hooks**
   ```bash
   poetry run pre-commit install
   poetry run pre-commit autoupdate
   ```

2. **Run Pre-commit Checks**
   ```bash
   poetry run pre-commit run --all-files
   ```

## ✅ Development Workflow

1. **Run All Checks**
   ```bash
   make check
   ```

2. **Run CI Pipeline Locally**
   ```bash
   make ci
   ```

## 🔄 Updating Dependencies

Keep your dependencies up to date:

```bash
make update
```
