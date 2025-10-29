#!/bin/bash

echo "🚀 Starting MCP Robot Driver API Server"
echo "======================================="

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: Please run this script from the 'api' directory"
    echo "💡 Usage: cd api && ./start_server.sh"
    exit 1
fi

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
python -c "import fastapi, uvicorn, playwright" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies..."
    pip install -r ../requirements.txt
    playwright install chromium
fi

echo "✅ Dependencies ready!"

# Start the server
echo "🌐 Starting FastAPI server..."
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🧪 Test endpoints: http://localhost:8000/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000