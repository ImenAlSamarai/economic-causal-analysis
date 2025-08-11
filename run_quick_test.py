#!/usr/bin/env python3
"""Run the quick test for causal mechanisms."""

import subprocess
import sys
import os

# Change to the project directory
project_dir = '/Users/imenalsamarai/Documents/projects_MCP/economic_causal_analysis'
os.chdir(project_dir)

try:
    # Run the test
    result = subprocess.run([
        sys.executable, 'test_quick_mechanisms.py'
    ], capture_output=True, text=True, timeout=30)
    
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("\nSTDERR:")
        print(result.stderr)
    
    print(f"\nReturn code: {result.returncode}")
    
    if result.returncode == 0:
        print("\n🎉 SUCCESS: All tests passed!")
    else:
        print("\n❌ FAILURE: Tests failed!")
        
except subprocess.TimeoutExpired:
    print("❌ Test timed out after 30 seconds")
except Exception as e:
    print(f"❌ Error running test: {e}")
