# Publishing to PyPI

This guide walks through publishing your package to PyPI.

## Prerequisites

1. **Python 3.8+** installed
2. **Build tools**:
   ```bash
   pip install build twine
   ```
3. **PyPI Account**: Create one at https://pypi.org/account/register/

## Step 1: Verify Your Package Structure

Your package should have this structure:
```
ezDebugger/
├── ezDebugger/
│   ├── __init__.py
│   └── debugger.py
├── pyproject.toml
├── README.md
├── LICENSE
├── MANIFEST.in
└── .gitignore
```

**Note**: If you want to use the modern structure with an `ezDebugger/` subdirectory, move your files like this:
```bash
mkdir ezDebugger
move __init__.py ezDebugger/
move debugger.py ezDebugger/
```

This is optional but recommended for larger projects.

## Step 2: Build Your Distribution

From your project root directory:

```bash
python -m build
```

This creates:
- `dist/ezDebugger-0.1.0.tar.gz` (source distribution)
- `dist/ezDebugger-0.1.0-py3-none-any.whl` (wheel)

## Step 3: Test Locally (Optional but Recommended)

```bash
pip install dist/ezDebugger-0.1.0-py3-none-any.whl
python -c "from ezDebugger import Logger; print(Logger)"
```

## Step 4: Upload to PyPI

### Option A: Using Twine (Recommended)

```bash
twine upload dist/*
```

You'll be prompted for your PyPI credentials.

### Option B: Using PyPI Token (More Secure)

1. Generate a PyPI API token at https://pypi.org/manage/account/
2. Store it securely (don't commit to git!)
3. Upload:
   ```bash
   twine upload dist/* --username __token__ --password <your-token>
   ```

## Step 5: Test Your Published Package

After a few minutes, your package will be available on PyPI. Test installation:

```bash
pip install ezDebugger
python -c "from ezDebugger import Logger; print(Logger)"
```

## Before Publishing

Make sure to:

1. **Update pyproject.toml**:
   - Keep the author metadata minimal and appropriate for PyPI
   - Update the Repository URL to your GitHub repo
   - Verify the version number is unique

2. **Check your README**:
   - Verify all examples work correctly
   - Make sure formatting looks good on PyPI (check at https://pypi.org with a preview tool)

3. **Test the package**:
   - Install it in a clean virtual environment
   - Run the examples from README

## Updating Your Package

To release a new version:

1. Update version in `pyproject.toml`
2. Update version in `__init__.py`
3. Update `CHANGELOG.md` or release notes
4. Commit changes to git
5. Run `python -m build`
6. Run `twine upload dist/*`

## Troubleshooting

**Error: "400 Client Error: Invalid distribution"**
- Check that `pyproject.toml` has no syntax errors
- Verify version follows PEP 440 (e.g., "0.1.0")
- Ensure README.md renders as valid reStructuredText

**Error: "403 Forbidden: Invalid API token"**
- Verify token is correct and hasn't expired
- Use the exact token from PyPI settings

**Package already exists with this version**
- You must increment the version number before uploading again
- Previous versions cannot be overwritten

## Resources

- [PyPI Help](https://pypi.org/help/)
- [Python Packaging Guide](https://packaging.python.org/)
- [PEP 427 - Wheel Format](https://www.python.org/dev/peps/pep-0427/)
- [PEP 440 - Version Identification](https://www.python.org/dev/peps/pep-0440/)
