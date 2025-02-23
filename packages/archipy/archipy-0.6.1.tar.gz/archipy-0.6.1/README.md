# ArchiPy 🐍

**Architecture + Python – Perfect for Structured Design**

ArchiPy is a Python project designed to provide a robust and structured architecture for building scalable and
maintainable applications. It integrates modern Python tools and libraries to streamline development, testing, and
deployment.

---

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Development](#-development)
- [Version Management](#-version-management)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- **Modern Python Stack**: Built with Python 3.13 and leveraging tools like `pydantic`, `fastapi`, `gRPC` and
  `sqlalchemy`.
- **Modular Design**: Optional dependencies for Redis, gRPC, PostgreSQL, Prometheus, and more.
- **Type Safety**: Enforced by `mypy` and `pydantic` for robust code.
- **Testing**: Integrated with `pytest` and `behave` for comprehensive testing.
- **Linting and Formatting**: Uses `ruff` and `black` for clean and consistent code.
- **Pre-commit Hooks**: Automates code quality checks before commits.
- **Dependency Management**: Managed by `poetry` for reproducible builds.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.13 or higher**
  `archipy` is compatible with Python 3.13 and above but does not support Python 4 or higher.
  To check your Python version, run:
  ```bash
  python --version
  ```
  If your Python version is lower than 3.13, [download and install the latest version of Python](https://www.python.org/downloads/).

- **Poetry** (for dependency management)
  Poetry is required to manage dependencies and install the project. If you don’t have Poetry installed, follow the [official installation guide](https://python-poetry.org/docs/).

---


## 🚀 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/SyntaxArc/ArchiPy.git
   cd ArchiPy
   ```

2. **Set Up the Project**
   ```bash
   make setup
   ```

3. **Install Dependencies**
   ```bash
   make install
   ```

4. **Install Development Dependencies** (Optional)
   ```bash
   make install-dev
   ```

---

## 🎯 Usage


### Installing the Project

You can install the project and its dependencies using either `pip` or `poetry`. Below are the instructions for both.

#### Using `pip`

To install the core library:

```bash
pip install archipy
```

To install the library with optional dependencies (e.g., `redis`, `fastapi`, etc.):

```bash
pip install archipy[redis,fastapi]
```

#### Using `poetry`

To add the core library to your project:

```bash
poetry add archipy
```

To add the library with optional dependencies (e.g., `redis`, `fastapi`, etc.):

```bash
poetry add archipy[redis,fastapi]
```

---

### Optional Dependencies

The library provides optional dependencies for additional functionality. You can install them as needed:

| Feature              | Installation Command            |
|----------------------|---------------------------------|
| Redis                | `archipy[redis]`                |
| Elastic APM          | `archipy[elastic-apm]`          |
| FastAPI              | `archipy[fastapi]`              |
| JWT                  | `archipy[jwt]`                  |
| Kavenegar            | `archipy[kavenegar]`            |
| Prometheus           | `archipy[prometheus]`           |
| Sentry               | `archipy[sentry]`               |
| Dependency Injection | `archipy[dependency-injection]` |
| Scheduler            | `archipy[scheduler]`            |
| gRPC                 | `archipy[grpc]`                 |
| PostgreSQL           | `archipy[postgres]`             |
| aiosqlite            | `archipy[aiosqlite]`            |

---

### Troubleshooting Installation Issues

If you encounter issues during installation, ensure that:

1. Your Python version is **3.13 or higher**.
2. Your package manager (`pip` or `poetry`) is up to date.
3. You have the necessary build tools installed (e.g., `setuptools`, `wheel`).

For example, to upgrade `pip`, run:

```bash
pip install --upgrade pip
```

---

### Available Commands

Run `make help` to see all available commands:

```bash
make help
```

#### Common Commands

- **Format Code**
  ```bash
  make format
  ```

- **Run Linters**
  ```bash
  make lint
  ```

- **Run Tests**
  ```bash
  make behave
  ```

- **Build the Project**
  ```bash
  make build
  ```

- **Clean Build Artifacts**
  ```bash
  make clean
  ```

---

## 🛠️ Development

### Development Workflow

1. **Run All Checks**
   ```bash
   make check
   ```

2. **Run CI Pipeline Locally**
   ```bash
   make ci
   ```

3. **Update Dependencies**
   ```bash
   make update
   ```

### Pre-commit Hooks

1. **Install Pre-commit Hooks**
   ```bash
   poetry run pre-commit install
   ```

2. **Run Pre-commit Checks**
   ```bash
   poetry run pre-commit run --all-files
   ```

---

## 🔖 Version Management

We follow [Semantic Versioning (SemVer)](https://semver.org/) principles.

### Version Bumping Commands

- **Bump Patch Version** (Bug fixes)
  ```bash
  make bump-patch
  ```

- **Bump Minor Version** (New features)
  ```bash
  make bump-minor
  ```

- **Bump Major Version** (Breaking changes)
  ```bash
  make bump-major
  ```

#### Custom Version Messages

Add a custom message to your version bump:

```bash
make bump-patch message="Your custom message"
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

---

## 📄 License

This project is licensed under the terms of the [LICENSE](LICENSE) file.

---

## 📞 Contact

For questions or feedback, feel free to reach out:

- **Mehdi Einali**: [einali@gmail.com](mailto:einali@gmail.com)
- **Hossein Nejati**: [hosseinnejati14@gmail.com](mailto:hosseinnejati14@gmail.com)

---

## 🔗 Links

- **GitHub Repository**: [https://github.com/SyntaxArc/ArchiPy](https://github.com/SyntaxArc/ArchiPy)
- **Documentation**: [https://github.com/SyntaxArc/ArchiPy#readme](https://github.com/SyntaxArc/ArchiPy#readme)

---
