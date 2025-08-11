#!/usr/bin/env python3
"""
Final test of the fully enhanced demo
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("🚀 Testing the FULLY ENHANCED demo...")
    
    # Import and run the demo
    from demo_basic import EconomicDemo
    
    demo = EconomicDemo()
    demo.create_economic_model()
    
    print("\n⚡ Running Scenario A with all enhancements...")
    scenario_data = demo.run_scenario_a()
    
    # Analyze results
    initial = scenario_data["initial_state"]
    final = scenario_data["final_state"]
    results = scenario_data["results"]
    
    print(f"\n📊 FINAL ENHANCED RESULTS:")
    print(f"Enhanced relationships: {results.metadata.get('enhanced_relationships', 0)}")
    print(f"Convergence: {results.convergence_achieved}")
    
    # Check each variable for meaningful changes
    meaningful_changes = False
    major_changes = False
    
    for var_name in ["fed_funds_rate", "sp500_price", "gdp_growth", "unemployment_rate", "inflation_rate"]:
        initial_val = initial[var_name]
        final_val = final[var_name]
        change = final_val - initial_val
        pct_change = (change / initial_val * 100) if initial_val != 0 else 0
        
        if abs(pct_change) > 0.01:  # More than 0.01% change
            meaningful_changes = True
        if abs(pct_change) > 0.1:   # More than 0.1% change  
            major_changes = True
            
        print(f"  {var_name:20}: {initial_val:8.2f} → {final_val:8.2f} (Δ{change:+8.3f}, {pct_change:+6.2f}%)")
    
    # Final assessment
    if major_changes:
        print(f"\n🎉 SUCCESS: Enhanced demo shows major economic impacts!")
        print(f"✅ The enhanced relationships successfully fixed the propagation bug.")
    elif meaningful_changes:
        print(f"\n🟡 PARTIAL SUCCESS: Some changes detected but may be too small.")
        print(f"⚠️  May need further parameter tuning.")
    else:
        print(f"\n❌ FAILURE: Still no meaningful changes detected.")
        print(f"🔍 The issue is deeper in the architecture.")
        
        # Additional debug info
        print(f"\nDEBUG INFO:")
        print(f"  Scenario time: {scenario_data['scenario_time']:.6f}s")
        print(f"  Results metadata: {results.metadata}")
        
        # Show some time series data
        fed_series = results.time_series.get('fed_funds_rate', [])
        if len(fed_series) > 3:
            print(f"  Fed rate series: {fed_series[:4]} ...")
            print(f"  Period 0→1 change: {fed_series[1] - fed_series[0]:+.8f}")
    
except Exception as e:
    print(f"💥 Error during testing: {e}")
    import traceback
    traceback.print_exc()
