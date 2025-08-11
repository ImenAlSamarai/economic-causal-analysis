"""
Causal Economic Graph Implementation

This module implements a sophisticated causal graph system for economic scenario analysis.
The core innovation lies in representing economic relationships as a directed acyclic graph (DAG)
where nodes represent economic variables and edges represent causal relationships with
quantified strength, confidence, and temporal lag properties.

The system enables:
1. Modeling complex economic interdependencies
2. Scenario propagation through causal chains
3. Uncertainty quantification in economic relationships
4. Temporal lag modeling for realistic economic dynamics
5. Validation of causal assumptions through DAG structure enforcement

Author: Economic Analysis Team
Version: 0.1.0
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any
import networkx as nx
from collections import defaultdict
import logging


class VariableType(Enum):
    """
    Classification of economic variables based on their nature and controllability.
    
    This taxonomy is crucial for understanding how variables behave in economic models:
    - EXOGENOUS: External factors not determined within the model (e.g., oil prices, natural disasters)
    - ENDOGENOUS: Internal variables determined by model relationships (e.g., GDP, inflation)
    - POLICY: Variables controlled by policy makers (e.g., interest rates, tax rates)
    - MARKET: Variables determined by market forces (e.g., stock prices, exchange rates)
    - INDICATOR: Derived metrics that summarize economic conditions (e.g., economic indices)
    """
    EXOGENOUS = "exogenous"    # External factors
    ENDOGENOUS = "endogenous"  # Model-determined variables
    POLICY = "policy"          # Policy-controlled variables
    MARKET = "market"          # Market-determined variables
    INDICATOR = "indicator"    # Derived/calculated metrics


@dataclass
class EconomicVariable:
    """
    Represents an economic variable in the causal graph.
    
    This class encapsulates all relevant information about an economic variable,
    including its current state, uncertainty, and metadata necessary for
    causal modeling and scenario analysis.
    
    Attributes:
        name (str): Unique identifier for the variable
        variable_type (VariableType): Classification of the variable
        current_value (float): Current numerical value
        uncertainty (float): Standard deviation or confidence interval width
        description (str): Human-readable description
        unit (str): Measurement unit (e.g., "USD", "percentage", "index")
        bounds (Tuple[float, float]): Valid range for the variable
        metadata (Dict[str, Any]): Additional properties for extensibility
    """
    name: str
    variable_type: VariableType
    current_value: float
    uncertainty: float
    description: str
    unit: str = ""
    bounds: Tuple[Optional[float], Optional[float]] = (None, None)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate variable constraints after initialization."""
        if self.uncertainty < 0:
            raise ValueError("Uncertainty must be non-negative")
        
        if self.bounds[0] is not None and self.current_value < self.bounds[0]:
            raise ValueError(f"Current value {self.current_value} below lower bound {self.bounds[0]}")
        
        if self.bounds[1] is not None and self.current_value > self.bounds[1]:
            raise ValueError(f"Current value {self.current_value} above upper bound {self.bounds[1]}")
    
    def is_within_bounds(self, value: float) -> bool:
        """Check if a value is within the variable's bounds."""
        lower, upper = self.bounds
        if lower is not None and value < lower:
            return False
        if upper is not None and value > upper:
            return False
        return True


@dataclass
class CausalRelationship:
    """
    Represents a causal relationship between two economic variables.
    
    This class models the causal edge in our economic DAG, capturing not just
    the existence of a relationship but its quantitative properties that are
    essential for realistic economic modeling.
    
    Attributes:
        source (str): Name of the causing variable
        target (str): Name of the affected variable
        strength (float): Causal effect magnitude [-1, 1] where:
                         - Positive values indicate positive correlation
                         - Negative values indicate negative correlation
                         - Magnitude indicates effect size
        confidence (float): Confidence in the relationship [0, 1]
        lag_periods (int): Number of time periods for effect propagation
        relationship_type (str): Type of relationship (linear, exponential, etc.)
        conditions (Dict[str, Any]): Contextual conditions affecting the relationship
    """
    source: str
    target: str
    strength: float
    confidence: float
    lag_periods: int = 0
    relationship_type: str = "linear"
    conditions: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate relationship constraints."""
        if not -1 <= self.strength <= 1:
            raise ValueError("Strength must be between -1 and 1")
        
        if not 0 <= self.confidence <= 1:
            raise ValueError("Confidence must be between 0 and 1")
        
        if self.lag_periods < 0:
            raise ValueError("Lag periods must be non-negative")
    
    @property
    def effect_magnitude(self) -> float:
        """Calculate the effective strength considering confidence."""
        return abs(self.strength) * self.confidence


class CausalEconomicGraph:
    """
    A sophisticated causal graph system for economic scenario analysis.
    
    This class implements the core innovation of representing economic systems
    as directed acyclic graphs where:
    - Nodes represent economic variables with uncertainty quantification
    - Edges represent causal relationships with strength and temporal properties
    - The DAG structure enforces causal consistency and enables scenario propagation
    
    Key Features:
    1. DAG Structure Enforcement: Prevents circular causality
    2. Uncertainty Propagation: Tracks how uncertainty flows through causal chains
    3. Temporal Modeling: Handles time lags in economic relationships
    4. Scenario Analysis: Enables "what-if" analysis through graph traversal
    5. Validation Framework: Ensures economic and mathematical consistency
    
    The system supports both static analysis (current state) and dynamic
    scenario modeling (propagation of changes through the economic network).
    """
    
    def __init__(self):
        """Initialize an empty causal economic graph."""
        self.graph = nx.DiGraph()
        self.variables: Dict[str, EconomicVariable] = {}
        self.relationships: Dict[Tuple[str, str], CausalRelationship] = {}
        self._logger = logging.getLogger(__name__)
    
    def add_variable(self, variable: EconomicVariable) -> None:
        """
        Add an economic variable to the graph.
        
        Args:
            variable (EconomicVariable): The variable to add
            
        Raises:
            ValueError: If variable name already exists
        """
        if variable.name in self.variables:
            raise ValueError(f"Variable '{variable.name}' already exists")
        
        self.variables[variable.name] = variable
        self.graph.add_node(variable.name, **{
            'variable_type': variable.variable_type,
            'current_value': variable.current_value,
            'uncertainty': variable.uncertainty,
            'description': variable.description,
            'unit': variable.unit,
            'bounds': variable.bounds
        })
        
        self._logger.info(f"Added variable: {variable.name} ({variable.variable_type.value})")
    
    def add_relationship(self, relationship: CausalRelationship) -> None:
        """
        Add a causal relationship between variables.
        
        Args:
            relationship (CausalRelationship): The relationship to add
            
        Raises:
            ValueError: If variables don't exist or relationship creates cycle
        """
        # Validate that both variables exist
        if relationship.source not in self.variables:
            raise ValueError(f"Source variable '{relationship.source}' does not exist")
        
        if relationship.target not in self.variables:
            raise ValueError(f"Target variable '{relationship.target}' does not exist")
        
        # Prevent self-loops
        if relationship.source == relationship.target:
            raise ValueError("Self-loops are not allowed in causal relationships")
        
        # Check for cycle creation
        if self._would_create_cycle(relationship.source, relationship.target):
            raise ValueError(
                f"Adding relationship from '{relationship.source}' to '{relationship.target}' "
                "would create a cycle in the causal graph"
            )
        
        # Add the relationship
        edge_key = (relationship.source, relationship.target)
        self.relationships[edge_key] = relationship
        
        self.graph.add_edge(
            relationship.source,
            relationship.target,
            strength=relationship.strength,
            confidence=relationship.confidence,
            lag_periods=relationship.lag_periods,
            relationship_type=relationship.relationship_type,
            conditions=relationship.conditions
        )
        
        self._logger.info(
            f"Added relationship: {relationship.source} -> {relationship.target} "
            f"(strength: {relationship.strength}, confidence: {relationship.confidence})"
        )
    
    def _would_create_cycle(self, source: str, target: str) -> bool:
        """
        Check if adding an edge would create a cycle.
        
        Args:
            source (str): Source variable name
            target (str): Target variable name
            
        Returns:
            bool: True if adding the edge would create a cycle
        """
        # Temporarily add the edge
        temp_graph = self.graph.copy()
        temp_graph.add_edge(source, target)
        
        # Check if the resulting graph has cycles
        return not nx.is_directed_acyclic_graph(temp_graph)
    
    def validate_dag_structure(self) -> Tuple[bool, List[str]]:
        """
        Validate the DAG structure and return validation results.
        
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_issues)
        """
        issues = []
        
        # Check if graph is a DAG
        if not nx.is_directed_acyclic_graph(self.graph):
            cycles = list(nx.simple_cycles(self.graph))
            issues.append(f"Graph contains cycles: {cycles}")
        
        # Check for isolated nodes
        isolated = list(nx.isolates(self.graph))
        if isolated:
            issues.append(f"Isolated variables (no causal relationships): {isolated}")
        
        # Validate variable consistency
        for name, variable in self.variables.items():
            if name not in self.graph.nodes:
                issues.append(f"Variable '{name}' not in graph nodes")
        
        # Validate relationship consistency
        for (source, target), relationship in self.relationships.items():
            if not self.graph.has_edge(source, target):
                issues.append(f"Relationship {source}->{target} not in graph edges")
        
        is_valid = len(issues) == 0
        return is_valid, issues
    
    def get_variable(self, name: str) -> Optional[EconomicVariable]:
        """Get a variable by name."""
        return self.variables.get(name)
    
    def get_relationship(self, source: str, target: str) -> Optional[CausalRelationship]:
        """Get a relationship by source and target variable names."""
        return self.relationships.get((source, target))
    
    def get_causal_ancestors(self, variable_name: str) -> Set[str]:
        """
        Get all variables that causally influence the given variable.
        
        Args:
            variable_name (str): Name of the target variable
            
        Returns:
            Set[str]: Set of ancestor variable names
        """
        if variable_name not in self.graph.nodes:
            raise ValueError(f"Variable '{variable_name}' not found")
        
        return set(nx.ancestors(self.graph, variable_name))
    
    def get_causal_descendants(self, variable_name: str) -> Set[str]:
        """
        Get all variables that are causally influenced by the given variable.
        
        Args:
            variable_name (str): Name of the source variable
            
        Returns:
            Set[str]: Set of descendant variable names
        """
        if variable_name not in self.graph.nodes:
            raise ValueError(f"Variable '{variable_name}' not found")
        
        return set(nx.descendants(self.graph, variable_name))
    
    def get_direct_effects(self, variable_name: str) -> List[Tuple[str, CausalRelationship]]:
        """
        Get direct causal effects from a variable.
        
        Args:
            variable_name (str): Name of the source variable
            
        Returns:
            List[Tuple[str, CausalRelationship]]: List of (target, relationship) pairs
        """
        if variable_name not in self.graph.nodes:
            raise ValueError(f"Variable '{variable_name}' not found")
        
        effects = []
        for target in self.graph.successors(variable_name):
            relationship = self.get_relationship(variable_name, target)
            if relationship:
                effects.append((target, relationship))
        
        return effects
    
    def get_direct_causes(self, variable_name: str) -> List[Tuple[str, CausalRelationship]]:
        """
        Get direct causal influences on a variable.
        
        Args:
            variable_name (str): Name of the target variable
            
        Returns:
            List[Tuple[str, CausalRelationship]]: List of (source, relationship) pairs
        """
        if variable_name not in self.graph.nodes:
            raise ValueError(f"Variable '{variable_name}' not found")
        
        causes = []
        for source in self.graph.predecessors(variable_name):
            relationship = self.get_relationship(source, variable_name)
            if relationship:
                causes.append((source, relationship))
        
        return causes
    
    def get_topological_order(self) -> List[str]:
        """
        Get variables in topological order for scenario propagation.
        
        Returns:
            List[str]: Variables ordered such that all causes precede effects
        """
        return list(nx.topological_sort(self.graph))
    
    def get_summary_statistics(self) -> Dict[str, Any]:
        """
        Get summary statistics about the causal graph.
        
        Returns:
            Dict[str, Any]: Summary statistics
        """
        return {
            'num_variables': len(self.variables),
            'num_relationships': len(self.relationships),
            'is_dag': nx.is_directed_acyclic_graph(self.graph),
            'num_connected_components': nx.number_weakly_connected_components(self.graph),
            'density': nx.density(self.graph),
            'variable_types': {
                vtype.value: sum(1 for v in self.variables.values() if v.variable_type == vtype)
                for vtype in VariableType
            }
        }
    
    def __repr__(self) -> str:
        """String representation of the causal graph."""
        stats = self.get_summary_statistics()
        return (
            f"CausalEconomicGraph("
            f"variables={stats['num_variables']}, "
            f"relationships={stats['num_relationships']}, "
            f"is_dag={stats['is_dag']})"
        )
