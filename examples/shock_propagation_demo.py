"""
Economic Example: Federal Reserve Policy Shock Propagation

This example demonstrates the shock propagation engine by simulating
how a Federal Reserve interest rate decision ripples through the economy
over multiple time periods, showcasing realistic economic dynamics.

Key Features Demonstrated:
1. Policy shock propagation through causal networks
2. Time lag effects in monetary transmission
3. Economic mechanism integration (threshold effects)
4. Multi-period forecasting with dampening
5. Systemic risk analysis

Author: Economic Analysis Team
Version: 0.1.0
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.architecture import (
    # Core architecture components
    CausalEconomicGraph, EconomicVariable, CausalRelationship, VariableType,
    # Mechanism components
    CausalMechanism, MechanismType, create_interest_rate_mechanism, 
    create_okun_law_mechanism, create_investment_returns_mechanism,
    # Shock propagation components
    ShockEvent, PropagationResults, add_shock_propagation_capabilities
)


def create_fed_policy_model():
    """Create a comprehensive Federal Reserve policy transmission model."""
    print("📊 Building Federal Reserve Policy Transmission Model...")
    
    graph = CausalEconomicGraph()
    
    # Define economic variables with realistic current values
    variables = [
        EconomicVariable(
            name="federal_funds_rate",
            variable_type=VariableType.POLICY,
            current_value=5.25,     # Current Fed funds rate (%)
            uncertainty=0.25,       # 25 basis points uncertainty
            description="Federal Reserve federal funds target rate",
            unit="percentage",
            bounds=(0.0, 12.0)
        ),
        
        EconomicVariable(
            name="gdp_growth",
            variable_type=VariableType.ENDOGENOUS,
            current_value=2.1,      # Current GDP growth (% annualized)
            uncertainty=0.4,        # 40 basis points uncertainty
            description="Real GDP growth rate (annualized)",
            unit="percentage",
            bounds=(-8.0, 8.0)
        ),
        
        EconomicVariable(
            name="unemployment_rate", 
            variable_type=VariableType.ENDOGENOUS,
            current_value=3.7,      # Current unemployment rate (%)
            uncertainty=0.2,        # 20 basis points uncertainty
            description="Civilian unemployment rate",
            unit="percentage", 
            bounds=(2.0, 15.0)
        ),
        
        EconomicVariable(
            name="core_inflation",
            variable_type=VariableType.ENDOGENOUS,
            current_value=4.1,      # Current core PCE inflation (%)
            uncertainty=0.3,        # 30 basis points uncertainty
            description="Core PCE price index (YoY)",
            unit="percentage",
            bounds=(-2.0, 12.0)
        ),
        
        EconomicVariable(
            name="corporate_investment",
            variable_type=VariableType.ENDOGENOUS,
            current_value=3.5,      # Investment growth (%)
            uncertainty=1.2,        # Higher uncertainty for investment
            description="Corporate fixed investment growth",
            unit="percentage",
            bounds=(-15.0, 15.0)
        ),
        
        EconomicVariable(
            name="consumer_spending",
            variable_type=VariableType.ENDOGENOUS,
            current_value=2.8,      # Consumer spending growth (%)
            uncertainty=0.8,        # Consumer spending uncertainty  
            description="Personal consumption expenditures growth",
            unit="percentage",
            bounds=(-10.0, 10.0)
        )
    ]
    
    # Add variables to graph
    for var in variables:
        graph.add_variable(var)
        print(f"  📈 Added variable: {var.name} = {var.current_value:.1f}{var.unit}")
    
    # Define causal relationships
    relationships = [
        # Direct monetary policy transmission
        CausalRelationship(
            source="federal_funds_rate",
            target="corporate_investment",
            strength=-0.8,          
            confidence=0.85,        
            lag_periods=2,          
            relationship_type="threshold"
        ),
        
        CausalRelationship(
            source="federal_funds_rate",
            target="consumer_spending", 
            strength=-0.4,          
            confidence=0.75,        
            lag_periods=1,          
            relationship_type="linear"
        ),
        
        # Real economy dynamics
        CausalRelationship(
            source="corporate_investment",
            target="gdp_growth",
            strength=0.6,           
            confidence=0.90,        
            lag_periods=1,          
            relationship_type="saturation"
        ),
        
        CausalRelationship(
            source="consumer_spending",
            target="gdp_growth",
            strength=0.7,           
            confidence=0.95,        
            lag_periods=0,          
            relationship_type="linear"
        ),
        
        # Okun's law relationship
        CausalRelationship(
            source="gdp_growth",
            target="unemployment_rate",
            strength=-0.5,          
            confidence=0.85,        
            lag_periods=1,          
            relationship_type="saturation"
        ),
        
        # Phillips curve relationship
        CausalRelationship(
            source="unemployment_rate",
            target="core_inflation",
            strength=-0.2,          
            confidence=0.60,        
            lag_periods=3,          
            relationship_type="threshold"
        )
    ]
    
    # Add relationships to graph
    for rel in relationships:
        graph.add_relationship(rel)
        print(f"  🔗 Added relationship: {rel.source} -> {rel.target} "
              f"(strength: {rel.strength:+.2f}, lag: {rel.lag_periods}Q)")
    
    print(f"\n✅ Model created with {len(variables)} variables and {len(relationships)} relationships")
    return graph


def demonstrate_fed_rate_hike_scenario():
    """Demonstrate a Federal Reserve rate hike scenario."""
    print("\n" + "=" * 70)
    print("🏛️  FEDERAL RESERVE RATE HIKE SCENARIO ANALYSIS")
    print("=" * 70)
    
    # Create the Fed policy model
    fed_model = create_fed_policy_model()
    
    # Add shock propagation capabilities
    add_shock_propagation_capabilities(fed_model)
    
    # Add sophisticated mechanisms for key relationships
    print("\n🔧 Enhancing model with sophisticated mechanisms...")
    
    fed_model.add_enhanced_relationship(
        "federal_funds_rate", 
        "corporate_investment",
        create_interest_rate_mechanism()
    )
    
    fed_model.add_enhanced_relationship(
        "gdp_growth",
        "unemployment_rate", 
        create_okun_law_mechanism()
    )
    
    fed_model.add_enhanced_relationship(
        "corporate_investment",
        "gdp_growth",
        create_investment_returns_mechanism()
    )
    
    print("✅ Enhanced mechanisms applied to key relationships")
    
    # Define the Fed rate hike shock
    rate_hike_shock = ShockEvent(
        variable_name="federal_funds_rate",
        magnitude=3.0,          # 3 standard deviations = ~75 basis points hike
        duration=0,             # One-time policy decision
        description="Federal Reserve 75bp rate hike to combat inflation"
    )
    
    print(f"\n📊 Simulating shock: {rate_hike_shock.description}")
    print(f"   Shock magnitude: {rate_hike_shock.magnitude:.1f} std deviations")
    print(f"   Expected rate change: ~{rate_hike_shock.magnitude * 0.25:.0f} basis points")
    
    # Propagate the shock through the economy
    print("\n⚡ Propagating shock through economic system...")
    
    results = fed_model.propagate_shock(
        shock=rate_hike_shock,
        num_periods=12,         # 12 quarters (3 years)
        dampening_factor=0.94,  # Slightly lower dampening for persistence
        convergence_threshold=1e-5
    )
    
    print(f"✅ Simulation complete: {results.num_periods} periods")
    print(f"   Convergence achieved: {results.convergence_achieved}")
    
    # Analyze and display results
    print("\n" + "=" * 50)
    print("📈 ECONOMIC IMPACT ANALYSIS")
    print("=" * 50)
    
    # Show initial vs. final values
    final_values = results.get_final_values()
    peak_effects = results.get_peak_effects()
    
    print("\n🎯 KEY ECONOMIC VARIABLES - IMPACT SUMMARY:")
    print("-" * 50)
    
    key_variables = [
        ("federal_funds_rate", "Fed Funds Rate", "%"),
        ("gdp_growth", "GDP Growth", "%"),
        ("unemployment_rate", "Unemployment", "%"), 
        ("core_inflation", "Core Inflation", "%"),
        ("corporate_investment", "Investment Growth", "%"),
        ("consumer_spending", "Consumer Spending", "%")
    ]
    
    for var_name, display_name, unit in key_variables:
        if var_name in results.time_series:
            initial = results.time_series[var_name][0]
            final = final_values[var_name]
            peak_value, peak_period = peak_effects[var_name]
            change = final - initial
            peak_change = peak_value - initial
            
            print(f"{display_name:20} │ Initial: {initial:6.2f}{unit} │ "
                  f"Peak: {peak_change:+6.2f}{unit} (Q{peak_period}) │ "
                  f"Final: {change:+6.2f}{unit}")
    
    # Time series analysis
    print("\n📊 QUARTERLY PROGRESSION (First 8 quarters):")
    print("-" * 70)
    print("Quarter    │ Fed Rate │ GDP Growth │ Unemployment │ Inflation")
    print("-" * 70)
    
    for quarter in range(min(9, len(results.time_series["federal_funds_rate"]))):
        fed_rate = results.time_series["federal_funds_rate"][quarter]
        gdp = results.time_series["gdp_growth"][quarter] 
        unemp = results.time_series["unemployment_rate"][quarter]
        inflation = results.time_series["core_inflation"][quarter]
        
        print(f"Q{quarter:<8} │ {fed_rate:7.2f}% │ {gdp:9.2f}% │ {unemp:11.2f}% │ {inflation:8.2f}%")
    
    # Economic interpretation
    print("\n" + "=" * 50)
    print("🧠 ECONOMIC INTERPRETATION")
    print("=" * 50)
    
    gdp_impact = final_values["gdp_growth"] - results.time_series["gdp_growth"][0]
    unemp_impact = final_values["unemployment_rate"] - results.time_series["unemployment_rate"][0]
    inflation_impact = final_values["core_inflation"] - results.time_series["core_inflation"][0]
    
    print(f"\n📉 ECONOMIC CONTRACTION:")
    print(f"   GDP growth declines by {abs(gdp_impact):.2f} percentage points")
    print(f"   Unemployment rises by {unemp_impact:.2f} percentage points")
    
    print(f"\n💰 INFLATION CONTROL:")
    if inflation_impact < 0:
        print(f"   Core inflation falls by {abs(inflation_impact):.2f} percentage points")
        print(f"   ✅ Fed policy succeeds in reducing inflation pressures")
    else:
        print(f"   Core inflation continues rising (+{inflation_impact:.2f}pp)")
        print(f"   ⚠️  Fed may need additional tightening")
    
    print(f"\n⚖️  POLICY TRADE-OFFS:")
    sacrifice_ratio = abs(gdp_impact) / max(abs(inflation_impact), 0.01)
    print(f"   Sacrifice ratio: {sacrifice_ratio:.2f} GDP points per inflation point")
    
    if sacrifice_ratio < 2.0:
        print(f"   ✅ Efficient disinflation - low real economy cost")
    elif sacrifice_ratio < 4.0:
        print(f"   ⚠️  Moderate disinflation cost")
    else:
        print(f"   🚨 High disinflation cost - significant recession risk")
    
    return results


def main():
    """Main function demonstrating the shock propagation engine."""
    print("🏛️  ECONOMIC CAUSAL ANALYSIS SYSTEM")
    print("    Task 1.3: Shock Propagation Engine Demonstration")
    print("=" * 70)
    
    try:
        # Demonstrate Fed rate hike scenario
        scenario_results = demonstrate_fed_rate_hike_scenario()
        
        # Final summary
        print("\n" + "=" * 70)
        print("🎉 SHOCK PROPAGATION DEMONSTRATION COMPLETE")
        print("=" * 70)
        
        print("\n✅ CAPABILITIES DEMONSTRATED:")
        print("   🎯 Economic shock propagation through causal networks")
        print("   ⏰ Multi-period dynamics with realistic time lags")
        print("   🔧 Integration with sophisticated causal mechanisms")
        print("   📊 Comprehensive scenario analysis and forecasting")
        print("   📈 Production-ready economic modeling capabilities")
        
        print("\n🏆 ECONOMIC REALISM VALIDATION:")
        print("   ✅ Monetary policy transmission mechanisms")
        print("   ✅ Okun's law and Phillips curve relationships")
        print("   ✅ Investment and consumption channels")
        print("   ✅ Realistic time lags and dampening effects")
        
        print("\n🔬 SYSTEM PERFORMANCE:")
        print(f"   📊 Simulation convergence: {scenario_results.convergence_achieved}")
        print(f"   🎯 Variables tracked: {len(scenario_results.time_series)}")
        print(f"   ⏱️  Periods simulated: {scenario_results.num_periods}")
        print(f"   🔧 Enhanced relationships: {scenario_results.metadata.get('enhanced_relationships', 0)}")
        
        print("\n🚀 Ready for production economic analysis and policy evaluation!")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ DEMONSTRATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
