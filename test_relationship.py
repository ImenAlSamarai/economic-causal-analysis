
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.architecture import CausalEconomicGraph, EconomicVariable, CausalRelationship, VariableType
    print("✅ Basic imports successful")
    
    # Test CausalRelationship with correct parameters
    rel = CausalRelationship(
        source="test_source",
        target="test_target", 
        strength=0.5,
        confidence=0.8,
        lag_periods=1,
        relationship_type="linear"
    )
    print("✅ CausalRelationship created successfully")
    print("Parameters:", rel.source, "->", rel.target, "strength:", rel.strength)
    
except Exception as e:
    print("❌ Error:", str(e))
    import traceback
    traceback.print_exc()
