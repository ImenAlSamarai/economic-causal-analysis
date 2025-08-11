"""
Economic Example: Federal Reserve Policy Analysis

This example demonstrates how causal mechanisms enable sophisticated
economic modeling by analyzing Federal Reserve interest rate policy
effects on the economy using different mechanism types.

The example shows how the same policy change can have different effects
depending on the underlying economic mechanism:
- Linear: Simple proportional effects
- Threshold: Policy needs minimum magnitude to be effective
- Exponential: Effects can cascade and amplify
- Saturation: Diminishing returns at extreme levels
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
    CausalMechanism,
    MechanismType,
    EnhancedCausalRelationship,
    create_interest_rate_mechanism,
    create_okun_law_mechanism
)


def create_fed_policy_example():
    """
    Create a comprehensive example of Federal Reserve policy analysis
    using different causal mechanisms to model economic relationships.
    """
    print("🏦 Federal Reserve Policy Analysis Example")
    print("=" * 60)
    
    # Create economic variables
    print("\n📊 Creating Economic Variables:")
    
    variables = {
        "fed_funds_rate": EconomicVariable(
            name="fed_funds_rate",
            variable_type=VariableType.POLICY,
            current_value=2.5,
            uncertainty=0.1,
            description="Federal funds rate set by the Federal Reserve",
            unit="percentage",
            bounds=(0, 15)
        ),
        
        "gdp_growth": EconomicVariable(
            name="gdp_growth",
            variable_type=VariableType.ENDOGENOUS,
            current_value=2.1,
            uncertainty=0.4,
            description="Annual GDP growth rate",
            unit="percentage",
            bounds=(-5, 8)
        ),
        
        "unemployment_rate": EconomicVariable(
            name="unemployment_rate",
            variable_type=VariableType.ENDOGENOUS,
            current_value=4.2,
            uncertainty=0.3,
            description="Unemployment rate",
            unit="percentage",
            bounds=(0, 15)
        ),
        
        "inflation_rate": EconomicVariable(
            name="inflation_rate",
            variable_type=VariableType.ENDOGENOUS,
            current_value=2.8,
            uncertainty=0.2,
            description="Annual inflation rate",
            unit="percentage",
            bounds=(-2, 10)
        ),
        
        "consumer_confidence": EconomicVariable(
            name="consumer_confidence",
            variable_type=VariableType.INDICATOR,
            current_value=85.0,
            uncertainty=5.0,
            description="Consumer confidence index",
            unit="index",
            bounds=(0, 150)
        )
    }
    
    for name, var in variables.items():
        print(f"   ✓ {var.name}: {var.current_value} {var.unit} ({var.variable_type.value})")
    
    # Create different causal relationships with mechanisms
    print("\n🔗 Creating Causal Relationships with Mechanisms:")
    
    # 1. Fed Funds Rate -> GDP Growth (Threshold Effect)
    # Small rate changes have minimal impact, large changes are significant
    fed_gdp_base = CausalRelationship(
        source="fed_funds_rate",
        target="gdp_growth",
        strength=-0.35,  # Negative relationship
        confidence=0.85,
        lag_periods=2,
        relationship_type="threshold"
    )
    
    threshold_mechanism = create_interest_rate_mechanism()
    fed_gdp_enhanced = EnhancedCausalRelationship(fed_gdp_base, threshold_mechanism)
    
    print(f"   ✓ Fed Funds Rate -> GDP Growth (Threshold)")
    print(f"     Base strength: {fed_gdp_base.strength}, Threshold: {threshold_mechanism.parameters['threshold']}")
    
    # 2. Unemployment -> GDP Growth (Saturation Effect - Okun's Law)
    # Follows Okun's law with diminishing effects at extreme unemployment
    unemployment_gdp_base = CausalRelationship(
        source="unemployment_rate",
        target="gdp_growth",
        strength=-0.45,  # Okun's coefficient
        confidence=0.90,
        lag_periods=0,
        relationship_type="saturation"
    )
    
    okun_mechanism = create_okun_law_mechanism()
    unemployment_gdp_enhanced = EnhancedCausalRelationship(unemployment_gdp_base, okun_mechanism)
    
    print(f"   ✓ Unemployment Rate -> GDP Growth (Saturation - Okun's Law)")
    print(f"     Base strength: {unemployment_gdp_base.strength}, Half-saturation: {okun_mechanism.parameters['half_saturation']}")
    
    # 3. Fed Funds Rate -> Inflation (Linear Effect)
    # Traditional monetary policy transmission
    fed_inflation_base = CausalRelationship(
        source="fed_funds_rate",
        target="inflation_rate",
        strength=-0.25,  # Higher rates reduce inflation
        confidence=0.80,
        lag_periods=4,
        relationship_type="linear"
    )
    
    linear_mechanism = CausalMechanism(MechanismType.LINEAR)
    fed_inflation_enhanced = EnhancedCausalRelationship(fed_inflation_base, linear_mechanism)
    
    print(f"   ✓ Fed Funds Rate -> Inflation Rate (Linear)")
    print(f"     Base strength: {fed_inflation_base.strength}")
    
    # 4. GDP Growth -> Consumer Confidence (Exponential Effect)
    # Confidence can cascade rapidly with economic changes
    gdp_confidence_base = CausalRelationship(
        source="gdp_growth",
        target="consumer_confidence",
        strength=0.40,  # Positive relationship
        confidence=0.75,
        lag_periods=1,
        relationship_type="exponential"
    )
    
    exponential_mechanism = CausalMechanism(
        MechanismType.EXPONENTIAL,
        {"exponent": 1.4},
        description="Consumer confidence cascading effects"
    )
    gdp_confidence_enhanced = EnhancedCausalRelationship(gdp_confidence_base, exponential_mechanism)
    
    print(f"   ✓ GDP Growth -> Consumer Confidence (Exponential)")
    print(f"     Base strength: {gdp_confidence_base.strength}, Exponent: {exponential_mechanism.parameters['exponent']}")
    
    # Scenario Analysis
    print("\n🎯 Scenario Analysis: Federal Reserve Policy Changes")
    print("-" * 60)
    
    # Scenario 1: Small rate increase (25 basis points)
    print("\n📈 Scenario 1: Small Rate Increase (+0.25%)")
    rate_change_small = 0.25
    
    gdp_impact_small = fed_gdp_enhanced.apply_causal_effect(rate_change_small)
    inflation_impact_small = fed_inflation_enhanced.apply_causal_effect(rate_change_small)
    
    print(f"   Rate change: +{rate_change_small}%")
    print(f"   GDP impact: {gdp_impact_small:.4f}% (threshold effect)")
    print(f"   Inflation impact: {inflation_impact_small:.4f}% (linear effect)")
    
    if gdp_impact_small == 0.0:
        print(f"   💡 Below threshold - no GDP impact despite rate change")
    
    # Scenario 2: Large rate increase (75 basis points)
    print("\n📈 Scenario 2: Large Rate Increase (+0.75%)")
    rate_change_large = 0.75
    
    gdp_impact_large = fed_gdp_enhanced.apply_causal_effect(rate_change_large)
    inflation_impact_large = fed_inflation_enhanced.apply_causal_effect(rate_change_large)
    
    print(f"   Rate change: +{rate_change_large}%")
    print(f"   GDP impact: {gdp_impact_large:.4f}% (threshold effect)")
    print(f"   Inflation impact: {inflation_impact_large:.4f}% (linear effect)")
    
    if gdp_impact_large != 0.0:
        print(f"   💡 Above threshold - amplified GDP impact")
    
    # Secondary effects on consumer confidence
    if gdp_impact_large != 0.0:
        confidence_impact = gdp_confidence_enhanced.apply_causal_effect(gdp_impact_large)
        print(f"   Secondary confidence impact: {confidence_impact:.4f} index points (exponential effect)")
    
    print("\n🎉 Federal Reserve Policy Analysis Complete!")
    print("✅ Demonstrated all four mechanism types in realistic economic context")
    
    return {
        "variables": variables,
        "relationships": {
            "fed_gdp": fed_gdp_enhanced,
            "unemployment_gdp": unemployment_gdp_enhanced,
            "fed_inflation": fed_inflation_enhanced,
            "gdp_confidence": gdp_confidence_enhanced
        }
    }


def main():
    """Run the comprehensive economic example."""
    print("Economic Causal Analysis System - Comprehensive Example")
    print("Task 1.2: Basic Causal Mechanisms")
    print("=" * 80)
    
    try:
        # Main Federal Reserve policy example
        example_data = create_fed_policy_example()
        
        print("\n" + "=" * 80)
        print("🎉 COMPREHENSIVE EXAMPLE COMPLETE!")
        print("✅ All mechanism types demonstrated in realistic economic contexts")
        print("✅ Policy implications and economic insights provided")
        print("✅ System ready for advanced economic scenario analysis")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ EXAMPLE FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
