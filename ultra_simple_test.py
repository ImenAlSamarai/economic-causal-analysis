#!/usr/bin/env python3
"""
Ultra-simple test to see the actual time series values
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.architecture import *

def ultra_simple_test():
    """Run the simplest possible test."""
    print("🔬 ULTRA-SIMPLE SHOCK TEST")
    print("=" * 40)
    
    # Create ultra-minimal model
    graph = CausalEconomicGraph()
    
    # One variable only
    var = EconomicVariable(
        name="test_var",
        variable_type=VariableType.POLICY,
        current_value=10.0,
        uncertainty=1.0,
        description="Test variable",
        unit="units",
        bounds=(0.0, 100.0)
    )
    
    graph.add_variable(var)
    add_shock_propagation_capabilities(graph)
    
    print(f"📊 Initial value: {var.current_value}")
    
    # Create shock
    shock = ShockEvent(
        variable_name="test_var",
        magnitude=2.0,
        description="Test shock"
    )
    
    expected_shock_value = shock.magnitude * var.uncertainty
    expected_new_value = var.current_value + expected_shock_value
    
    print(f"⚡ Shock magnitude: {shock.magnitude}")
    print(f"⚡ Expected shock value: {expected_shock_value}")
    print(f"⚡ Expected new value: {expected_new_value}")
    
    # Run minimal propagation
    results = graph.propagate_shock(shock, num_periods=3, dampening_factor=1.0)
    
    print(f"\n📈 Results:")
    print(f"  Time series length: {len(results.time_series.get('test_var', []))}")
    
    series = results.time_series.get('test_var', [])
    for i, value in enumerate(series):
        change = value - series[0] if i > 0 else 0.0
        print(f"  Period {i}: {value:.6f} (change: {change:+.6f})")
    
    # Check final vs initial
    initial_value = results.time_series['test_var'][0]
    final_value = results.time_series['test_var'][-1]
    total_change = final_value - initial_value
    
    print(f"\n🎯 Summary:")
    print(f"  Initial: {initial_value:.6f}")
    print(f"  Final: {final_value:.6f}")
    print(f"  Total change: {total_change:+.6f}")
    print(f"  Expected change: ~{expected_shock_value:+.6f}")
    
    if abs(total_change) < 1e-6:
        print(f"  🚨 BUG: No change detected!")
        return False
    else:
        print(f"  ✅ Change detected!")
        return True

if __name__ == "__main__":
    try:
        success = ultra_simple_test()
        print(f"\n{'✅ PASS' if success else '❌ FAIL'}")
    except Exception as e:
        print(f"\n💥 Error: {e}")
        import traceback
        traceback.print_exc()
