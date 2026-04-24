# Contributing to pyufunc

Thank you for helping improve `pyufunc`. Contributions can include bug
reports, utility function ideas, documentation fixes, tests, examples, and
source code changes.

Please follow the [Code of Conduct](CODE_OF_CONDUCT.md) when participating in
the project.

## Ways to Contribute

- Report bugs or request enhancements in
  [GitHub Issues](https://github.com/xyluo25/pyufunc/issues).
- Improve documentation in `README.md`, `docs/`, or docstrings.
- Add tests for existing utilities.
- Propose or implement new utility functions that are broadly useful.
- Review open pull requests and issues.

For large changes or new utility categories, open an issue first so maintainers
can discuss the scope and expected API before implementation starts.

## Development Setup

`pyufunc` supports Python 3.10 and newer.

```bash
git clone https://github.com/YOUR_USERNAME/pyufunc.git
cd pyufunc
git remote add upstream https://github.com/xyluo25/pyufunc.git

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install pytest flake8 pylint build
```

The runtime dependencies are declared in `requirements.txt` and loaded through
`pyproject.toml`.

## Project Layout

- `pyufunc/`: package source code, organized by utility category.
- `tests/`: pytest test suite.
- `docs/`: documentation source and generated markdown utility lists.
- `.github/workflows/`: CI workflows for tests, linting, and package builds.
- `pyproject.toml`: package metadata and build configuration.

## Working on Changes

1. Create a branch from `main`.

   ```bash
   git fetch upstream
   git checkout main
   git rebase upstream/main
   git checkout -b feature/short-description
   ```

2. Keep changes focused. One pull request should solve one problem or add one
   related group of utilities.

3. Add or update tests for behavior changes.

4. Update documentation when changing public APIs, adding utilities, or changing
   installation or usage instructions.

5. Keep public utility functions discoverable through the package's existing
   module and `__init__.py` export patterns.

## Adding a Utility Function

When adding a new utility function:

- Place it in the most relevant `pyufunc/util_*` module.
- Reuse existing naming, import, and optional dependency patterns.
- Include a clear docstring with parameters, return values, and a short example
  when helpful.
- Avoid adding mandatory dependencies for niche functionality. If a dependency
  is only needed by one utility, follow the local pattern for optional imports
  and user-facing install guidance.
- Add pytest coverage in `tests/`.
- Update README or docs lists if the function should be visible to users.

## Tests and Checks

Run the test suite before opening a pull request:

```bash
pytest
```

Run the same syntax-focused flake8 check used by CI:

```bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

Optional local pylint check:

```bash
pylint $(git ls-files "*.py")
```

On Windows PowerShell, use:

```powershell
pylint (git ls-files "*.py")
```

Build the package locally when changing packaging metadata or included data
files:

```bash
python -m build
```

## Documentation

Documentation lives under `docs/`. If your change affects user-facing behavior,
update the relevant documentation page or README section.

To work on the Sphinx documentation, install the documentation dependencies:

```bash
python -m pip install -r docs/source/requirements_dev.txt
```

Then build from the docs source directory:

```bash
cd docs/source
sphinx-build -b html . _build/html
```

## Pull Request Checklist

Before submitting a pull request, confirm that:

- The change is based on the latest `main` branch.
- Tests pass locally, or the PR explains why they could not be run.
- New behavior has focused test coverage.
- Documentation and examples are updated when needed.
- Public APIs are named consistently with the existing package.
- The PR description explains what changed and why.
- Related issues are linked with `Fixes #123` or `Closes #123` when applicable.

## Commit Messages

Use clear, concise commit messages. Conventional commit prefixes are welcome:

- `feat:` for new features or utilities.
- `fix:` for bug fixes.
- `docs:` for documentation-only changes.
- `test:` for tests.
- `refactor:` for behavior-preserving code changes.
- `chore:` for maintenance.

Example:

```text
feat(pathio): add helper for resolving user paths
```

## License

By contributing to `pyufunc`, you agree that your contributions will be licensed
under the project's [MIT License](LICENSE).
