#!/usr/bin/env python3
"""
Quick test to verify the bug fix for the Economic Demo
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from demo_basic import EconomicDemo
    
    print("🧪 Testing the Economic Demo fix...")
    
    # Create demo instance
    demo = EconomicDemo()
    
    # Create the economic model
    demo.create_economic_model()
    
    # Test scenario A with debugging
    print("\n⚡ Testing Scenario A: Fed Rate Hike")
    print("=" * 50)
    
    scenario_a_data = demo.run_scenario_a()
    
    # Check if we have meaningful changes
    initial = scenario_a_data["initial_state"]
    final = scenario_a_data["final_state"]
    
    print("\n📊 RESULTS ANALYSIS:")
    
    meaningful_changes = False
    for var_name in ["fed_funds_rate", "sp500_price", "gdp_growth", "unemployment_rate", "inflation_rate"]:
        initial_val = initial[var_name]
        final_val = final[var_name]
        change = final_val - initial_val
        pct_change = (change / initial_val * 100) if initial_val != 0 else 0
        
        print(f"  {var_name}: {initial_val:.2f} -> {final_val:.2f} (Δ: {change:+.3f}, {pct_change:+.2f}%)")
        
        # Check if we have meaningful economic changes (more than 0.001%)
        if abs(pct_change) > 0.001:
            meaningful_changes = True
    
    print(f"\n✅ Fix Status: {'SUCCESS - Meaningful economic impacts detected!' if meaningful_changes else 'FAILED - Still showing zero impacts'}")
    
    # Test a simple shock directly for validation
    print(f"\n🔍 DEBUG INFO:")
    print(f"  Results convergence: {scenario_a_data['results'].convergence_achieved}")
    print(f"  Time series length: {len(scenario_a_data['results'].time_series.get('fed_funds_rate', []))}")
    print(f"  Scenario execution time: {scenario_a_data['scenario_time']:.4f} seconds")
    
    if meaningful_changes:
        print("\n🎉 BUG FIX SUCCESSFUL! The demo now shows realistic economic impacts.")
    else:
        print("\n❌ BUG STILL EXISTS - Need further investigation.")
        
        # Additional debugging
        print("\nDEBUG - First few time series values:")
        for var in ["fed_funds_rate", "sp500_price"]:
            series = scenario_a_data['results'].time_series.get(var, [])
            if len(series) > 3:
                print(f"  {var}: [{series[0]:.3f}, {series[1]:.3f}, {series[2]:.3f}, ...]")
    
except Exception as e:
    print(f"❌ ERROR during testing: {e}")
    import traceback
    traceback.print_exc()
