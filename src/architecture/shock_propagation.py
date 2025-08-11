"""
Shock Propagation Engine

This module implements sophisticated counterfactual reasoning through economic shock
propagation in causal graphs. It enables "what-if" scenario analysis by simulating
how economic disturbances spread through the causal network over time.

The core innovation lies in combining:
1. Topological ordering for causal precedence
2. Time-lag modeling for realistic economic dynamics  
3. Mechanism-based transformations for non-linear effects
4. Dampening factors for stability and convergence
5. Multi-period forecasting with uncertainty propagation

This system enables economists and policy makers to understand:
- How policy interventions ripple through the economy
- The temporal dynamics of economic shocks
- Cumulative effects of sustained disturbances
- Identification of systemic vulnerabilities

Author: Economic Analysis Team
Version: 0.1.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Union
import numpy as np
from collections import defaultdict, deque
import copy
import warnings

from .causal_economic_graph import CausalEconomicGraph, EconomicVariable
from .causal_mechanisms import CausalMechanism, EnhancedCausalRelationship


@dataclass
class ShockEvent:
    """
    Represents an economic shock event for propagation analysis.
    
    This class encapsulates all information about an economic disturbance,
    including its magnitude, temporal properties, and uncertainty characteristics.
    
    Attributes:
        variable_name (str): Name of the variable receiving the shock
        magnitude (float): Shock magnitude in standard deviations
        duration (int): Number of periods the shock persists (0 = one-time shock)
        decay_rate (float): Rate at which persistent shocks decay [0, 1]
        uncertainty_multiplier (float): Factor to adjust uncertainty during shock
        description (str): Human-readable description of the shock event
    """
    variable_name: str
    magnitude: float
    duration: int = 0
    decay_rate: float = 0.0
    uncertainty_multiplier: float = 1.0
    description: str = ""
    
    def __post_init__(self):
        """Validate shock event parameters."""
        if not isinstance(self.magnitude, (int, float)):
            raise ValueError("Shock magnitude must be numeric")
        
        if self.duration < 0:
            raise ValueError("Duration must be non-negative")
        
        if not 0 <= self.decay_rate <= 1:
            raise ValueError("Decay rate must be between 0 and 1")
        
        if self.uncertainty_multiplier < 0:
            raise ValueError("Uncertainty multiplier must be non-negative")
    
    def get_shock_at_period(self, period: int) -> float:
        """
        Calculate the shock magnitude at a specific period.
        
        For one-time shocks (duration=0), returns magnitude only at period 0.
        For persistent shocks, applies exponential decay over time.
        
        Args:
            period (int): Time period (0-indexed)
            
        Returns:
            float: Shock magnitude at the specified period
        """
        if period < 0:
            return 0.0
        
        # One-time shock
        if self.duration == 0:
            return self.magnitude if period == 0 else 0.0
        
        # Persistent shock with decay
        if period <= self.duration:
            decay_factor = (1 - self.decay_rate) ** period
            return self.magnitude * decay_factor
        
        return 0.0


@dataclass
class PropagationResults:
    """
    Container for shock propagation simulation results.
    
    This class stores the complete time-series output of a shock propagation
    simulation, including variable trajectories, uncertainty bounds, and
    metadata about the simulation configuration.
    
    Attributes:
        time_series (Dict[str, List[float]]): Variable values over time
        uncertainty_series (Dict[str, List[float]]): Uncertainty bounds over time
        shock_event (ShockEvent): Original shock that was propagated
        num_periods (int): Number of time periods simulated
        dampening_factor (float): Dampening factor used in simulation
        convergence_achieved (bool): Whether system reached equilibrium
        metadata (Dict[str, Any]): Additional simulation information
    """
    time_series: Dict[str, List[float]] = field(default_factory=dict)
    uncertainty_series: Dict[str, List[float]] = field(default_factory=dict)
    shock_event: Optional[ShockEvent] = None
    num_periods: int = 0
    dampening_factor: float = 0.95
    convergence_achieved: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_variable_trajectory(self, variable_name: str) -> Optional[List[float]]:
        """Get the complete trajectory for a specific variable."""
        return self.time_series.get(variable_name)
    
    def get_final_values(self) -> Dict[str, float]:
        """Get the final values for all variables."""
        return {var: series[-1] for var, series in self.time_series.items() if series}
    
    def get_peak_effects(self) -> Dict[str, Tuple[float, int]]:
        """
        Get the peak effect magnitude and timing for each variable.
        
        Returns:
            Dict[str, Tuple[float, int]]: Mapping of variable -> (peak_value, peak_period)
        """
        peak_effects = {}
        for var, series in self.time_series.items():
            if not series:
                continue
            
            # Find peak absolute deviation from initial value
            initial_value = series[0]
            deviations = [abs(val - initial_value) for val in series]
            peak_idx = deviations.index(max(deviations))
            peak_effects[var] = (series[peak_idx], peak_idx)
        
        return peak_effects
    
    def calculate_cumulative_impact(self, variable_name: str) -> float:
        """
        Calculate the cumulative impact of the shock on a variable.
        
        This measures the total area under the curve of deviations from
        the initial value, providing a sense of the overall economic impact.
        
        Args:
            variable_name (str): Name of the variable
            
        Returns:
            float: Cumulative impact measure
        """
        series = self.time_series.get(variable_name)
        if not series or len(series) < 2:
            return 0.0
        
        initial_value = series[0]
        cumulative_impact = sum(abs(val - initial_value) for val in series[1:])
        return cumulative_impact


class ShockPropagationEngine:
    """
    Advanced shock propagation engine for economic scenario analysis.
    
    This class implements sophisticated counterfactual reasoning by simulating
    how economic shocks propagate through causal networks over time. It handles
    complex dynamics including temporal lags, non-linear mechanisms, and
    stability considerations.
    
    Key Features:
    1. Topological Precedence: Respects causal ordering during propagation
    2. Temporal Dynamics: Handles multi-period lags between causes and effects
    3. Mechanism Integration: Applies sophisticated causal mechanisms
    4. Stability Control: Includes dampening to prevent unrealistic explosions
    5. Uncertainty Tracking: Propagates uncertainty through the system
    """
    
    def __init__(self, causal_graph: CausalEconomicGraph):
        """
        Initialize the shock propagation engine.
        
        Args:
            causal_graph (CausalEconomicGraph): The causal graph to propagate through
            
        Raises:
            ValueError: If the causal graph is invalid for propagation
        """
        if not isinstance(causal_graph, CausalEconomicGraph):
            raise ValueError("Must provide a valid CausalEconomicGraph instance")
        
        # Validate graph structure
        is_valid, issues = causal_graph.validate_dag_structure()
        if not is_valid:
            raise ValueError(f"Invalid causal graph structure: {issues}")
        
        self.graph = causal_graph
        self._topological_order = None
        self._enhanced_relationships = {}
        
        # Cache topological order for efficiency
        self._compute_topological_order()
    
    def _compute_topological_order(self) -> None:
        """Compute and cache the topological ordering of variables."""
        self._topological_order = self.graph.get_topological_order()
    
    def add_enhanced_relationship(self, source: str, target: str, 
                                mechanism: CausalMechanism) -> None:
        """
        Add an enhanced relationship with a specific mechanism.
        
        This allows upgrading basic causal relationships to use sophisticated
        mechanisms for more realistic shock propagation.
        
        Args:
            source (str): Source variable name
            target (str): Target variable name
            mechanism (CausalMechanism): Mechanism to apply to the relationship
            
        Raises:
            ValueError: If the relationship doesn't exist in the base graph
        """
        base_relationship = self.graph.get_relationship(source, target)
        if base_relationship is None:
            raise ValueError(f"No relationship exists from {source} to {target}")
        
        enhanced_rel = EnhancedCausalRelationship(base_relationship, mechanism)
        self._enhanced_relationships[(source, target)] = enhanced_rel
    
    def propagate_shock(self, shock: ShockEvent, num_periods: int = 12, 
                       dampening_factor: float = 0.95,
                       convergence_threshold: float = 1e-6) -> PropagationResults:
        """
        Propagate an economic shock through the causal graph.
        
        This is the core method that simulates how an economic disturbance
        spreads through the causal network over time, producing a complete
        time-series forecast for all variables in the system.
        
        Args:
            shock (ShockEvent): The shock event to propagate
            num_periods (int): Number of time periods to simulate
            dampening_factor (float): Stability dampening factor [0, 1]
            convergence_threshold (float): Threshold for convergence detection
            
        Returns:
            PropagationResults: Complete simulation results with time series
            
        Raises:
            ValueError: If shock variable doesn't exist or parameters are invalid
        """
        # Validate inputs
        if shock.variable_name not in self.graph.variables:
            raise ValueError(f"Shock variable '{shock.variable_name}' not found in graph")
        
        if num_periods <= 0:
            raise ValueError("Number of periods must be positive")
        
        if not 0 < dampening_factor <= 1:
            raise ValueError("Dampening factor must be between 0 and 1")
        
        # Initialize results container
        results = PropagationResults(
            shock_event=shock,
            num_periods=num_periods,
            dampening_factor=dampening_factor
        )
        
        # Initialize variable states
        current_values = {}
        current_uncertainties = {}
        
        for var_name, variable in self.graph.variables.items():
            current_values[var_name] = variable.current_value
            current_uncertainties[var_name] = variable.uncertainty
            results.time_series[var_name] = [variable.current_value]
            results.uncertainty_series[var_name] = [variable.uncertainty]
        
        # Create lag buffers for temporal dynamics
        lag_buffers = self._initialize_lag_buffers()
        
        # Propagation loop
        converged = False
        for period in range(1, num_periods + 1):
            # Apply direct shock to target variable
            shock_magnitude = shock.get_shock_at_period(period - 1)
            if shock_magnitude != 0:
                shocked_variable = self.graph.variables[shock.variable_name]
                shock_value = shock_magnitude * shocked_variable.uncertainty
                current_values[shock.variable_name] += shock_value
                current_uncertainties[shock.variable_name] *= shock.uncertainty_multiplier
            
            # Prepare for this period's propagation
            period_changes = defaultdict(float)
            period_uncertainty_changes = defaultdict(float)
            
            # Process variables in topological order
            for var_name in self._topological_order:
                # Get all causal influences on this variable
                causal_effects = self._calculate_causal_effects(
                    var_name, current_values, lag_buffers, period
                )
                
                # Accumulate effects
                total_effect = sum(causal_effects.values())
                period_changes[var_name] += total_effect
                
                # Update uncertainty (simplified propagation)
                if total_effect != 0:
                    base_uncertainty = current_uncertainties[var_name]
                    effect_uncertainty = abs(total_effect) * 0.1  # 10% of effect magnitude
                    period_uncertainty_changes[var_name] += effect_uncertainty
            
            # Apply dampening and update values
            previous_values = current_values.copy()
            for var_name in current_values:
                # Apply dampening to prevent explosion
                damped_change = period_changes[var_name] * dampening_factor
                current_values[var_name] += damped_change
                
                # Update uncertainty
                current_uncertainties[var_name] += period_uncertainty_changes[var_name]
                current_uncertainties[var_name] *= dampening_factor  # Uncertainty also decays
                
                # Enforce variable bounds if specified
                variable = self.graph.variables[var_name]
                if variable.bounds[0] is not None:
                    current_values[var_name] = max(current_values[var_name], variable.bounds[0])
                if variable.bounds[1] is not None:
                    current_values[var_name] = min(current_values[var_name], variable.bounds[1])
            
            # Store results for this period
            for var_name in current_values:
                results.time_series[var_name].append(current_values[var_name])
                results.uncertainty_series[var_name].append(current_uncertainties[var_name])
            
            # Update lag buffers
            self._update_lag_buffers(lag_buffers, current_values, previous_values)
            
            # Check for convergence
            if period > 3:  # Only check after a few periods
                max_change = max(abs(period_changes[var]) for var in period_changes)
                if max_change < convergence_threshold:
                    converged = True
                    results.convergence_achieved = True
                    break
        
        # Add metadata
        results.metadata = {
            'total_variables': len(self.graph.variables),
            'total_relationships': len(self.graph.relationships),
            'enhanced_relationships': len(self._enhanced_relationships),
            'periods_to_convergence': period if converged else num_periods,
            'max_shock_magnitude': shock.magnitude,
            'shock_duration': shock.duration
        }
        
        return results
    
    def _initialize_lag_buffers(self) -> Dict[Tuple[str, str], deque]:
        """
        Initialize lag buffers for temporal dynamics.
        
        Returns:
            Dict[Tuple[str, str], deque]: Lag buffers for each relationship
        """
        lag_buffers = {}
        
        for (source, target), relationship in self.graph.relationships.items():
            if relationship.lag_periods > 0:
                # Initialize with current source value
                source_value = self.graph.variables[source].current_value
                buffer = deque([source_value] * relationship.lag_periods, 
                             maxlen=relationship.lag_periods)
                lag_buffers[(source, target)] = buffer
        
        return lag_buffers
    
    def _update_lag_buffers(self, lag_buffers: Dict[Tuple[str, str], deque],
                          current_values: Dict[str, float],
                          previous_values: Dict[str, float]) -> None:
        """Update lag buffers with new values."""
        for (source, target), buffer in lag_buffers.items():
            # Add the change in source value to the buffer
            value_change = current_values[source] - previous_values[source]
            if len(buffer) > 0:
                # Add change to the most recent value in buffer
                buffer[-1] += value_change
            buffer.append(current_values[source])
    
    def _calculate_causal_effects(self, target_var: str, current_values: Dict[str, float],
                                lag_buffers: Dict[Tuple[str, str], deque],
                                period: int) -> Dict[str, float]:
        """
        Calculate all causal effects on a target variable for the current period.
        
        Args:
            target_var (str): Target variable name
            current_values (Dict[str, float]): Current values of all variables
            lag_buffers (Dict[Tuple[str, str], deque]): Lag buffers for relationships
            period (int): Current time period
            
        Returns:
            Dict[str, float]: Effects from each source variable
        """
        effects = {}
        
        # Get all direct causes of this variable
        direct_causes = self.graph.get_direct_causes(target_var)
        
        for source_var, relationship in direct_causes:
            # Determine effective input value considering lags
            if relationship.lag_periods == 0:
                # No lag - use current value
                effective_input = current_values[source_var]
            else:
                # Use lagged value from buffer
                buffer = lag_buffers.get((source_var, target_var))
                if buffer and len(buffer) > 0:
                    effective_input = buffer[0]  # Oldest value in buffer
                else:
                    effective_input = self.graph.variables[source_var].current_value
            
            # Calculate the causal effect
            if (source_var, target_var) in self._enhanced_relationships:
                # Use enhanced relationship with mechanism
                enhanced_rel = self._enhanced_relationships[(source_var, target_var)]
                effect = enhanced_rel.apply_causal_effect(effective_input)
            else:
                # Use basic linear relationship
                effect = relationship.strength * effective_input
            
            effects[source_var] = effect
        
        return effects


# Integration function to extend CausalEconomicGraph
def add_shock_propagation_capabilities(graph: CausalEconomicGraph) -> None:
    """
    Extend a CausalEconomicGraph with shock propagation capabilities.
    
    This function adds shock propagation methods directly to an existing
    CausalEconomicGraph instance, maintaining backward compatibility while
    providing advanced counterfactual reasoning capabilities.
    
    Args:
        graph (CausalEconomicGraph): The graph to extend with shock propagation
        
    Example:
        >>> graph = CausalEconomicGraph()
        >>> # ... add variables and relationships ...
        >>> add_shock_propagation_capabilities(graph)
        >>> shock = ShockEvent("federal_funds_rate", magnitude=2.0)
        >>> results = graph.propagate_shock(shock)
    """
    # Create the shock propagation engine
    engine = ShockPropagationEngine(graph)
    
    # Add methods to the graph instance
    def propagate_shock(shock: ShockEvent, num_periods: int = 12, 
                       dampening_factor: float = 0.95,
                       convergence_threshold: float = 1e-6) -> PropagationResults:
        """Propagate an economic shock through the causal graph."""
        return engine.propagate_shock(shock, num_periods, dampening_factor, convergence_threshold)
    
    def add_enhanced_relationship(source: str, target: str, mechanism: CausalMechanism) -> None:
        """Add an enhanced relationship with sophisticated mechanism."""
        return engine.add_enhanced_relationship(source, target, mechanism)
    
    def analyze_sensitivity(shock: ShockEvent, magnitude_range: List[float] = None,
                          dampening_range: List[float] = None, num_periods: int = 12) -> Dict[str, Any]:
        """Perform sensitivity analysis on shock propagation."""
        return engine.analyze_sensitivity(shock, magnitude_range, dampening_range, num_periods)
    
    def identify_systemic_risks(standard_shock_magnitude: float = 1.0,
                              num_periods: int = 12) -> Dict[str, Any]:
        """Identify systemic risks by testing shocks to each variable."""
        return engine.identify_systemic_risks(standard_shock_magnitude, num_periods)
    
    # Attach methods to the graph instance
    graph.propagate_shock = propagate_shock
    graph.add_enhanced_relationship = add_enhanced_relationship
    graph.analyze_sensitivity = analyze_sensitivity
    graph.identify_systemic_risks = identify_systemic_risks
    graph._shock_engine = engine  # Store reference for advanced usage
