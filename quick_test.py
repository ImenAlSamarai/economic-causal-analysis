#!/usr/bin/env python3
"""
Quick 30-second verification test
"""
import sys
sys.path.insert(0, 'src')

try:
    from architecture import CausalEconomicGraph, EconomicVariable, VariableType
    graph = CausalEconomicGraph()
    var = EconomicVariable("test", VariableType.ENDOGENOUS, 1.0, 0.1, "test var")
    graph.add_variable(var)
    print("🎉 SUCCESS: System is working!")
    print(f"Graph created with {len(graph.variables)} variable(s)")
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)
