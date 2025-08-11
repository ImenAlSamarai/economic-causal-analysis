#!/usr/bin/env python3
"""Quick test to validate the causal mechanisms implementation."""

import sys
import os
sys.path.append('/Users/imenalsamarai/Documents/projects_MCP/economic_causal_analysis')

try:
    from src.architecture import (
        CausalMechanism,
        MechanismType,
        EnhancedCausalRelationship,
        CausalRelationship,
        create_interest_rate_mechanism,
        create_okun_law_mechanism,
        create_oil_shock_mechanism,
        create_investment_returns_mechanism
    )
    print("✅ Imports successful")
    
    # Test basic linear mechanism
    linear_mech = CausalMechanism(MechanismType.LINEAR)
    result = linear_mech.apply_mechanism(2.0, 0.5)
    print(f"✅ Linear mechanism test: 2.0 * 0.5 = {result}")
    assert result == 1.0, f"Expected 1.0, got {result}"
    
    # Test exponential mechanism
    exp_mech = CausalMechanism(MechanismType.EXPONENTIAL, {"exponent": 2.0})
    result = exp_mech.apply_mechanism(3.0, 0.5)
    expected = 0.5 * (3.0 ** 2.0)  # 0.5 * 9 = 4.5
    print(f"✅ Exponential mechanism test: 3.0^2 * 0.5 = {result}")
    assert abs(result - expected) < 1e-10, f"Expected {expected}, got {result}"
    
    # Test threshold mechanism
    threshold_mech = CausalMechanism(
        MechanismType.THRESHOLD,
        {"threshold": 1.0, "scale_factor": 2.0}
    )
    result_below = threshold_mech.apply_mechanism(0.5, 0.5)  # Below threshold
    result_above = threshold_mech.apply_mechanism(2.0, 0.5)  # Above threshold
    print(f"✅ Threshold mechanism test: below={result_below}, above={result_above}")
    assert result_below == 0.0, f"Expected 0.0 below threshold, got {result_below}"
    expected_above = 0.5 * 2.0 * (2.0 - 1.0)  # 1.0
    assert abs(result_above - expected_above) < 1e-10, f"Expected {expected_above}, got {result_above}"
    
    # Test saturation mechanism
    sat_mech = CausalMechanism(
        MechanismType.SATURATION,
        {"max_effect": 1.0, "half_saturation": 5.0}
    )
    result = sat_mech.apply_mechanism(5.0, 0.5)  # At half saturation
    expected = 0.5 * 0.5  # Should be 50% of max effect
    print(f"✅ Saturation mechanism test at half-saturation: {result}")
    assert abs(result - expected) < 1e-10, f"Expected {expected}, got {result}"
    
    # Test integration with existing system
    base_rel = CausalRelationship("x", "y", 0.6, 0.8)
    enhanced = EnhancedCausalRelationship(base_rel, linear_mech)
    enhanced_result = enhanced.apply_causal_effect(3.0)
    expected_enhanced = 0.6 * 3.0  # 1.8
    print(f"✅ Enhanced relationship test: {enhanced_result}")
    assert abs(enhanced_result - expected_enhanced) < 1e-10, f"Expected {expected_enhanced}, got {enhanced_result}"
    
    # Test economic example functions
    interest_mech = create_interest_rate_mechanism()
    print(f"✅ Interest rate mechanism created: {interest_mech.mechanism_type}")
    assert interest_mech.mechanism_type == MechanismType.THRESHOLD
    
    okun_mech = create_okun_law_mechanism()
    print(f"✅ Okun's law mechanism created: {okun_mech.mechanism_type}")
    assert okun_mech.mechanism_type == MechanismType.SATURATION
    
    oil_mech = create_oil_shock_mechanism()
    print(f"✅ Oil shock mechanism created: {oil_mech.mechanism_type}")
    assert oil_mech.mechanism_type == MechanismType.EXPONENTIAL
    
    investment_mech = create_investment_returns_mechanism()
    print(f"✅ Investment returns mechanism created: {investment_mech.mechanism_type}")
    assert investment_mech.mechanism_type == MechanismType.SATURATION
    
    # Test different behaviors between mechanisms
    test_input = 2.0
    base_strength = 0.5
    
    linear_result = linear_mech.apply_mechanism(test_input, base_strength)
    exp_result = exp_mech.apply_mechanism(test_input, base_strength)
    threshold_result = threshold_mech.apply_mechanism(test_input, base_strength)
    sat_result = sat_mech.apply_mechanism(test_input, base_strength)
    
    print(f"\n📊 Different mechanism behaviors for input={test_input}, strength={base_strength}:")
    print(f"   Linear:     {linear_result:.4f}")
    print(f"   Exponential: {exp_result:.4f}")
    print(f"   Threshold:   {threshold_result:.4f}")
    print(f"   Saturation:  {sat_result:.4f}")
    
    # Verify they produce different outputs
    results = [linear_result, exp_result, threshold_result, sat_result]
    unique_results = len(set(f"{r:.6f}" for r in results))
    print(f"✅ Mechanism uniqueness test: {unique_results}/4 unique behaviors")
    assert unique_results >= 3, "Mechanisms should produce different behaviors"
    
    print("\n🎉 All comprehensive tests passed!")
    print("✅ Task 1.2: Basic Causal Mechanisms - IMPLEMENTATION COMPLETE")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
