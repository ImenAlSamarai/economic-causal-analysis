#!/usr/bin/env python3
"""
Quick test of the enhanced demo
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from demo_basic import EconomicDemo
    
    print("🧪 Testing the ENHANCED Economic Demo...")
    
    # Create demo instance
    demo = EconomicDemo()
    
    # Create the economic model (now with enhanced relationships)
    demo.create_economic_model()
    
    # Test scenario A with debugging
    print("\n⚡ Testing Enhanced Scenario A: Fed Rate Hike")
    print("=" * 50)
    
    scenario_a_data = demo.run_scenario_a()
    
    # Check if we have meaningful changes
    initial = scenario_a_data["initial_state"]
    final = scenario_a_data["final_state"]
    
    print("\n📊 ENHANCED RESULTS ANALYSIS:")
    
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
    
    print(f"\n✅ Enhanced Fix Status: {'SUCCESS - Enhanced mechanisms working!' if meaningful_changes else 'STILL FAILING - Need deeper investigation'}")
    
    if meaningful_changes:
        print("\n🎉 ENHANCED BUG FIX SUCCESSFUL! The enhanced mechanisms resolved the issue.")
    else:
        print("\n❌ ENHANCED FIX FAILED - The issue is deeper in the architecture.")
        
        # Additional debugging
        print("\nDEBUG - Enhanced mechanisms didn't help:")
        results = scenario_a_data['results']
        print(f"  Enhanced relationships count: {results.metadata.get('enhanced_relationships', 0)}")
        print(f"  Total relationships: {results.metadata.get('total_relationships', 0)}")
        
        # Show first few time series values
        for var in ["fed_funds_rate", "sp500_price"]:
            series = results.time_series.get(var, [])
            if len(series) > 3:
                print(f"  {var}: [{series[0]:.3f}, {series[1]:.3f}, {series[2]:.3f}, ...]")
                if len(series) > 1:
                    change = series[1] - series[0]
                    print(f"    First period change: {change:+.6f}")
    
except Exception as e:
    print(f"❌ ERROR during enhanced testing: {e}")
    import traceback
    traceback.print_exc()
