#!/usr/bin/env python3
"""
PyPI Upload Script for App Store Icon Hunter

This script automates the process of building and uploading the package to PyPI.
It handles the build process and upload while avoiding the license metadata issues
we encountered during initial publishing.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"   {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"   {e.stderr.strip()}")
        return False


def clean_build_artifacts():
    """Clean up build artifacts before building."""
    artifacts = ['dist/', 'build/', '*.egg-info/', '__pycache__/']
    
    print("🧹 Cleaning build artifacts...")
    for pattern in artifacts:
        if pattern.endswith('/'):
            # Directory
            dir_name = pattern.rstrip('/')
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
                print(f"   Removed {dir_name}/")
        else:
            # File pattern
            for file in Path('.').glob(pattern):
                if file.is_dir():
                    shutil.rmtree(file)
                else:
                    file.unlink()
                print(f"   Removed {file}")


def backup_license():
    """Temporarily backup LICENSE file to avoid metadata issues."""
    if os.path.exists('LICENSE'):
        shutil.move('LICENSE', 'LICENSE.backup')
        print("📄 Temporarily backed up LICENSE file")
        return True
    return False


def restore_license():
    """Restore LICENSE file after build."""
    if os.path.exists('LICENSE.backup'):
        shutil.move('LICENSE.backup', 'LICENSE')
        print("📄 Restored LICENSE file")


def build_package():
    """Build the package using traditional setup.py method."""
    print("📦 Building package...")
    
    # Build source distribution
    if not run_command("python3 setup.py sdist", "Building source distribution"):
        return False
    
    # Build wheel using pip (avoids metadata issues)
    if not run_command("pip3 wheel . --no-deps", "Building wheel"):
        return False
    
    # Move wheel to dist directory
    wheel_files = list(Path('.').glob('*.whl'))
    if wheel_files:
        wheel_file = wheel_files[0]
        dist_dir = Path('dist')
        dist_dir.mkdir(exist_ok=True)
        shutil.move(str(wheel_file), f"dist/{wheel_file.name}")
        print(f"   Moved {wheel_file.name} to dist/")
    
    return True


def upload_to_pypi(test=False):
    """Upload package to PyPI or TestPyPI."""
    repository = "testpypi" if test else "pypi"
    repo_url = "https://test.pypi.org/legacy/" if test else "https://upload.pypi.org/legacy/"
    
    print(f"🚀 Uploading to {'TestPyPI' if test else 'PyPI'}...")
    
    command = f"python3 -m twine upload dist/*"
    if test:
        command += f" --repository-url {repo_url}"
    
    return run_command(command, f"Uploading to {'TestPyPI' if test else 'PyPI'}")


def main():
    """Main upload process."""
    print("🎯 App Store Icon Hunter - PyPI Upload Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('setup.py'):
        print("❌ Error: setup.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Parse command line arguments
    test_upload = '--test' in sys.argv
    skip_build = '--skip-build' in sys.argv
    
    if test_upload:
        print("🧪 Test mode: Will upload to TestPyPI")
    
    try:
        # Step 1: Clean build artifacts
        if not skip_build:
            clean_build_artifacts()
            
            # Step 2: Backup LICENSE temporarily to avoid metadata issues
            license_backed_up = backup_license()
            
            # Step 3: Build package
            if not build_package():
                print("❌ Build failed!")
                return False
            
            # Step 4: Restore LICENSE
            if license_backed_up:
                restore_license()
        
        # Step 5: Check if dist files exist
        dist_files = list(Path('dist').glob('*'))
        if not dist_files:
            print("❌ No distribution files found in dist/")
            return False
        
        print("📋 Distribution files ready:")
        for file in dist_files:
            print(f"   {file}")
        
        # Step 6: Upload to PyPI
        if upload_to_pypi(test=test_upload):
            repo_name = "TestPyPI" if test_upload else "PyPI"
            print(f"✅ Successfully uploaded to {repo_name}!")
            
            if test_upload:
                print("\n🔗 View your package at: https://test.pypi.org/project/app-store-icon-hunter/")
                print("📦 Test install with: pip install --index-url https://test.pypi.org/simple/ app-store-icon-hunter")
            else:
                print("\n🔗 View your package at: https://pypi.org/project/app-store-icon-hunter/")
                print("📦 Install with: pip install app-store-icon-hunter")
            
            return True
        else:
            print("❌ Upload failed!")
            return False
            
    except KeyboardInterrupt:
        print("\n⏹️  Upload cancelled by user")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        # Always restore LICENSE if it was backed up
        if os.path.exists('LICENSE.backup'):
            restore_license()


def show_help():
    """Show help information."""
    print("""
App Store Icon Hunter - PyPI Upload Script

Usage:
  python3 scripts/upload_to_pypi.py [options]

Options:
  --test        Upload to TestPyPI instead of PyPI
  --skip-build  Skip the build process and upload existing dist/ files
  --help        Show this help message

Examples:
  # Normal upload to PyPI
  python3 scripts/upload_to_pypi.py
  
  # Test upload to TestPyPI
  python3 scripts/upload_to_pypi.py --test
  
  # Upload existing build without rebuilding
  python3 scripts/upload_to_pypi.py --skip-build

Before running:
1. Make sure you have updated the version in setup.py
2. Ensure you have twine installed: pip install twine
3. Have your PyPI API token ready
""")


if __name__ == "__main__":
    if '--help' in sys.argv:
        show_help()
    else:
        success = main()
        sys.exit(0 if success else 1)
