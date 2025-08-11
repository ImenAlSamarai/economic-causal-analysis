#!/usr/bin/env python3
"""
Targeted debugging script to identify the exact issue in shock propagation
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.architecture import (
    CausalEconomicGraph, EconomicVariable, CausalRelationship, VariableType,
    ShockEvent, add_shock_propagation_capabilities
)

def debug_shock_propagation():
    """Debug the shock propagation step by step."""
    print("🔍 DEBUGGING SHOCK PROPAGATION")
    print("=" * 50)
    
    # Create a minimal economic model
    graph = CausalEconomicGraph()
    
    # Add just two variables for simplicity
    fed_rate = EconomicVariable(
        name="fed_funds_rate",
        variable_type=VariableType.POLICY,
        current_value=5.25,
        uncertainty=0.25,
        description="Federal Reserve federal funds rate",
        unit="percentage",
        bounds=(0.0, 12.0)
    )
    
    sp500 = EconomicVariable(
        name="sp500_price",
        variable_type=VariableType.MARKET,
        current_value=4500.0,
        uncertainty=150.0,
        description="S&P 500 stock market index",
        unit="index_points",
        bounds=(1000.0, 8000.0)
    )
    
    graph.add_variable(fed_rate)
    graph.add_variable(sp500)
    
    # Add one relationship: Fed rate affects stock prices
    relationship = CausalRelationship(
        source="fed_funds_rate",
        target="sp500_price",
        strength=-0.9,  # Strong negative relationship
        confidence=0.80,
        lag_periods=0,  # Immediate effect
        relationship_type="linear"
    )
    
    graph.add_relationship(relationship)
    
    print("📊 Model created:")
    print(f"  Fed Rate: {fed_rate.current_value} (uncertainty: {fed_rate.uncertainty})")
    print(f"  S&P 500: {sp500.current_value} (uncertainty: {sp500.uncertainty})")
    print(f"  Relationship: fed_rate -> sp500 (strength: {relationship.strength})")
    
    # Add shock propagation capabilities
    add_shock_propagation_capabilities(graph)
    
    # Create a shock event
    shock = ShockEvent(
        variable_name="fed_funds_rate",
        magnitude=2.0,  # 2 standard deviations
        description="Fed raises rates by 50bp"
    )
    
    # Calculate expected shock value
    shock_value = shock.magnitude * fed_rate.uncertainty
    expected_new_fed_rate = fed_rate.current_value + shock_value
    
    print(f"\n⚡ SHOCK APPLICATION:")
    print(f"  Shock magnitude: {shock.magnitude} std devs")
    print(f"  Shock value: {shock.magnitude} × {fed_rate.uncertainty} = {shock_value}")
    print(f"  Expected new fed rate: {fed_rate.current_value} + {shock_value} = {expected_new_fed_rate}")
    
    # Run propagation with just 3 periods for debugging
    print(f"\n🔄 RUNNING PROPAGATION...")
    results = graph.propagate_shock(
        shock=shock,
        num_periods=3,
        dampening_factor=0.95
    )
    
    print(f"\n📈 RESULTS ANALYSIS:")
    print(f"  Convergence: {results.convergence_achieved}")
    print(f"  Time series length: {len(results.time_series.get('fed_funds_rate', []))}")
    
    # Print detailed time series
    print(f"\n📊 DETAILED TIME SERIES:")
    fed_series = results.time_series.get('fed_funds_rate', [])
    sp500_series = results.time_series.get('sp500_price', [])
    
    print(f"  Period | Fed Rate | S&P 500 | Fed Change | S&P Change")
    print(f"  -------|----------|---------|------------|------------")
    
    for i in range(len(fed_series)):
        fed_val = fed_series[i]
        sp500_val = sp500_series[i] if i < len(sp500_series) else 0
        
        fed_change = fed_val - fed_series[0] if i > 0 else 0
        sp500_change = sp500_val - sp500_series[0] if i > 0 and sp500_series else 0
        
        print(f"  {i:6d} | {fed_val:8.3f} | {sp500_val:7.1f} | {fed_change:+10.3f} | {sp500_change:+10.1f}")
    
    # Check if we have meaningful changes
    if len(fed_series) > 1:
        final_fed_change = fed_series[-1] - fed_series[0]
        final_sp500_change = sp500_series[-1] - sp500_series[0] if len(sp500_series) > 1 else 0
        
        print(f"\n✅ FINAL ANALYSIS:")
        print(f"  Fed rate change: {final_fed_change:+.3f} (expected: ~{shock_value:+.3f})")
        print(f"  S&P 500 change: {final_sp500_change:+.1f}")
        
        if abs(final_fed_change) < 0.001:
            print(f"  🚨 BUG CONFIRMED: Fed rate shows no change despite shock!")
            return False
        else:
            print(f"  ✅ Fed rate change detected, investigating S&P 500...")
            if abs(final_sp500_change) < 1.0:
                print(f"  🚨 BUG: S&P 500 shows no meaningful change!")
                return False
            else:
                print(f"  ✅ Both variables show changes - system working!")
                return True
    else:
        print(f"  🚨 ERROR: No time series data generated!")
        return False

if __name__ == "__main__":
    try:
        success = debug_shock_propagation()
        if success:
            print(f"\n🎉 System appears to be working correctly!")
        else:
            print(f"\n❌ Bug confirmed - system not propagating shocks properly")
    except Exception as e:
        print(f"\n💥 Error during debugging: {e}")
        import traceback
        traceback.print_exc()
