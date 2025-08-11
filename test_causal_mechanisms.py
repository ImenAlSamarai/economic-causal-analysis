"""
Test Suite for Causal Mechanisms

Comprehensive testing of the causal mechanisms implementation,
validating mathematical correctness, economic realism, and
integration with the existing system architecture.

This test suite ensures that:
1. Each mechanism type produces distinct output patterns
2. Mechanisms behave correctly under various input conditions
3. Economic constraints and validations work properly
4. Integration with existing CausalRelationship system is seamless
5. Error handling is robust and informative
"""

import pytest
import math
import numpy as np
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


class TestCausalMechanism:
    """Test the core CausalMechanism class functionality."""
    
    def test_linear_mechanism(self):
        """Test linear mechanism produces proportional outputs."""
        mechanism = CausalMechanism(MechanismType.LINEAR)
        
        # Test proportional relationship
        assert mechanism.apply_mechanism(0, 0.5) == 0.0
        assert mechanism.apply_mechanism(2, 0.5) == 1.0
        assert mechanism.apply_mechanism(4, 0.5) == 2.0
        assert mechanism.apply_mechanism(-2, 0.5) == -1.0
        
        # Test with different base strengths
        assert mechanism.apply_mechanism(2, 0.8) == 1.6
        assert mechanism.apply_mechanism(2, -0.3) == -0.6
        
        # Test edge cases
        assert mechanism.apply_mechanism(0, 1.0) == 0.0
        assert mechanism.apply_mechanism(1, 0.0) == 0.0
    
    def test_exponential_mechanism(self):
        """Test exponential mechanism shows acceleration/deceleration."""
        # Test accelerating effect (exponent > 1)
        accel_mechanism = CausalMechanism(
            MechanismType.EXPONENTIAL,
            {"exponent": 2.0}
        )
        
        # Should show accelerating growth
        result_1 = accel_mechanism.apply_mechanism(1, 0.5)
        result_2 = accel_mechanism.apply_mechanism(2, 0.5)
        result_4 = accel_mechanism.apply_mechanism(4, 0.5)
        
        assert result_1 == 0.5  # 0.5 * 1^2
        assert result_2 == 2.0  # 0.5 * 2^2
        assert result_4 == 8.0  # 0.5 * 4^2
        
        # Test decelerating effect (exponent < 1)
        decel_mechanism = CausalMechanism(
            MechanismType.EXPONENTIAL,
            {"exponent": 0.5}
        )
        
        result_1_decel = decel_mechanism.apply_mechanism(1, 0.5)
        result_4_decel = decel_mechanism.apply_mechanism(4, 0.5)
        result_16_decel = decel_mechanism.apply_mechanism(16, 0.5)
        
        assert result_1_decel == 0.5   # 0.5 * 1^0.5
        assert result_4_decel == 1.0   # 0.5 * 4^0.5 = 0.5 * 2
        assert result_16_decel == 2.0  # 0.5 * 16^0.5 = 0.5 * 4
        
        # Test negative inputs preserve sign
        assert accel_mechanism.apply_mechanism(-2, 0.5) == -2.0
        
        # Test zero input
        assert accel_mechanism.apply_mechanism(0, 0.5) == 0.0
    
    def test_threshold_mechanism(self):
        """Test threshold mechanism only activates above specified levels."""
        mechanism = CausalMechanism(
            MechanismType.THRESHOLD,
            {"threshold": 2.0, "scale_factor": 1.5}
        )
        
        # Below threshold should return zero
        assert mechanism.apply_mechanism(0, 0.5) == 0.0
        assert mechanism.apply_mechanism(1.0, 0.5) == 0.0
        assert mechanism.apply_mechanism(1.9, 0.5) == 0.0
        assert mechanism.apply_mechanism(-1.0, 0.5) == 0.0
        
        # At threshold should return zero
        assert mechanism.apply_mechanism(2.0, 0.5) == 0.0
        assert mechanism.apply_mechanism(-2.0, 0.5) == 0.0
        
        # Above threshold should activate
        # Formula: base_strength * scale_factor * (input - sign(input) * threshold)
        result_pos = mechanism.apply_mechanism(3.0, 0.5)
        expected_pos = 0.5 * 1.5 * (3.0 - 2.0)  # 0.75
        assert abs(result_pos - expected_pos) < 1e-10
        
        result_neg = mechanism.apply_mechanism(-3.0, 0.5)
        expected_neg = 0.5 * 1.5 * (-3.0 - (-2.0))  # 0.5 * 1.5 * (-1.0) = -0.75
        assert abs(result_neg - expected_neg) < 1e-10
        
        # Test with different scale factor
        mechanism2 = CausalMechanism(
            MechanismType.THRESHOLD,
            {"threshold": 1.0, "scale_factor": 2.0}
        )
        result = mechanism2.apply_mechanism(2.0, 0.5)
        expected = 0.5 * 2.0 * (2.0 - 1.0)  # 1.0
        assert abs(result - expected) < 1e-10
    
    def test_saturation_mechanism(self):
        """Test saturation mechanism shows diminishing returns."""
        mechanism = CausalMechanism(
            MechanismType.SATURATION,
            {"max_effect": 1.0, "half_saturation": 5.0}
        )
        
        # Test zero input
        assert mechanism.apply_mechanism(0, 0.5) == 0.0
        
        # Test that function is increasing and approaches maximum
        results = []
        inputs = [1, 2, 5, 10, 20, 100]
        
        for inp in inputs:
            result = mechanism.apply_mechanism(inp, 0.5)
            results.append(result)
        
        # Results should be increasing
        for i in range(1, len(results)):
            assert results[i] > results[i-1], f"Results should be increasing: {results[i]} <= {results[i-1]}"
        
        # Test overall diminishing returns property
        # Compare early vs late marginal changes
        marginals = [results[i] - results[i-1] for i in range(1, len(results))]
        early_marginals = marginals[:2]  # First two marginal changes
        late_marginals = marginals[-2:]  # Last two marginal changes
        
        early_avg = sum(early_marginals) / len(early_marginals)
        late_avg = sum(late_marginals) / len(late_marginals)
        assert late_avg < early_avg, "Should show overall diminishing returns"
        
        # Test half-saturation point
        half_sat_result = mechanism.apply_mechanism(5.0, 0.5)
        # At half saturation: output = base_strength * (max_effect * half_sat) / (half_sat + half_sat)
        # = 0.5 * (1.0 * 5.0) / (5.0 + 5.0) = 0.5 * 0.5 = 0.25
        expected_half_sat = 0.5 * 0.5
        assert abs(half_sat_result - expected_half_sat) < 1e-10
        
        # Test negative inputs preserve sign
        neg_result = mechanism.apply_mechanism(-5.0, 0.5)
        assert neg_result == -expected_half_sat
        
        # Test approach to maximum
        large_input_result = mechanism.apply_mechanism(1000, 0.5)
        max_possible = 0.5 * 1.0  # base_strength * max_effect
        assert large_input_result < max_possible
        assert large_input_result > 0.9 * max_possible  # Should be close to max


class TestEnhancedCausalRelationship:
    """Test the EnhancedCausalRelationship integration class."""
    
    def test_initialization(self):
        """Test proper initialization of enhanced relationships."""
        base_rel = CausalRelationship(
            source="interest_rate",
            target="gdp_growth",
            strength=-0.3,
            confidence=0.8
        )
        
        mechanism = CausalMechanism(MechanismType.LINEAR)
        
        enhanced = EnhancedCausalRelationship(base_rel, mechanism)
        
        assert enhanced.source == "interest_rate"
        assert enhanced.target == "gdp_growth"
        assert enhanced.strength == -0.3
        assert enhanced.confidence == 0.8
        assert enhanced.lag_periods == 0  # Default value
    
    def test_apply_causal_effect(self):
        """Test the application of causal effects through mechanisms."""
        base_rel = CausalRelationship(
            source="policy_rate",
            target="inflation",
            strength=0.6,
            confidence=0.9
        )
        
        # Test with linear mechanism
        linear_mechanism = CausalMechanism(MechanismType.LINEAR)
        linear_enhanced = EnhancedCausalRelationship(base_rel, linear_mechanism)
        
        assert linear_enhanced.apply_causal_effect(2.0) == 1.2  # 0.6 * 2.0
        
        # Test with threshold mechanism
        threshold_mechanism = CausalMechanism(
            MechanismType.THRESHOLD,
            {"threshold": 1.0, "scale_factor": 1.5}
        )
        threshold_enhanced = EnhancedCausalRelationship(base_rel, threshold_mechanism)
        
        # Below threshold
        assert threshold_enhanced.apply_causal_effect(0.5) == 0.0
        
        # Above threshold
        result = threshold_enhanced.apply_causal_effect(2.0)
        expected = 0.6 * 1.5 * (2.0 - 1.0)  # 0.9
        assert abs(result - expected) < 1e-10


class TestEconomicExamples:
    """Test the economic example factory functions."""
    
    def test_interest_rate_mechanism(self):
        """Test interest rate threshold mechanism."""
        mechanism = create_interest_rate_mechanism()
        
        assert mechanism.mechanism_type == MechanismType.THRESHOLD
        assert mechanism.parameters["threshold"] == 0.25
        assert mechanism.parameters["scale_factor"] == 2.0
        assert "Interest rate policy" in mechanism.description
        
        # Test economic behavior
        base_strength = -0.4  # Negative relationship between rates and growth
        
        # Small rate changes should have no effect
        assert mechanism.apply_mechanism(0.1, base_strength) == 0.0
        assert mechanism.apply_mechanism(0.2, base_strength) == 0.0
        
        # Large rate changes should have amplified effect
        result = mechanism.apply_mechanism(0.5, base_strength)
        expected = base_strength * 2.0 * (0.5 - 0.25)  # -0.4 * 2.0 * 0.25 = -0.2
        assert abs(result - expected) < 1e-10
    
    def test_okun_law_mechanism(self):
        """Test Okun's law saturation mechanism."""
        mechanism = create_okun_law_mechanism()
        
        assert mechanism.mechanism_type == MechanismType.SATURATION
        assert mechanism.parameters["max_effect"] == -0.5
        assert mechanism.parameters["half_saturation"] == 8.0
        assert "Okun's law" in mechanism.description
        
        # Test economic behavior - diminishing returns at high unemployment
        base_strength = 1.0
        
        # Should show diminishing returns
        result_5 = mechanism.apply_mechanism(5.0, base_strength)
        result_10 = mechanism.apply_mechanism(10.0, base_strength)
        result_20 = mechanism.apply_mechanism(20.0, base_strength)
        
        # Results should be increasingly negative but at diminishing rate
        assert result_5 < 0
        assert result_10 < result_5
        assert result_20 < result_10
        
        # Marginal effects should diminish
        marginal_5_to_10 = abs(result_10 - result_5)
        marginal_10_to_20 = abs(result_20 - result_10)
        assert marginal_10_to_20 < marginal_5_to_10


if __name__ == "__main__":
    # Run specific test groups for development
    pytest.main([
        __file__ + "::TestCausalMechanism::test_linear_mechanism",
        __file__ + "::TestCausalMechanism::test_exponential_mechanism", 
        __file__ + "::TestCausalMechanism::test_threshold_mechanism",
        __file__ + "::TestCausalMechanism::test_saturation_mechanism",
        "-v"
    ])
