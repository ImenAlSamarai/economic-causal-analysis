"""
Validation Script for Causal Economic Graph

This script validates the core functionality of the CausalEconomicGraph system
by creating a sample economic network and testing all required operations.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.architecture import (
    CausalEconomicGraph, 
    EconomicVariable, 
    CausalRelationship, 
    VariableType
)


def test_basic_functionality():
    """Test basic graph creation and validation."""
    print("=== Testing Basic Functionality ===")
    
    # Create graph
    graph = CausalEconomicGraph()
    print(f"✓ Created empty graph: {graph}")
    
    # Create 5 economic variables as specified
    variables = [
        EconomicVariable(
            name="GDP_growth",
            variable_type=VariableType.ENDOGENOUS,
            current_value=2.5,
            uncertainty=0.3,
            description="Annual GDP growth rate",
            unit="percentage",
            bounds=(0, 10)
        ),
        EconomicVariable(
            name="interest_rate",
            variable_type=VariableType.POLICY,
            current_value=3.0,
            uncertainty=0.1,
            description="Central bank interest rate",
            unit="percentage",
            bounds=(0, 15)
        ),
        EconomicVariable(
            name="inflation",
            variable_type=VariableType.ENDOGENOUS,
            current_value=2.0,
            uncertainty=0.2,
            description="Consumer price inflation",
            unit="percentage",
            bounds=(-2, 10)
        ),
        EconomicVariable(
            name="unemployment",
            variable_type=VariableType.ENDOGENOUS,
            current_value=5.2,
            uncertainty=0.4,
            description="Unemployment rate",
            unit="percentage",
            bounds=(0, 20)
        ),
        EconomicVariable(
            name="oil_price",
            variable_type=VariableType.EXOGENOUS,
            current_value=75.0,
            uncertainty=5.0,
            description="Crude oil price per barrel",
            unit="USD",
            bounds=(20, 200)
        )
    ]
    
    # Add variables to graph
    for var in variables:
        graph.add_variable(var)
    
    print(f"✓ Added {len(variables)} variables to graph")
    
    # Test variable retrieval
    gdp_var = graph.get_variable("GDP_growth")
    assert gdp_var is not None
    assert gdp_var.name == "GDP_growth"
    print("✓ Variable retrieval works")
    
    return graph


def test_causal_relationships(graph):
    """Test adding causal relationships without creating cycles."""
    print("\n=== Testing Causal Relationships ===")
    
    # Define realistic economic relationships
    relationships = [
        CausalRelationship(
            source="interest_rate",
            target="GDP_growth",
            strength=-0.6,  # Higher interest rates reduce GDP growth
            confidence=0.8,
            lag_periods=2,
            relationship_type="linear"
        ),
        CausalRelationship(
            source="interest_rate",
            target="inflation",
            strength=-0.4,  # Higher interest rates reduce inflation
            confidence=0.7,
            lag_periods=3,
            relationship_type="linear"
        ),
        CausalRelationship(
            source="GDP_growth",
            target="unemployment",
            strength=-0.7,  # Higher GDP growth reduces unemployment (Okun's law)
            confidence=0.9,
            lag_periods=1,
            relationship_type="linear"
        ),
        CausalRelationship(
            source="oil_price",
            target="inflation",
            strength=0.3,  # Higher oil prices increase inflation
            confidence=0.6,
            lag_periods=1,
            relationship_type="linear"
        ),
        CausalRelationship(
            source="oil_price",
            target="GDP_growth",
            strength=-0.2,  # Higher oil prices reduce GDP growth
            confidence=0.5,
            lag_periods=2,
            relationship_type="linear"
        )
    ]
    
    # Add relationships
    for rel in relationships:
        graph.add_relationship(rel)
    
    print(f"✓ Added {len(relationships)} causal relationships")
    
    # Test relationship retrieval
    interest_gdp_rel = graph.get_relationship("interest_rate", "GDP_growth")
    assert interest_gdp_rel is not None
    assert interest_gdp_rel.strength == -0.6
    print("✓ Relationship retrieval works")
    
    # Test causal queries
    gdp_ancestors = graph.get_causal_ancestors("GDP_growth")
    print(f"✓ GDP growth ancestors: {gdp_ancestors}")
    
    interest_descendants = graph.get_causal_descendants("interest_rate")
    print(f"✓ Interest rate descendants: {interest_descendants}")
    
    # Test direct effects
    oil_effects = graph.get_direct_effects("oil_price")
    print(f"✓ Oil price direct effects: {[(target, rel.strength) for target, rel in oil_effects]}")
    
    return graph


def test_dag_validation(graph):
    """Test DAG structure validation."""
    print("\n=== Testing DAG Validation ===")
    
    # Validate current DAG
    is_valid, issues = graph.validate_dag_structure()
    print(f"✓ DAG validation: valid={is_valid}, issues={issues}")
    assert is_valid, f"Expected valid DAG, but got issues: {issues}"
    
    # Test cycle prevention
    try:
        # Try to create a cycle: GDP_growth -> interest_rate (would close loop)
        cycle_rel = CausalRelationship(
            source="GDP_growth",
            target="interest_rate",
            strength=0.3,
            confidence=0.5
        )
        graph.add_relationship(cycle_rel)
        assert False, "Expected cycle detection to raise ValueError"
    except ValueError as e:
        print(f"✓ Cycle prevention works: {e}")
    
    return graph


def test_error_handling():
    """Test error handling for invalid inputs."""
    print("\n=== Testing Error Handling ===")
    
    graph = CausalEconomicGraph()
    
    # Test invalid variable bounds
    try:
        invalid_var = EconomicVariable(
            name="test",
            variable_type=VariableType.ENDOGENOUS,
            current_value=15.0,  # Above upper bound
            uncertainty=0.1,
            description="Test variable",
            bounds=(0, 10)
        )
        assert False, "Expected bounds validation to raise ValueError"
    except ValueError:
        print("✓ Variable bounds validation works")
    
    # Test invalid relationship strength
    try:
        invalid_rel = CausalRelationship(
            source="A",
            target="B",
            strength=1.5,  # Outside [-1, 1] range
            confidence=0.8
        )
        assert False, "Expected strength validation to raise ValueError"
    except ValueError:
        print("✓ Relationship strength validation works")
    
    # Test adding relationship with non-existent variables
    try:
        graph.add_relationship(CausalRelationship(
            source="nonexistent",
            target="also_nonexistent",
            strength=0.5,
            confidence=0.8
        ))
        assert False, "Expected missing variable error"
    except ValueError as e:
        print(f"✓ Missing variable detection works: {e}")


def test_summary_statistics(graph):
    """Test summary statistics generation."""
    print("\n=== Testing Summary Statistics ===")
    
    stats = graph.get_summary_statistics()
    print(f"Graph Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Verify expected values
    assert stats['num_variables'] == 5
    assert stats['num_relationships'] == 5
    assert stats['is_dag'] == True
    
    print("✓ Summary statistics are correct")


def test_topological_order(graph):
    """Test topological ordering for scenario propagation."""
    print("\n=== Testing Topological Order ===")
    
    topo_order = graph.get_topological_order()
    print(f"Topological order: {topo_order}")
    
    # Verify that exogenous variables come before endogenous
    oil_idx = topo_order.index("oil_price")
    interest_idx = topo_order.index("interest_rate")
    gdp_idx = topo_order.index("GDP_growth")
    
    # Oil price and interest rate should come before GDP growth
    assert oil_idx < gdp_idx or interest_idx < gdp_idx
    print("✓ Topological ordering respects causal structure")


def main():
    """Run all validation tests."""
    print("Economic Causal Graph Validation")
    print("=" * 50)
    
    try:
        # Test basic functionality
        graph = test_basic_functionality()
        
        # Test causal relationships
        graph = test_causal_relationships(graph)
        
        # Test DAG validation
        graph = test_dag_validation(graph)
        
        # Test error handling
        test_error_handling()
        
        # Test summary statistics
        test_summary_statistics(graph)
        
        # Test topological order
        test_topological_order(graph)
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("The CausalEconomicGraph system is working correctly.")
        print(f"Final graph: {graph}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
