#!/bin/bash
set -e

echo "Setting up local development environment..."

# Create data directories if they don't exist
echo "Creating data directories..."
mkdir -p data/db
mkdir -p data/uploads
mkdir -p data/outputs

# Copy .env.example to .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please review and update .env file with your settings."
else
    echo ".env file already exists, skipping..."
fi

# Check if podman is installed
if ! command -v podman &> /dev/null; then
    echo "Warning: podman is not installed. Please install podman to continue."
    exit 1
fi

# Check if podman-compose is installed
if ! command -v podman-compose &> /dev/null; then
    echo "Warning: podman-compose is not installed. Please install podman-compose to continue."
    echo "You can install it with: pip install podman-compose"
    exit 1
fi

# Check if podman machine is running (macOS only)
if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! podman machine list | grep -q "Currently running"; then
        echo "Podman machine is not running. Starting podman machine..."
        podman machine start
    fi
fi

echo ""
echo "Development environment setup complete!"
echo ""
echo "Next steps:"
echo "  1. Review and update the .env file if needed"
echo "  2. Run 'podman-compose build' to build the containers"
echo "  3. Run 'podman-compose up' to start the development environment"
echo "  4. Run 'podman-compose exec web python manage.py migrate' to apply database migrations"
echo "  5. Visit http://localhost:8000 in your browser"
echo ""
echo "For more information, see DEVELOPMENT.md"
