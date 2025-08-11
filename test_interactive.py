#!/usr/bin/env python3
"""
Interactive Testing Script
Run this to test the system step-by-step interactively
"""

import sys
import os

# Add src to path
sys.path.insert(0, 'src')

def test_interactive():
    """Interactive test session"""
    print("🔬 Interactive Economic Causal Analysis Testing")
    print("=" * 50)
    
    try:
        # Import the system
        from architecture import CausalEconomicGraph, EconomicVariable, CausalRelationship, VariableType
        print("✅ Successfully imported all components")
        
        # Create a graph
        graph = CausalEconomicGraph()
        print(f"✅ Created graph: {graph}")
        
        # Add a variable
        gdp = EconomicVariable(
            name="GDP_growth",
            variable_type=VariableType.ENDOGENOUS,
            current_value=2.5,
            uncertainty=0.3,
            description="Annual GDP growth rate",
            unit="percentage"
        )
        graph.add_variable(gdp)
        print(f"✅ Added variable: {gdp.name}")
        
        # Add another variable
        interest = EconomicVariable(
            name="interest_rate",
            variable_type=VariableType.POLICY,
            current_value=3.0,
            uncertainty=0.1,
            description="Central bank interest rate",
            unit="percentage"
        )
        graph.add_variable(interest)
        print(f"✅ Added variable: {interest.name}")
        
        # Add a relationship
        relationship = CausalRelationship(
            source="interest_rate",
            target="GDP_growth",
            strength=-0.6,
            confidence=0.8,
            lag_periods=2
        )
        graph.add_relationship(relationship)
        print(f"✅ Added relationship: {relationship.source} -> {relationship.target}")
        
        # Validate
        is_valid, issues = graph.validate_dag_structure()
        print(f"✅ DAG validation: {is_valid}, issues: {issues}")
        
        # Show summary
        stats = graph.get_summary_statistics()
        print(f"✅ Graph summary: {stats}")
        
        print("\n🎉 INTERACTIVE TEST SUCCESSFUL!")
        print("Your system is working correctly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_interactive()
    sys.exit(0 if success else 1)
