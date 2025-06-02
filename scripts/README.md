# Scripts Directory

This directory contains utility scripts for the App Store Icon Hunter project.

## PyPI Upload Scripts

Two scripts are provided for uploading the package to PyPI:

### 1. Python Script (`upload_to_pypi.py`)
A comprehensive Python script with detailed error handling and progress reporting.

**Usage:**
```bash
# Normal upload to PyPI
python3 scripts/upload_to_pypi.py

# Test upload to TestPyPI
python3 scripts/upload_to_pypi.py --test

# Upload existing build without rebuilding
python3 scripts/upload_to_pypi.py --skip-build

# Show help
python3 scripts/upload_to_pypi.py --help
```

### 2. Bash Script (`upload_to_pypi.sh`)
A simpler bash script for quick uploads.

**Usage:**
```bash
# Normal upload to PyPI
./scripts/upload_to_pypi.sh

# Test upload to TestPyPI
./scripts/upload_to_pypi.sh --test

# Upload existing build without rebuilding
./scripts/upload_to_pypi.sh --skip-build

# Show help
./scripts/upload_to_pypi.sh --help
```

## What These Scripts Do

1. **Clean build artifacts** - Removes old dist/, build/, and .egg-info/ directories
2. **Backup LICENSE** - Temporarily moves LICENSE file to avoid metadata conflicts
3. **Build package** - Creates source distribution and wheel using `setup.py sdist` and `pip wheel`
4. **Restore LICENSE** - Puts the LICENSE file back
5. **Upload to PyPI** - Uses twine to upload to PyPI or TestPyPI

## Prerequisites

Before using these scripts, make sure you have:

1. **Updated version** in `setup.py`
2. **Installed twine**: `pip install twine`
3. **PyPI API token** ready for authentication

## Testing Before Release

Always test your package first:

```bash
# Upload to TestPyPI first
./scripts/upload_to_pypi.sh --test

# Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ app-store-icon-hunter

# If everything works, upload to real PyPI
./scripts/upload_to_pypi.sh
```

## Manual Process (Alternative)

If you prefer to do it manually:

```bash
# Clean and build
rm -rf dist/ build/ *.egg-info/
mv LICENSE LICENSE.backup  # Temporary workaround
python3 setup.py sdist
pip3 wheel . --no-deps
mv *.whl dist/
mv LICENSE.backup LICENSE

# Upload
python3 -m twine upload dist/*
```

## Troubleshooting

### License Metadata Issues
The scripts automatically handle the "license-file" metadata issue by temporarily backing up the LICENSE file during build. This is a workaround for setuptools automatically adding license metadata that causes upload conflicts.

### Authentication
When prompted, use your PyPI API token (not username/password). The token should start with `pypi-`.

### Build Failures
If the build fails, check that:
- All dependencies are properly specified in `setup.py`
- The package structure is correct
- No syntax errors in your code
