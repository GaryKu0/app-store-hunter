#!/usr/bin/env python3
"""
Version Bump Script for App Store Icon Hunter

This script helps bump the version number in setup.py before publishing.
"""

import re
import sys
import argparse
from pathlib import Path


def get_current_version():
    """Get the current version from setup.py."""
    setup_py = Path("setup.py")
    if not setup_py.exists():
        print("❌ setup.py not found!")
        return None
    
    content = setup_py.read_text()
    match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    
    print("❌ Could not find version in setup.py")
    return None


def bump_version(current_version, bump_type):
    """Bump version number based on type (major, minor, patch)."""
    try:
        major, minor, patch = map(int, current_version.split('.'))
    except ValueError:
        print(f"❌ Invalid version format: {current_version}")
        return None
    
    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'patch':
        patch += 1
    else:
        print(f"❌ Invalid bump type: {bump_type}")
        return None
    
    return f"{major}.{minor}.{patch}"


def update_version_in_setup(new_version):
    """Update version in setup.py."""
    setup_py = Path("setup.py")
    content = setup_py.read_text()
    
    # Replace version
    new_content = re.sub(
        r'(version\s*=\s*["\'])[^"\']+(["\'])',
        rf'\g<1>{new_version}\g<2>',
        content
    )
    
    if new_content == content:
        print("❌ Could not update version in setup.py")
        return False
    
    setup_py.write_text(new_content)
    return True


def main():
    parser = argparse.ArgumentParser(description='Bump version in setup.py')
    parser.add_argument('bump_type', choices=['major', 'minor', 'patch'], 
                       help='Type of version bump')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be changed without actually changing it')
    
    args = parser.parse_args()
    
    # Check if we're in the right directory
    if not Path("setup.py").exists():
        print("❌ setup.py not found. Please run from project root.")
        sys.exit(1)
    
    # Get current version
    current_version = get_current_version()
    if not current_version:
        sys.exit(1)
    
    # Calculate new version
    new_version = bump_version(current_version, args.bump_type)
    if not new_version:
        sys.exit(1)
    
    print(f"📦 Current version: {current_version}")
    print(f"📦 New version: {new_version}")
    
    if args.dry_run:
        print("🔍 Dry run - no changes made")
        return
    
    # Confirm the change
    response = input(f"\n❓ Update version to {new_version}? (y/N): ")
    if response.lower() != 'y':
        print("❌ Version update cancelled")
        sys.exit(0)
    
    # Update version
    if update_version_in_setup(new_version):
        print(f"✅ Version updated to {new_version}")
        print("\n📝 Next steps:")
        print("1. Commit the version change")
        print("2. Create a git tag: git tag v" + new_version)
        print("3. Run the upload script: ./scripts/upload_to_pypi.sh")
    else:
        print("❌ Failed to update version")
        sys.exit(1)


if __name__ == "__main__":
    main()
