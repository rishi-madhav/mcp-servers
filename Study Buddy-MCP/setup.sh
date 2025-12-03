#!/bin/bash

echo "🚀 Setting up StudyBuddy MCP Server..."

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Create virtual environment
echo "🐍 Creating virtual environment..."
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
uv pip install -e .

# Create data directory
echo "📁 Creating data directory..."
mkdir -p data

# Copy .env.example to .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Edit .env and add your GEMINI_API_KEY"
fi

# Initialize database
echo "🗄️  Initializing database..."
python -c "
import asyncio
from mcp_server import database
asyncio.run(database.init_database())
print('✅ Database initialized')
"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GEMINI_API_KEY"
echo "2. Configure Claude Desktop (see README.md)"
echo "3. Run: python gradio_app/app.py"
echo ""
