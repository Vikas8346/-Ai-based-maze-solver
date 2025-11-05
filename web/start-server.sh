#!/bin/bash

# Simple HTTP server for the maze solver web app

PORT=8000

echo "🚀 Starting AI Maze Solver Web Server..."
echo "📍 Server running at: http://localhost:$PORT"
echo "🌐 Opening in browser..."
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd /workspaces/-Ai-based-maze-solver/web

# Start Python HTTP server
python3 -m http.server $PORT
