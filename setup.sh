#!/bin/bash
# Setup script for AI-Based Maze Solver

echo "=========================================="
echo "  AI-Based Maze Solver - Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check if Python 3.8+
required_version="3.8"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then 
    echo "✓ Python version is compatible"
else
    echo "✗ Python 3.8+ required. Please upgrade Python."
    exit 1
fi

echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -eq 0 ]; then
    echo "✓ Virtual environment created"
else
    echo "✗ Failed to create virtual environment"
    exit 1
fi

echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip -q

echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

echo ""

# Create results directory
echo "Creating results directory..."
mkdir -p results
echo "✓ Results directory created"

echo ""

# Run quick test
echo "Running quick test..."
python -c "from src.maze import Maze; from src.algorithms import PathfindingAlgorithms; print('✓ Import test passed')"

if [ $? -eq 0 ]; then
    echo "✓ All systems ready!"
else
    echo "✗ Import test failed"
    exit 1
fi

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "To get started:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the application:"
echo "     python main.py              # GUI mode"
echo "     python main.py --console    # Console mode"
echo "     python demo.py              # Quick demo"
echo ""
echo "For more information, see README.md"
echo ""
