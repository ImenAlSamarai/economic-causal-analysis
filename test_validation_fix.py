#!/usr/bin/env python3
"""Quick test to verify the fixed validation script works."""

import subprocess
import sys
import os

def run_validation():
    """Run the validation script and return results."""
    os.chdir('/Users/imenalsamarai/Documents/projects_MCP/economic_causal_analysis')
    
    try:
        result = subprocess.run([
            sys.executable, 'validate_mechanisms.py'
        ], capture_output=True, text=True, timeout=60)
        
        return {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
    except subprocess.TimeoutExpired:
        return {'error': 'Timeout'}
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    print("Testing the fixed validation script...")
    result = run_validation()
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)
    
    print("=== VALIDATION OUTPUT ===")
    print(result['stdout'])
    
    if result['stderr']:
        print("\n=== STDERR ===")
        print(result['stderr'])
    
    print(f"\n=== EXIT CODE: {result['returncode']} ===")
    
    if result['returncode'] == 0:
        print("\n🎉 SUCCESS: All validation tests passed!")
        print("✅ Task 1.2 implementation is working correctly!")
    else:
        print("\n❌ FAILURE: Validation tests failed!")
        sys.exit(1)
