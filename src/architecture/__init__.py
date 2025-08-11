"""
Architecture Module

Core components for building and managing causal economic graphs.
"""

from .causal_economic_graph import (
    EconomicVariable,
    CausalRelationship, 
    CausalEconomicGraph,
    VariableType
)

from .causal_mechanisms import (
    CausalMechanism,
    MechanismType,
    EnhancedCausalRelationship,
    create_interest_rate_mechanism,
    create_okun_law_mechanism,
    create_oil_shock_mechanism,
    create_investment_returns_mechanism
)

from .shock_propagation import (
    ShockEvent,
    PropagationResults,
    ShockPropagationEngine,
    add_shock_propagation_capabilities
)

from .visualization import (
    plot_causal_network,
    plot_shock_propagation,
    plot_mechanism_comparison,
    create_results_dashboard,
    quick_visualize
)

__all__ = [
    # Task 1.1 - Existing exports
    "EconomicVariable",
    "CausalRelationship",
    "CausalEconomicGraph", 
    "VariableType",
    # Task 1.2 - Existing exports
    "CausalMechanism",
    "MechanismType",
    "EnhancedCausalRelationship",
    "create_interest_rate_mechanism",
    "create_okun_law_mechanism",
    "create_oil_shock_mechanism",
    "create_investment_returns_mechanism",
    # Task 1.3 - New exports
    "ShockEvent",
    "PropagationResults",
    "ShockPropagationEngine",
    "add_shock_propagation_capabilities",
    # Visualization exports
    "plot_causal_network",
    "plot_shock_propagation",
    "plot_mechanism_comparison",
    "create_results_dashboard",
    "quick_visualize"
]
