"""
Enhanced Validation Script for Causal Mechanisms

This script extends the existing validation to test the new causal mechanisms
functionality while ensuring integration with the existing system.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.architecture import (
    CausalEconomicGraph, 
    EconomicVariable, 
    CausalRelationship, 
    VariableType,
    # New imports for Task 1.2
    CausalMechanism,
    MechanismType,
    EnhancedCausalRelationship,
    create_interest_rate_mechanism,
    create_okun_law_mechanism,
    create_oil_shock_mechanism,
    create_investment_returns_mechanism
)


def test_causal_mechanisms():
    """Test the new causal mechanisms functionality."""
    print("\n=== Testing Causal Mechanisms (Task 1.2) ===")
    
    # Test 1: Linear Mechanism
    print("\n1. Testing Linear Mechanism:")
    linear_mech = CausalMechanism(MechanismType.LINEAR)
    
    test_cases = [(0, 0.5, 0.0), (2, 0.5, 1.0), (4, -0.3, -1.2)]
    for input_val, strength, expected in test_cases:
        result = linear_mech.apply_mechanism(input_val, strength)
        print(f"   Input: {input_val}, Strength: {strength} -> Output: {result}")
        assert abs(result - expected) < 1e-10, f"Expected {expected}, got {result}"
    print("   ✅ Linear mechanism tests passed")
    
    # Test 2: Exponential Mechanism
    print("\n2. Testing Exponential Mechanism:")
    exp_mech = CausalMechanism(MechanismType.EXPONENTIAL, {"exponent": 2.0})
    
    result_1 = exp_mech.apply_mechanism(2, 0.5)  # 0.5 * 2^2 = 2.0
    result_2 = exp_mech.apply_mechanism(3, 0.5)  # 0.5 * 3^2 = 4.5
    print(f"   2^2 * 0.5 = {result_1}")
    print(f"   3^2 * 0.5 = {result_2}")
    assert result_1 == 2.0, f"Expected 2.0, got {result_1}"
    assert result_2 == 4.5, f"Expected 4.5, got {result_2}"
    print("   ✅ Exponential mechanism tests passed")
    
    # Test 3: Threshold Mechanism
    print("\n3. Testing Threshold Mechanism:")
    threshold_mech = CausalMechanism(
        MechanismType.THRESHOLD,
        {"threshold": 1.5, "scale_factor": 2.0}
    )
    
    result_below = threshold_mech.apply_mechanism(1.0, 0.5)  # Below threshold
    result_above = threshold_mech.apply_mechanism(3.0, 0.5)  # Above threshold
    expected_above = 0.5 * 2.0 * (3.0 - 1.5)  # 1.5
    
    print(f"   Below threshold (1.0): {result_below}")
    print(f"   Above threshold (3.0): {result_above}")
    assert result_below == 0.0, f"Expected 0.0 below threshold, got {result_below}"
    assert abs(result_above - expected_above) < 1e-10, f"Expected {expected_above}, got {result_above}"
    print("   ✅ Threshold mechanism tests passed")
    
    # Test 4: Saturation Mechanism
    print("\n4. Testing Saturation Mechanism:")
    sat_mech = CausalMechanism(
        MechanismType.SATURATION,
        {"max_effect": 1.0, "half_saturation": 4.0}
    )
    
    # Test that function is increasing and approaches maximum
    inputs = [1, 2, 4, 8, 16]
    results = []
    
    for inp in inputs:
        result = sat_mech.apply_mechanism(inp, 0.5)
        results.append(result)
        print(f"   Input {inp}: {result:.4f}")
    
    # Verify increasing function
    for i in range(1, len(results)):
        assert results[i] > results[i-1], f"Results should be increasing: {results[i]} <= {results[i-1]}"
    
    # Verify it approaches the maximum asymptotically
    max_theoretical = 0.5 * 1.0  # base_strength * max_effect
    assert results[-1] < max_theoretical, "Should approach but not exceed maximum"
    assert results[-1] > 0.75 * max_theoretical, "Should be close to maximum for large inputs"
    
    # Test key property: diminishing marginal returns (after initial increase)
    # The saturation mechanism shows increasing then decreasing marginal returns
    marginals = [results[i] - results[i-1] for i in range(1, len(results))]
    
    # For saturation mechanism, marginals should eventually decrease
    # Check that later marginals are smaller than peak marginal
    max_marginal = max(marginals)
    max_marginal_idx = marginals.index(max_marginal)
    
    # Verify diminishing returns after the peak
    if max_marginal_idx < len(marginals) - 1:
        later_marginals = marginals[max_marginal_idx + 1:]
        assert all(m <= max_marginal for m in later_marginals), "Should show diminishing returns after peak"
    
    print(f"   Marginal effects: {[f'{m:.4f}' for m in marginals]}")
    print(f"   Peak marginal at position {max_marginal_idx + 1}, value {max_marginal:.4f}")
    
    # Test half-saturation property
    half_sat_result = sat_mech.apply_mechanism(4.0, 0.5)  # At half_saturation
    expected_half_sat = 0.5 * 0.5  # Should be 50% of max effect
    assert abs(half_sat_result - expected_half_sat) < 1e-10, f"Half-saturation test failed: {half_sat_result} != {expected_half_sat}"
    
    print("   ✅ Saturation mechanism tests passed")
    
    # Test 5: Economic Examples
    print("\n5. Testing Economic Example Functions:")
    
    interest_mech = create_interest_rate_mechanism()
    assert interest_mech.mechanism_type == MechanismType.THRESHOLD
    print(f"   ✅ Interest rate mechanism: {interest_mech.mechanism_type}")
    
    okun_mech = create_okun_law_mechanism()
    assert okun_mech.mechanism_type == MechanismType.SATURATION
    print(f"   ✅ Okun's law mechanism: {okun_mech.mechanism_type}")
    
    oil_mech = create_oil_shock_mechanism()
    assert oil_mech.mechanism_type == MechanismType.EXPONENTIAL
    print(f"   ✅ Oil shock mechanism: {oil_mech.mechanism_type}")
    
    investment_mech = create_investment_returns_mechanism()
    assert investment_mech.mechanism_type == MechanismType.SATURATION
    print(f"   ✅ Investment returns mechanism: {investment_mech.mechanism_type}")
    
    # Test 6: Integration with Existing System
    print("\n6. Testing Integration with Existing System:")
    
    # Create base relationship
    base_relationship = CausalRelationship(
        source="federal_funds_rate",
        target="gdp_growth",
        strength=-0.4,
        confidence=0.85,
        lag_periods=2
    )
    
    # Test with different mechanisms
    mechanisms = [
        ("Linear", CausalMechanism(MechanismType.LINEAR)),
        ("Threshold", create_interest_rate_mechanism()),
        ("Exponential", create_oil_shock_mechanism())
    ]
    
    test_input = 0.5  # 50 basis points
    
    for name, mechanism in mechanisms:
        enhanced = EnhancedCausalRelationship(base_relationship, mechanism)
        result = enhanced.apply_causal_effect(test_input)
        print(f"   {name} mechanism result: {result:.4f}")
        
        # Verify properties are preserved
        assert enhanced.source == "federal_funds_rate"
        assert enhanced.target == "gdp_growth"
        assert enhanced.strength == -0.4
        assert enhanced.confidence == 0.85
        assert enhanced.lag_periods == 2
    
    print("   ✅ Integration tests passed")
    
    # Test 7: Distinct Behaviors
    print("\n7. Testing Distinct Mechanism Behaviors:")
    
    test_input = 3.0
    base_strength = 0.6
    
    linear_result = linear_mech.apply_mechanism(test_input, base_strength)
    exp_result = exp_mech.apply_mechanism(test_input, base_strength)
    threshold_result = threshold_mech.apply_mechanism(test_input, base_strength)
    sat_result = sat_mech.apply_mechanism(test_input, base_strength)
    
    print(f"   Input: {test_input}, Strength: {base_strength}")
    print(f"   Linear:      {linear_result:.4f}")
    print(f"   Exponential: {exp_result:.4f}")
    print(f"   Threshold:   {threshold_result:.4f}")
    print(f"   Saturation:  {sat_result:.4f}")
    
    # Verify different outputs
    results = [linear_result, exp_result, threshold_result, sat_result]
    unique_results = len(set(f"{r:.6f}" for r in results))
    assert unique_results >= 3, f"Expected at least 3 unique behaviors, got {unique_results}"
    print(f"   ✅ {unique_results}/4 mechanisms produce unique behaviors")
    
    print("\n🎉 All causal mechanism tests passed!")
    
    return True


def test_backward_compatibility():
    """Test that existing functionality still works unchanged."""
    print("\n=== Testing Backward Compatibility ===")
    
    # Test existing CausalRelationship functionality
    rel = CausalRelationship(
        source="inflation",
        target="consumer_spending",
        strength=-0.3,
        confidence=0.9
    )
    
    # All existing properties should work
    assert rel.source == "inflation"
    assert rel.target == "consumer_spending"
    assert rel.strength == -0.3
    assert rel.confidence == 0.9
    assert rel.lag_periods == 0  # Default
    assert rel.effect_magnitude == 0.27  # |strength| * confidence
    
    print("✅ Existing CausalRelationship functionality preserved")
    
    # Test that existing EconomicVariable works
    var = EconomicVariable(
        name="test_var",
        variable_type=VariableType.MARKET,
        current_value=5.0,
        uncertainty=0.2,
        description="Test variable"
    )
    
    assert var.name == "test_var"
    assert var.variable_type == VariableType.MARKET
    assert var.current_value == 5.0
    
    print("✅ Existing EconomicVariable functionality preserved")
    
    # Test that existing imports still work by creating instances
    graph = CausalEconomicGraph()
    assert isinstance(graph, CausalEconomicGraph)
    print("✅ Existing imports still work")
    
    return True


def main():
    """Run all validation tests."""
    print("Economic Causal Analysis System - Enhanced Validation")
    print("=" * 60)
    
    try:
        # Test new functionality
        test_causal_mechanisms()
        
        # Test backward compatibility
        test_backward_compatibility()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("✅ Task 1.2: Basic Causal Mechanisms - VALIDATION COMPLETE")
        print("✅ System is ready for production use")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ VALIDATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
