#!/bin/bash

# Test Runner Script for Economic Causal Analysis System
# Run this from the project root directory

echo "=== Economic Causal Analysis System Test Runner ==="
echo ""

# Check if we're in the right directory
if [ ! -f "validate_system.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "   Expected: economic_causal_analysis/"
    exit 1
fi

echo "📍 Current directory: $(pwd)"
echo ""

# Check Python installation
echo "🐍 Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.7+"
    exit 1
fi
echo "✅ Python 3 found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✅ Dependencies installed"
echo ""

# Run the validation script
echo "🧪 Running validation tests..."
echo "=============================================="
python3 validate_system.py

# Check the exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "=============================================="
    echo "🎉 ALL TESTS PASSED! System is working correctly."
else
    echo ""
    echo "=============================================="
    echo "❌ Some tests failed. Check the output above."
    exit 1
fi
