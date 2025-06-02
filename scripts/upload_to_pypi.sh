#!/bin/bash

# App Store Icon Hunter - PyPI Upload Script (Bash version)
# Simple script to build and upload package to PyPI

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_step() {
    echo -e "${BLUE}🔄 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    print_error "setup.py not found. Please run this script from the project root."
    exit 1
fi

# Parse arguments
TEST_UPLOAD=false
SKIP_BUILD=false

for arg in "$@"; do
    case $arg in
        --test)
            TEST_UPLOAD=true
            shift
            ;;
        --skip-build)
            SKIP_BUILD=true
            shift
            ;;
        --help)
            echo "App Store Icon Hunter - PyPI Upload Script"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --test        Upload to TestPyPI instead of PyPI"
            echo "  --skip-build  Skip the build process and upload existing dist/ files"
            echo "  --help        Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                 # Normal upload to PyPI"
            echo "  $0 --test         # Test upload to TestPyPI"
            echo "  $0 --skip-build   # Upload existing build"
            exit 0
            ;;
        *)
            print_error "Unknown argument: $arg"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo "🎯 App Store Icon Hunter - PyPI Upload Script"
echo "================================================="

if [ "$TEST_UPLOAD" = true ]; then
    print_warning "Test mode: Will upload to TestPyPI"
fi

# Step 1: Clean build artifacts (if not skipping build)
if [ "$SKIP_BUILD" = false ]; then
    print_step "Cleaning build artifacts..."
    rm -rf dist/ build/ *.egg-info/ __pycache__/
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    
    # Step 2: Backup LICENSE temporarily
    LICENSE_BACKED_UP=false
    if [ -f "LICENSE" ]; then
        mv LICENSE LICENSE.backup
        LICENSE_BACKED_UP=true
        print_step "Temporarily backed up LICENSE file"
    fi
    
    # Step 3: Build package
    print_step "Building source distribution..."
    python3 setup.py sdist
    
    print_step "Building wheel..."
    pip3 wheel . --no-deps
    
    # Move wheel to dist directory
    mkdir -p dist
    mv *.whl dist/ 2>/dev/null || true
    
    # Step 4: Restore LICENSE
    if [ "$LICENSE_BACKED_UP" = true ]; then
        mv LICENSE.backup LICENSE
        print_step "Restored LICENSE file"
    fi
    
    print_success "Package built successfully"
fi

# Step 5: Check if dist files exist
if [ ! -d "dist" ] || [ -z "$(ls -A dist)" ]; then
    print_error "No distribution files found in dist/"
    exit 1
fi

echo ""
print_step "Distribution files ready:"
ls -la dist/

echo ""
print_step "Uploading to $([ "$TEST_UPLOAD" = true ] && echo "TestPyPI" || echo "PyPI")..."

# Step 6: Upload
if [ "$TEST_UPLOAD" = true ]; then
    python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
else
    python3 -m twine upload dist/*
fi

# Success message
if [ $? -eq 0 ]; then
    echo ""
    if [ "$TEST_UPLOAD" = true ]; then
        print_success "Successfully uploaded to TestPyPI!"
        echo ""
        echo "🔗 View your package at: https://test.pypi.org/project/app-store-icon-hunter/"
        echo "📦 Test install with: pip install --index-url https://test.pypi.org/simple/ app-store-icon-hunter"
    else
        print_success "Successfully uploaded to PyPI!"
        echo ""
        echo "🔗 View your package at: https://pypi.org/project/app-store-icon-hunter/"
        echo "📦 Install with: pip install app-store-icon-hunter"
    fi
else
    print_error "Upload failed!"
    exit 1
fi
