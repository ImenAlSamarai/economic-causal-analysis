"""
Visual Demo: Economic Causal Analysis with Comprehensive Visualizations

This demo showcases the visualization capabilities of the Economic Causal Analysis System,
providing compelling visual representations of causal relationships, shock propagation,
and mechanism behaviors.

Key Features Demonstrated:
- Interactive causal network visualization
- Shock propagation time series with uncertainty bands
- Mechanism comparison charts
- Comprehensive results dashboard

Run this demo to see the full power of the system's visualization capabilities.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.architecture import (
    CausalEconomicGraph, EconomicVariable, CausalRelationship, VariableType,
    ShockEvent, add_shock_propagation_capabilities,
    plot_causal_network, plot_shock_propagation, plot_mechanism_comparison,
    create_results_dashboard, quick_visualize
)


def create_comprehensive_economic_model():
    """Create a realistic economic model for visualization."""
    
    print("🏗️ Building Comprehensive Economic Model...")
    
    # Create graph
    graph = CausalEconomicGraph()
    
    # Define economic variables
    variables = {
        "fed_funds_rate": EconomicVariable(
            name="fed_funds_rate",
            variable_type=VariableType.POLICY,
            current_value=3.0,
            uncertainty=0.25,
            description="Federal funds rate",
            unit="percentage",
            bounds=(0, 15)
        ),
        
        "gdp_growth": EconomicVariable(
            name="gdp_growth", 
            variable_type=VariableType.ENDOGENOUS,
            current_value=2.3,
            uncertainty=0.4,
            description="GDP growth rate",
            unit="percentage",
            bounds=(-5, 8)
        ),
        
        "inflation_rate": EconomicVariable(
            name="inflation_rate",
            variable_type=VariableType.ENDOGENOUS, 
            current_value=2.8,
            uncertainty=0.3,
            description="Consumer price inflation",
            unit="percentage",
            bounds=(-2, 12)
        ),
        
        "unemployment_rate": EconomicVariable(
            name="unemployment_rate",
            variable_type=VariableType.ENDOGENOUS,
            current_value=4.1,
            uncertainty=0.2,
            description="Unemployment rate", 
            unit="percentage",
            bounds=(2, 15)
        ),
        
        "consumer_confidence": EconomicVariable(
            name="consumer_confidence",
            variable_type=VariableType.INDICATOR,
            current_value=85.0,
            uncertainty=8.0,
            description="Consumer confidence index",
            unit="index",
            bounds=(20, 150)
        ),
        
        "oil_price": EconomicVariable(
            name="oil_price",
            variable_type=VariableType.EXOGENOUS,
            current_value=75.0,
            uncertainty=12.0,
            description="Crude oil price",
            unit="USD/barrel", 
            bounds=(20, 200)
        ),
        
        "stock_market": EconomicVariable(
            name="stock_market",
            variable_type=VariableType.MARKET,
            current_value=4200.0,
            uncertainty=200.0,
            description="S&P 500 index",
            unit="index",
            bounds=(1000, 8000)
        )
    }
    
    # Add variables to graph
    for variable in variables.values():
        graph.add_variable(variable)
        print(f"   ✓ Added {variable.name}: {variable.current_value} {variable.unit}")
    
    # Define causal relationships
    relationships = [
        # Monetary policy transmission
        CausalRelationship("fed_funds_rate", "gdp_growth", -0.45, 0.85, 2),
        CausalRelationship("fed_funds_rate", "inflation_rate", -0.35, 0.80, 4),
        CausalRelationship("fed_funds_rate", "stock_market", -0.60, 0.75, 1),
        
        # Okun's law and Phillips curve
        CausalRelationship("gdp_growth", "unemployment_rate", -0.40, 0.90, 1),
        CausalRelationship("unemployment_rate", "inflation_rate", -0.25, 0.70, 2),
        
        # Confidence and market effects
        CausalRelationship("gdp_growth", "consumer_confidence", 0.55, 0.75, 1),
        CausalRelationship("stock_market", "consumer_confidence", 0.40, 0.65, 0),
        # Note: Removed consumer_confidence -> gdp_growth to prevent cycle
        
        # Oil price impacts
        CausalRelationship("oil_price", "inflation_rate", 0.20, 0.80, 1),
        CausalRelationship("oil_price", "gdp_growth", -0.15, 0.70, 2),
    ]
    
    # Add relationships to graph
    print(f"\n🔗 Adding {len(relationships)} Causal Relationships:")
    for relationship in relationships:
        graph.add_relationship(relationship)
        print(f"   ✓ {relationship.source} → {relationship.target} "
              f"(strength: {relationship.strength:+.2f}, lag: {relationship.lag_periods})")
    
    # Add shock propagation capabilities
    add_shock_propagation_capabilities(graph)
    
    # Validate
    is_valid, issues = graph.validate_dag_structure()
    if is_valid:
        print(f"\n✅ Economic model validated successfully!")
        print(f"   📊 Variables: {len(variables)}")
        print(f"   🔗 Relationships: {len(relationships)}")
        print(f"   📈 DAG structure: Valid")
    else:
        print(f"\n❌ Validation issues: {issues}")
        
    return graph


def run_visualization_demo():
    """Run comprehensive visualization demonstration."""
    
    print("\n" + "="*80)
    print("🎨 ECONOMIC CAUSAL ANALYSIS - VISUAL DEMONSTRATION")
    print("="*80)
    
    # Create model
    graph = create_comprehensive_economic_model()
    
    print("\n" + "="*60)
    print("📊 VISUALIZATION 1: CAUSAL NETWORK STRUCTURE")
    print("="*60)
    print("Displaying the causal relationships as an interactive network...")
    
    # 1. Network visualization
    plot_causal_network(graph, figsize=(14, 10))
    
    print("\n" + "="*60)
    print("📈 VISUALIZATION 2: MECHANISM COMPARISON")
    print("="*60)
    print("Comparing different causal mechanism types...")
    
    # 2. Mechanism comparison
    plot_mechanism_comparison(figsize=(12, 8))
    
    print("\n" + "="*60)  
    print("🎯 VISUALIZATION 3: SHOCK PROPAGATION ANALYSIS")
    print("="*60)
    print("Simulating Federal Reserve emergency rate hike...")
    
    # 3. Create and propagate shock
    emergency_hike = ShockEvent(
        variable_name="fed_funds_rate",
        magnitude=2.5,  # 2.5 standard deviation shock
        duration=0,     # One-time shock
        description="Emergency Fed Rate Hike - Financial Crisis Response"
    )
    
    # Run shock propagation
    print(f"   🎯 Shock: {emergency_hike.description}")
    print(f"   📊 Magnitude: {emergency_hike.magnitude}σ")
    print(f"   ⏱️  Simulation periods: 12")
    
    results = graph.propagate_shock(
        shock=emergency_hike,
        num_periods=12,
        dampening_factor=0.94
    )
    
    print(f"   ✅ Simulation complete!")
    print(f"   🎯 Convergence: {'Achieved' if results.convergence_achieved else 'Not achieved'}")
    
    # 4. Time series visualization
    plot_shock_propagation(results, 
                          variables=['fed_funds_rate', 'gdp_growth', 'inflation_rate', 
                                   'unemployment_rate', 'consumer_confidence'],
                          figsize=(15, 8))
    
    print("\n" + "="*60)
    print("📋 VISUALIZATION 4: COMPREHENSIVE DASHBOARD")
    print("="*60)
    print("Creating executive summary dashboard...")
    
    # 5. Results dashboard
    create_results_dashboard(results, graph, figsize=(18, 12))
    
    # Print key insights
    print("\n" + "="*60)
    print("🔍 KEY INSIGHTS FROM ANALYSIS")
    print("="*60)
    
    peak_effects = results.get_peak_effects()
    final_values = results.get_final_values()
    
    print(f"📈 PEAK EFFECTS:")
    for var, (peak_val, period) in list(peak_effects.items())[:5]:
        initial = results.time_series[var][0]
        impact = peak_val - initial
        print(f"   • {var.replace('_', ' ').title()}: {impact:+.2f} at period {period}")
    
    print(f"\n💰 ECONOMIC IMPACT:")
    gdp_impact = final_values['gdp_growth'] - results.time_series['gdp_growth'][0]
    unemployment_impact = final_values['unemployment_rate'] - results.time_series['unemployment_rate'][0]
    
    print(f"   • GDP Growth: {gdp_impact:+.2f} percentage points")
    print(f"   • Unemployment: {unemployment_impact:+.2f} percentage points")
    print(f"   • Consumer Confidence: {final_values['consumer_confidence'] - results.time_series['consumer_confidence'][0]:+.1f} index points")
    
    print(f"\n📊 SIMULATION QUALITY:")
    print(f"   • Convergence: {'✓' if results.convergence_achieved else '✗'}")
    print(f"   • Periods simulated: {results.num_periods}")
    print(f"   • Dampening factor: {results.dampening_factor}")
    
    return graph, results


def main():
    """Main demonstration function."""
    
    try:
        print("🚀 Starting Economic Causal Analysis Visual Demo...")
        
        # Run visualization demo
        graph, results = run_visualization_demo()
        
        print("\n" + "="*80)
        print("🎉 VISUAL DEMONSTRATION COMPLETE!")
        print("="*80)
        print("✅ Successfully demonstrated all visualization capabilities:")
        print("   📊 Causal network structure visualization")
        print("   📈 Mechanism comparison charts")
        print("   🎯 Shock propagation time series")
        print("   📋 Comprehensive results dashboard")
        print("\n💡 The Economic Causal Analysis System provides powerful")
        print("   visualization tools for policy analysis and research!")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ DEMO FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)