"""
Causal Mechanisms Implementation

This module implements sophisticated causal mechanisms for economic modeling,
providing different mathematical transformations that capture real-world
economic relationships beyond simple linear correlations.

The core innovation lies in providing mechanism types that reflect common
economic phenomena:
- LINEAR: Direct proportional effects
- EXPONENTIAL: Accelerating/decelerating effects with compounding
- THRESHOLD: Step-function effects that only activate above certain levels
- SATURATION: Diminishing returns effects following logistic-style curves

These mechanisms enable more realistic modeling of economic relationships
where effects are often non-linear, context-dependent, and subject to
various economic constraints such as policy thresholds and market saturation.

Author: Economic Analysis Team
Version: 0.1.0
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Union, Callable
import numpy as np
import math
from .causal_economic_graph import CausalRelationship


class MechanismType(Enum):
    """
    Types of causal mechanisms for economic modeling.
    
    Each mechanism type captures different economic behaviors:
    - LINEAR: Simple proportional relationships (y = strength * x)
    - EXPONENTIAL: Accelerating or decelerating effects (y = strength * x^exponent)
    - THRESHOLD: Step functions that activate above minimum levels
    - SATURATION: Diminishing returns following logistic curves
    """
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    THRESHOLD = "threshold"
    SATURATION = "saturation"


@dataclass
class CausalMechanism:
    """
    Represents a causal mechanism that transforms economic relationships.
    
    This class implements various mathematical transformations that capture
    realistic economic behaviors beyond simple linear relationships. Each
    mechanism type models specific economic phenomena observed in real markets.
    
    Attributes:
        mechanism_type (MechanismType): Type of mechanism transformation
        parameters (Dict[str, float]): Mechanism-specific parameters
        description (str): Human-readable description of the mechanism
        
    Parameter Specifications by Mechanism Type:
    
    LINEAR:
        - No additional parameters (uses base relationship strength)
        
    EXPONENTIAL:
        - exponent (float): Power exponent (>1 accelerating, <1 decelerating)
        - Default: {"exponent": 1.5}
        
    THRESHOLD:
        - threshold (float): Minimum input value for activation
        - scale_factor (float): Multiplier applied above threshold
        - Default: {"threshold": 1.0, "scale_factor": 1.0}
        
    SATURATION:
        - max_effect (float): Maximum possible output value
        - half_saturation (float): Input value at which output reaches 50% of max
        - Default: {"max_effect": 1.0, "half_saturation": 5.0}
    """
    mechanism_type: MechanismType
    parameters: Dict[str, float] = field(default_factory=dict)
    description: str = ""
    
    def __post_init__(self):
        """Initialize mechanism with default parameters and validate."""
        self._set_default_parameters()
        self.validate_parameters()
    
    def _set_default_parameters(self) -> None:
        """Set default parameters for each mechanism type."""
        defaults = {
            MechanismType.LINEAR: {},
            MechanismType.EXPONENTIAL: {"exponent": 1.5},
            MechanismType.THRESHOLD: {"threshold": 1.0, "scale_factor": 1.0},
            MechanismType.SATURATION: {"max_effect": 1.0, "half_saturation": 5.0}
        }
        
        # Only set defaults for missing parameters
        for key, value in defaults[self.mechanism_type].items():
            if key not in self.parameters:
                self.parameters[key] = value
    
    def apply_mechanism(self, input_value: float, base_strength: float) -> float:
        """
        Apply the causal mechanism to transform input value.
        
        This method implements the core transformation logic for each mechanism type,
        taking an input economic value and the base relationship strength to
        produce a transformed output that reflects the mechanism's behavior.
        
        Args:
            input_value (float): Input economic value to transform
            base_strength (float): Base causal relationship strength [-1, 1]
            
        Returns:
            float: Transformed output value
            
        Raises:
            ValueError: If input values are invalid or mechanism parameters are incorrect
        """
        if not isinstance(input_value, (int, float)):
            raise ValueError("Input value must be numeric")
        
        if not isinstance(base_strength, (int, float)):
            raise ValueError("Base strength must be numeric")
        
        if not -1 <= base_strength <= 1:
            raise ValueError("Base strength must be between -1 and 1")
        
        # Handle mechanism-specific transformations
        if self.mechanism_type == MechanismType.LINEAR:
            return self._apply_linear(input_value, base_strength)
        
        elif self.mechanism_type == MechanismType.EXPONENTIAL:
            return self._apply_exponential(input_value, base_strength)
        
        elif self.mechanism_type == MechanismType.THRESHOLD:
            return self._apply_threshold(input_value, base_strength)
        
        elif self.mechanism_type == MechanismType.SATURATION:
            return self._apply_saturation(input_value, base_strength)
        
        else:
            raise ValueError(f"Unknown mechanism type: {self.mechanism_type}")
    
    def _apply_linear(self, input_value: float, base_strength: float) -> float:
        """
        Apply linear mechanism: Simple proportional relationship.
        
        Formula: output = base_strength * input_value
        
        This represents the most basic economic relationship where effects
        are directly proportional to causes. Common in situations where
        no significant constraints or non-linearities are present.
        
        Economic Examples:
        - Direct cost pass-through in competitive markets
        - Simple tax rate changes on revenue
        - Basic supply-demand relationships in equilibrium
        """
        return base_strength * input_value
    
    def _apply_exponential(self, input_value: float, base_strength: float) -> float:
        """
        Apply exponential mechanism: Accelerating or decelerating effects.
        
        Formula: output = base_strength * sign(input_value) * |input_value|^exponent
        
        This captures economic relationships where effects compound or diminish
        at increasing rates. The exponent determines the nature of the relationship:
        - exponent > 1: Accelerating effects (super-linear growth)
        - exponent < 1: Decelerating effects (sub-linear growth)
        - exponent = 1: Reduces to linear relationship
        
        Economic Examples:
        - Network effects in technology adoption
        - Economies/diseconomies of scale
        - Crisis propagation through financial systems
        - Learning curve effects in production
        """
        exponent = self.parameters["exponent"]
        
        if input_value == 0:
            return 0.0
        
        # Preserve sign while applying exponential to absolute value
        sign = 1 if input_value >= 0 else -1
        abs_input = abs(input_value)
        
        # Apply exponential transformation
        transformed = sign * (abs_input ** exponent)
        
        return base_strength * transformed
    
    def _apply_threshold(self, input_value: float, base_strength: float) -> float:
        """
        Apply threshold mechanism: Step-function that activates above minimum levels.
        
        Formula: 
        if |input_value| < threshold: output = 0
        else: output = base_strength * scale_factor * (input_value - sign(input_value) * threshold)
        
        This models economic relationships where a minimum magnitude is required
        before any effect occurs. Common in policy interventions and market reactions
        where small changes are absorbed or ignored but larger changes trigger responses.
        
        Economic Examples:
        - Monetary policy transmission (interest rate changes need minimum magnitude)
        - Consumer behavior changes (price changes below threshold go unnoticed)
        - Market volatility triggers (small movements ignored, large ones cause reactions)
        - Regulatory compliance costs (fixed costs create effective thresholds)
        """
        threshold = self.parameters["threshold"]
        scale_factor = self.parameters["scale_factor"]
        
        if threshold < 0:
            raise ValueError("Threshold must be non-negative")
        
        # Check if absolute value is below threshold
        if abs(input_value) < threshold:
            return 0.0
        
        # Apply threshold offset and scale factor
        sign = 1 if input_value >= 0 else -1
        effective_input = input_value - (sign * threshold)
        
        return base_strength * scale_factor * effective_input
    
    def _apply_saturation(self, input_value: float, base_strength: float) -> float:
        """
        Apply saturation mechanism: Diminishing returns following logistic curves.
        
        Formula: output = base_strength * (max_effect * input_value) / (half_saturation + |input_value|)
        
        This models economic relationships where effects diminish as inputs increase,
        eventually approaching a maximum limit. The relationship follows a logistic-style
        curve that captures the common economic phenomenon of diminishing marginal returns.
        
        Parameters:
        - max_effect: Maximum possible output magnitude
        - half_saturation: Input value at which output reaches 50% of maximum
        
        Economic Examples:
        - Okun's law (unemployment-GDP relationship saturates at extreme levels)
        - Investment returns (diminishing marginal productivity of capital)
        - Market penetration (adoption rates slow as market saturates)
        - Labor productivity (diminishing returns to additional workers)
        """
        max_effect = self.parameters["max_effect"]
        half_saturation = self.parameters["half_saturation"]
        
        if half_saturation <= 0:
            raise ValueError("Half saturation must be positive")
        
        if input_value == 0:
            return 0.0
        
        # Preserve sign for negative inputs
        sign = 1 if input_value >= 0 else -1
        abs_input = abs(input_value)
        
        # Apply saturation formula (Michaelis-Menten-like kinetics)
        saturated_effect = (max_effect * abs_input) / (half_saturation + abs_input)
        
        return base_strength * sign * saturated_effect
    
    def validate_parameters(self) -> bool:
        """
        Validate mechanism parameters are economically reasonable.
        
        Checks parameter values for economic validity and mathematical consistency.
        Different mechanism types have different parameter requirements and constraints.
        
        Returns:
            bool: True if all parameters are valid
            
        Raises:
            ValueError: If any parameter is invalid for the mechanism type
        """
        if self.mechanism_type == MechanismType.LINEAR:
            # Linear mechanism requires no parameters
            return True
        
        elif self.mechanism_type == MechanismType.EXPONENTIAL:
            if "exponent" not in self.parameters:
                raise ValueError("Exponential mechanism requires 'exponent' parameter")
            
            exponent = self.parameters["exponent"]
            if not isinstance(exponent, (int, float)):
                raise ValueError("Exponent must be numeric")
            
            if exponent <= 0:
                raise ValueError("Exponent must be positive")
            
            # Economic warning for extreme exponents
            if exponent > 3.0:
                import warnings
                warnings.warn(
                    f"Exponent {exponent} > 3.0 may produce unrealistic exponential growth",
                    UserWarning
                )
        
        elif self.mechanism_type == MechanismType.THRESHOLD:
            required_params = ["threshold", "scale_factor"]
            for param in required_params:
                if param not in self.parameters:
                    raise ValueError(f"Threshold mechanism requires '{param}' parameter")
                
                value = self.parameters[param]
                if not isinstance(value, (int, float)):
                    raise ValueError(f"Parameter '{param}' must be numeric")
            
            if self.parameters["threshold"] < 0:
                raise ValueError("Threshold must be non-negative")
            
            if self.parameters["scale_factor"] <= 0:
                raise ValueError("Scale factor must be positive")
        
        elif self.mechanism_type == MechanismType.SATURATION:
            required_params = ["max_effect", "half_saturation"]
            for param in required_params:
                if param not in self.parameters:
                    raise ValueError(f"Saturation mechanism requires '{param}' parameter")
                
                value = self.parameters[param]
                if not isinstance(value, (int, float)):
                    raise ValueError(f"Parameter '{param}' must be numeric")
            
            if self.parameters["half_saturation"] <= 0:
                raise ValueError("Half saturation must be positive")
        
        else:
            raise ValueError(f"Unknown mechanism type: {self.mechanism_type}")
        
        return True
    
    def get_example_output(self, test_range: List[float]) -> List[float]:
        """
        Generate example outputs for documentation and testing.
        
        This method applies the mechanism to a range of test values using
        a standard base strength of 0.5, demonstrating the mechanism's
        behavior pattern across different input magnitudes.
        
        Args:
            test_range (List[float]): List of input values to test
            
        Returns:
            List[float]: Corresponding output values
            
        Example:
            >>> mechanism = CausalMechanism(MechanismType.LINEAR)
            >>> inputs = [0, 1, 2, 3, 4, 5]
            >>> outputs = mechanism.get_example_output(inputs)
            >>> # For linear with strength 0.5: [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
        """
        if not isinstance(test_range, list):
            raise ValueError("Test range must be a list")
        
        if not all(isinstance(x, (int, float)) for x in test_range):
            raise ValueError("All test range values must be numeric")
        
        # Use standard base strength for examples
        base_strength = 0.5
        
        outputs = []
        for input_value in test_range:
            try:
                output = self.apply_mechanism(input_value, base_strength)
                outputs.append(output)
            except (ValueError, ZeroDivisionError) as e:
                # Handle edge cases gracefully
                outputs.append(float('nan'))
        
        return outputs
    
    def __str__(self) -> str:
        """String representation of the mechanism."""
        param_str = ", ".join(f"{k}={v}" for k, v in self.parameters.items())
        return f"CausalMechanism({self.mechanism_type.value}, {param_str})"
    
    def __repr__(self) -> str:
        """Detailed representation of the mechanism."""
        return (f"CausalMechanism(mechanism_type={self.mechanism_type}, "
                f"parameters={self.parameters}, description='{self.description}')")


class EnhancedCausalRelationship:
    """
    Extended causal relationship that incorporates mechanism transformations.
    
    This class provides a composition pattern that extends the functionality
    of the base CausalRelationship without modifying the existing implementation.
    It allows for sophisticated mechanism-based transformations while maintaining
    backward compatibility with the existing system.
    
    The class acts as a wrapper that combines a base causal relationship with
    a mechanism, enabling complex economic modeling while preserving the
    architectural integrity of the original system.
    """
    
    def __init__(self, base_relationship: CausalRelationship, mechanism: CausalMechanism):
        """
        Initialize enhanced relationship with mechanism.
        
        Args:
            base_relationship (CausalRelationship): Base causal relationship
            mechanism (CausalMechanism): Mechanism for transformation
            
        Raises:
            ValueError: If inputs are not of correct types
        """
        if not isinstance(base_relationship, CausalRelationship):
            raise ValueError("base_relationship must be a CausalRelationship instance")
        
        if not isinstance(mechanism, CausalMechanism):
            raise ValueError("mechanism must be a CausalMechanism instance")
        
        self.base_relationship = base_relationship
        self.mechanism = mechanism
    
    def apply_causal_effect(self, input_value: float) -> float:
        """
        Apply the causal effect with mechanism transformation.
        
        This method combines the base relationship strength with the mechanism's
        transformation function to produce a realistic economic response that
        goes beyond simple linear relationships.
        
        Args:
            input_value (float): Input economic value
            
        Returns:
            float: Transformed output value incorporating both base strength and mechanism
            
        Example:
            >>> # Create a threshold relationship for interest rate policy
            >>> base_rel = CausalRelationship("interest_rate", "gdp_growth", -0.3, 0.8)
            >>> threshold_mech = CausalMechanism(
            ...     MechanismType.THRESHOLD,
            ...     {"threshold": 0.25, "scale_factor": 2.0}
            ... )
            >>> enhanced_rel = EnhancedCausalRelationship(base_rel, threshold_mech)
            >>> 
            >>> # Small rate change (below threshold) has no effect
            >>> enhanced_rel.apply_causal_effect(0.1)  # Returns 0.0
            >>> 
            >>> # Large rate change (above threshold) has amplified effect
            >>> enhanced_rel.apply_causal_effect(0.5)  # Returns significant negative impact
        """
        return self.mechanism.apply_mechanism(input_value, self.base_relationship.strength)
    
    @property
    def source(self) -> str:
        """Source variable name from base relationship."""
        return self.base_relationship.source
    
    @property
    def target(self) -> str:
        """Target variable name from base relationship."""
        return self.base_relationship.target
    
    @property
    def strength(self) -> float:
        """Base strength from underlying relationship."""
        return self.base_relationship.strength
    
    @property
    def confidence(self) -> float:
        """Confidence from base relationship."""
        return self.base_relationship.confidence
    
    @property
    def lag_periods(self) -> int:
        """Lag periods from base relationship."""
        return self.base_relationship.lag_periods
    
    def __str__(self) -> str:
        """String representation of enhanced relationship."""
        return (f"EnhancedCausalRelationship({self.source} -> {self.target}, "
                f"mechanism={self.mechanism.mechanism_type.value})")
    
    def __repr__(self) -> str:
        """Detailed representation of enhanced relationship."""
        return (f"EnhancedCausalRelationship(base_relationship={self.base_relationship}, "
                f"mechanism={self.mechanism})")


# Economic Example Factory Functions
def create_interest_rate_mechanism() -> CausalMechanism:
    """
    Create a threshold mechanism for interest rate policy effects.
    
    Models the empirical observation that small interest rate changes
    (< 0.25%) often have minimal immediate economic impact, while larger
    changes trigger significant responses across the economy.
    
    Returns:
        CausalMechanism: Configured threshold mechanism for interest rate effects
    """
    return CausalMechanism(
        mechanism_type=MechanismType.THRESHOLD,
        parameters={"threshold": 0.25, "scale_factor": 2.0},
        description="Interest rate policy threshold effect - small changes ignored, large changes amplified"
    )


def create_okun_law_mechanism() -> CausalMechanism:
    """
    Create a saturation mechanism for Okun's law (unemployment-GDP relationship).
    
    Models the empirical observation that the unemployment-GDP relationship
    shows diminishing effects at extreme unemployment levels, as the economy
    approaches structural unemployment limits.
    
    Returns:
        CausalMechanism: Configured saturation mechanism for Okun's law
    """
    return CausalMechanism(
        mechanism_type=MechanismType.SATURATION,
        parameters={"max_effect": -0.5, "half_saturation": 8.0},
        description="Okun's law with saturation effects at extreme unemployment levels"
    )


def create_oil_shock_mechanism() -> CausalMechanism:
    """
    Create an exponential mechanism for oil price shock propagation.
    
    Models the empirical observation that oil price shocks often have
    cascading effects through the economy that amplify over time,
    particularly during crisis periods.
    
    Returns:
        CausalMechanism: Configured exponential mechanism for oil price shocks
    """
    return CausalMechanism(
        mechanism_type=MechanismType.EXPONENTIAL,
        parameters={"exponent": 1.3},
        description="Oil price shock cascading effects through economy"
    )


def create_investment_returns_mechanism() -> CausalMechanism:
    """
    Create a saturation mechanism for investment returns.
    
    Models the diminishing marginal productivity of capital investment,
    where initial investments have high returns but additional capital
    faces decreasing marginal productivity.
    
    Returns:
        CausalMechanism: Configured saturation mechanism for investment returns
    """
    return CausalMechanism(
        mechanism_type=MechanismType.SATURATION,
        parameters={"max_effect": 0.8, "half_saturation": 10.0},
        description="Diminishing marginal productivity of capital investment"
    )
