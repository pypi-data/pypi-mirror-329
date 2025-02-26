#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Log function
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Check if maturin is installed
if ! command -v maturin &> /dev/null; then
    error "Maturin is not installed. Please install it using 'pip install maturin'."
fi

# Parse arguments
PUBLISH_FLAG=""
TARGET="--release"
SKIP_EXISTING="--skip-existing"
TOKEN_FILE="${HOME}/.pypi_token"
TOKEN_OPTION=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --test)
            PUBLISH_FLAG="--repository testpypi"
            TOKEN_FILE="${HOME}/.testpypi_token"
            shift
            ;;
        --production)
            PUBLISH_FLAG=""
            TOKEN_FILE="${HOME}/.pypi_token"
            shift
            ;;
        --debug)
            TARGET=""
            shift
            ;;
        --token=*)
            TOKEN_OPTION="${1#*=}"
            shift
            ;;
        --token-file=*)
            TOKEN_FILE="${1#*=}"
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --test                Publish to TestPyPI"
            echo "  --production          Publish to PyPI (default)"
            echo "  --debug               Build in debug mode"
            echo "  --token=YOUR_TOKEN    Use the provided PyPI token"
            echo "  --token-file=PATH     Path to file containing PyPI token (default: ~/.pypi_token or ~/.testpypi_token)"
            echo "  --help                Show this help message"
            exit 0
            ;;
        *)
            warning "Unknown option: $1"
            shift
            ;;
    esac
done

# Clean previous builds
log "Cleaning previous builds..."
rm -rf target/wheels dist

# Build the package
log "Building the package..."
maturin build $TARGET

# Get the token
if [ -z "$TOKEN_OPTION" ]; then
    if [ -f "$TOKEN_FILE" ]; then
        TOKEN_OPTION=$(cat "$TOKEN_FILE")
        log "Using token from $TOKEN_FILE"
    else
        warning "No token provided and token file not found at $TOKEN_FILE"
        warning "You will be prompted for your PyPI credentials"
    fi
fi

# Prepare token argument if token is available
if [ -n "$TOKEN_OPTION" ]; then
    TOKEN_ARG="--username __token__ --password $TOKEN_OPTION"
else
    TOKEN_ARG=""
fi

# Check if we should publish
if [ -z "$PUBLISH_FLAG" ]; then
    log "Built package successfully. Ready to publish to PyPI."
    read -p "Do you want to publish to PyPI? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "Publishing skipped."
        exit 0
    fi
    log "Publishing to PyPI..."
else
    log "Publishing to TestPyPI..."
fi

# Publish the package
if [ -n "$TOKEN_ARG" ]; then
    # Use token for authentication
    maturin publish $PUBLISH_FLAG $SKIP_EXISTING $TOKEN_ARG
else
    # Fall back to interactive authentication
    maturin publish $PUBLISH_FLAG $SKIP_EXISTING
fi

log "Package published successfully!"