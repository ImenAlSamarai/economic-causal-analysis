#!/usr/bin/env python3
"""
Quick test for demo_basic.py imports and basic functionality
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("🧪 Testing imports...")
    
    from src.architecture import (
        CausalEconomicGraph, EconomicVariable, CausalRelationship, VariableType,
        CausalMechanism, MechanismType, EnhancedCausalRelationship,
        create_interest_rate_mechanism, create_okun_law_mechanism,
        create_oil_shock_mechanism, create_investment_returns_mechanism,
        ShockEvent, PropagationResults, ShockPropagationEngine,
        add_shock_propagation_capabilities
    )
    print("✅ All imports successful!")
    
    # Test basic class instantiation
    print("🧪 Testing basic instantiation...")
    graph = CausalEconomicGraph()
    print("✅ CausalEconomicGraph created successfully!")
    
    # Test variable creation
    variable = EconomicVariable(
        name="test_var",
        variable_type=VariableType.POLICY,
        current_value=5.0,
        uncertainty=0.1,
        description="Test variable",
        unit="percentage",
        bounds=(0.0, 10.0)
    )
    print("✅ EconomicVariable created successfully!")
    
    # Test adding variable to graph
    graph.add_variable(variable)
    print("✅ Variable added to graph successfully!")
    
    print("\n🚀 Basic setup test PASSED!")
    print("📝 demo_basic.py should work correctly.")
    
except Exception as e:
    print(f"❌ Test FAILED: {str(e)}")
    print("🔧 Please check system configuration")
    import traceback
    traceback.print_exc()
