"""
Economic Analysis Visualization Module

This module provides essential visualization capabilities for the Economic Causal Analysis System,
enabling clear presentation of causal relationships, shock propagation results, and mechanism behavior.

Key Features:
- Causal graph network visualization
- Shock propagation time series plots
- Mechanism comparison charts
- Economic dashboard summaries

Author: Economic Analysis Team
Version: 0.1.0
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import networkx as nx
from matplotlib.patches import FancyBboxPatch

from .causal_economic_graph import CausalEconomicGraph, VariableType
from .shock_propagation import PropagationResults


def plot_causal_network(graph: CausalEconomicGraph, figsize: Tuple[int, int] = (12, 8), 
                       save_path: Optional[str] = None) -> None:
    """
    Visualize the causal economic network with colored nodes and weighted edges.
    
    Args:
        graph: CausalEconomicGraph instance to visualize
        figsize: Figure size (width, height)
        save_path: Optional path to save the plot
    """
    plt.figure(figsize=figsize)
    
    # Color mapping for variable types
    type_colors = {
        VariableType.EXOGENOUS: '#FF6B6B',    # Red - external factors
        VariableType.ENDOGENOUS: '#4ECDC4',   # Teal - internal variables  
        VariableType.POLICY: '#45B7D1',       # Blue - policy variables
        VariableType.MARKET: '#96CEB4',       # Green - market variables
        VariableType.INDICATOR: '#FFEAA7'     # Yellow - indicators
    }
    
    # Get node colors
    node_colors = [type_colors.get(graph.variables[node].variable_type, '#95A5A6') 
                   for node in graph.graph.nodes()]
    
    # Position nodes using spring layout
    pos = nx.spring_layout(graph.graph, k=3, iterations=50, seed=42)
    
    # Draw nodes
    nx.draw_networkx_nodes(graph.graph, pos, node_color=node_colors, 
                          node_size=2000, alpha=0.8)
    
    # Draw edges with thickness based on strength
    edges = graph.graph.edges(data=True)
    edge_weights = [abs(edge[2].get('strength', 0.5)) * 5 for edge in edges]
    nx.draw_networkx_edges(graph.graph, pos, width=edge_weights, 
                          alpha=0.6, edge_color='#7F8C8D')
    
    # Draw labels
    nx.draw_networkx_labels(graph.graph, pos, font_size=10, font_weight='bold')
    
    # Create legend
    legend_elements = [plt.scatter([], [], c=color, s=100, label=vtype.value.title()) 
                      for vtype, color in type_colors.items()]
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
    
    plt.title('Economic Causal Network', size=16, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_shock_propagation(results: PropagationResults, variables: Optional[List[str]] = None,
                          figsize: Tuple[int, int] = (14, 8), save_path: Optional[str] = None) -> None:
    """
    Plot time series of shock propagation through the economic system.
    
    Args:
        results: PropagationResults from shock simulation
        variables: List of variables to plot (None = plot all)
        figsize: Figure size (width, height)  
        save_path: Optional path to save the plot
    """
    plt.figure(figsize=figsize)
    
    # Select variables to plot
    if variables is None:
        variables = list(results.time_series.keys())[:5]  # Limit to 5 for clarity
    
    # Color palette
    colors = plt.cm.Set1(np.linspace(0, 1, len(variables)))
    
    # Plot time series
    for i, var in enumerate(variables):
        if var in results.time_series:
            series = results.time_series[var]
            periods = list(range(len(series)))
            
            plt.plot(periods, series, color=colors[i], linewidth=2.5, 
                    marker='o', markersize=4, label=var.replace('_', ' ').title())
            
            # Add uncertainty bands if available
            if var in results.uncertainty_series:
                uncertainty = results.uncertainty_series[var]
                plt.fill_between(periods, 
                               [series[j] - uncertainty[j] for j in range(len(series))],
                               [series[j] + uncertainty[j] for j in range(len(series))],
                               alpha=0.2, color=colors[i])
    
    # Highlight shock period
    plt.axvline(x=0, color='red', linestyle='--', alpha=0.7, linewidth=2, label='Shock Event')
    
    # Formatting
    plt.xlabel('Time Periods', fontsize=12, fontweight='bold')
    plt.ylabel('Variable Values', fontsize=12, fontweight='bold') 
    plt.title(f'Economic Shock Propagation Analysis\n{results.shock_event.description}', 
             fontsize=14, fontweight='bold', pad=20)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_mechanism_comparison(input_range: List[float] = None, 
                            figsize: Tuple[int, int] = (12, 8),
                            save_path: Optional[str] = None) -> None:
    """
    Compare different causal mechanisms on the same input range.
    
    Args:
        input_range: Range of input values to test
        figsize: Figure size (width, height)
        save_path: Optional path to save the plot
    """
    if input_range is None:
        input_range = list(np.linspace(0, 5, 50))
    
    # Import here to avoid circular imports
    from .causal_mechanisms import CausalMechanism, MechanismType
    
    plt.figure(figsize=figsize)
    
    # Define mechanisms to compare
    mechanisms = {
        'Linear': CausalMechanism(MechanismType.LINEAR),
        'Exponential': CausalMechanism(MechanismType.EXPONENTIAL, {'exponent': 1.3}),
        'Threshold': CausalMechanism(MechanismType.THRESHOLD, {'threshold': 1.0, 'scale_factor': 2.0}),
        'Saturation': CausalMechanism(MechanismType.SATURATION, {'max_effect': 2.0, 'half_saturation': 2.0})
    }
    
    colors = ['#3498DB', '#E74C3C', '#F39C12', '#27AE60']
    
    # Plot each mechanism
    for i, (name, mechanism) in enumerate(mechanisms.items()):
        outputs = []
        for input_val in input_range:
            try:
                output = mechanism.apply_mechanism(input_val, 0.5)  # Base strength 0.5
                outputs.append(output)
            except:
                outputs.append(np.nan)
        
        plt.plot(input_range, outputs, color=colors[i], linewidth=3, 
                label=name, marker='o', markersize=3, alpha=0.8)
    
    plt.xlabel('Input Value', fontsize=12, fontweight='bold')
    plt.ylabel('Output Value', fontsize=12, fontweight='bold')
    plt.title('Causal Mechanism Comparison\n(Base Strength = 0.5)', 
             fontsize=14, fontweight='bold', pad=20)
    plt.legend(fontsize=11, loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def create_results_dashboard(results: PropagationResults, graph: CausalEconomicGraph,
                           figsize: Tuple[int, int] = (16, 10), 
                           save_path: Optional[str] = None) -> None:
    """
    Create a comprehensive dashboard showing key results and insights.
    
    Args:
        results: PropagationResults from shock simulation
        graph: Original CausalEconomicGraph
        figsize: Figure size (width, height)
        save_path: Optional path to save the plot
    """
    fig = plt.figure(figsize=figsize)
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. Network plot (top left)
    ax1 = fig.add_subplot(gs[0, 0])
    plt.sca(ax1)
    
    # Simplified network
    type_colors = {
        VariableType.EXOGENOUS: '#FF6B6B',
        VariableType.ENDOGENOUS: '#4ECDC4', 
        VariableType.POLICY: '#45B7D1',
        VariableType.MARKET: '#96CEB4',
        VariableType.INDICATOR: '#FFEAA7'
    }
    
    node_colors = [type_colors.get(graph.variables[node].variable_type, '#95A5A6') 
                   for node in graph.graph.nodes()]
    pos = nx.spring_layout(graph.graph, k=1, iterations=30, seed=42)
    nx.draw_networkx_nodes(graph.graph, pos, node_color=node_colors, node_size=300, alpha=0.8)
    nx.draw_networkx_edges(graph.graph, pos, alpha=0.5, width=1)
    nx.draw_networkx_labels(graph.graph, pos, font_size=8)
    ax1.set_title('Causal Network', fontweight='bold', fontsize=10)
    ax1.axis('off')
    
    # 2. Time series (top center and right)
    ax2 = fig.add_subplot(gs[0, 1:])
    plt.sca(ax2)
    
    # Plot key variables
    key_vars = list(results.time_series.keys())[:4]
    colors = plt.cm.Set1(np.linspace(0, 1, len(key_vars)))
    
    for i, var in enumerate(key_vars):
        if var in results.time_series:
            series = results.time_series[var]
            periods = list(range(len(series)))
            plt.plot(periods, series, color=colors[i], linewidth=2, 
                    marker='o', markersize=3, label=var.replace('_', ' ').title())
    
    plt.axvline(x=0, color='red', linestyle='--', alpha=0.7, linewidth=1, label='Shock')
    plt.xlabel('Periods', fontsize=9)
    plt.ylabel('Values', fontsize=9)
    plt.title('Shock Propagation Over Time', fontweight='bold', fontsize=10)
    plt.legend(fontsize=8)
    plt.grid(True, alpha=0.3)
    
    # 3. Peak effects (middle left)
    ax3 = fig.add_subplot(gs[1, 0])
    plt.sca(ax3)
    
    peak_effects = results.get_peak_effects()
    vars_list = list(peak_effects.keys())[:5]
    peak_values = [abs(peak_effects[var][0] - results.time_series[var][0]) for var in vars_list]
    
    bars = plt.barh(range(len(vars_list)), peak_values, color=plt.cm.Reds(np.linspace(0.4, 0.8, len(vars_list))))
    plt.yticks(range(len(vars_list)), [v.replace('_', ' ').title() for v in vars_list], fontsize=8)
    plt.xlabel('Peak Impact', fontsize=9)
    plt.title('Peak Effects', fontweight='bold', fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # 4. Key metrics (middle center)
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    
    # Create metrics box
    metrics_text = f"""
    SIMULATION METRICS
    
    Shock Magnitude: {results.shock_event.magnitude:.2f}σ
    Total Periods: {results.num_periods}
    Converged: {'✓' if results.convergence_achieved else '✗'}
    Dampening: {results.dampening_factor:.2f}
    
    Variables: {results.metadata.get('total_variables', 'N/A')}
    Relationships: {results.metadata.get('total_relationships', 'N/A')}
    """
    
    bbox_props = dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8)
    ax4.text(0.5, 0.5, metrics_text, transform=ax4.transAxes, fontsize=9,
             verticalalignment='center', horizontalalignment='center', bbox=bbox_props)
    
    # 5. Cumulative impacts (middle right)
    ax5 = fig.add_subplot(gs[1, 2])
    plt.sca(ax5)
    
    cumulative_impacts = {var: results.calculate_cumulative_impact(var) for var in vars_list}
    
    plt.pie(list(cumulative_impacts.values()), 
            labels=[v.replace('_', ' ').title() for v in cumulative_impacts.keys()],
            autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})
    plt.title('Cumulative Impact Distribution', fontweight='bold', fontsize=10)
    
    # 6. Final values comparison (bottom)
    ax6 = fig.add_subplot(gs[2, :])
    plt.sca(ax6)
    
    final_values = results.get_final_values()
    initial_values = {var: results.time_series[var][0] for var in final_values.keys()}
    
    vars_subset = list(final_values.keys())[:6]
    x_pos = np.arange(len(vars_subset))
    width = 0.35
    
    initial_vals = [initial_values[var] for var in vars_subset]
    final_vals = [final_values[var] for var in vars_subset]
    
    plt.bar(x_pos - width/2, initial_vals, width, label='Initial', color='lightgray', alpha=0.7)
    plt.bar(x_pos + width/2, final_vals, width, label='Final', color='steelblue', alpha=0.8)
    
    plt.xlabel('Economic Variables', fontsize=9)
    plt.ylabel('Values', fontsize=9)
    plt.title('Initial vs Final Variable Values', fontweight='bold', fontsize=10)
    plt.xticks(x_pos, [v.replace('_', ' ').title() for v in vars_subset], rotation=45, ha='right', fontsize=8)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Main title
    fig.suptitle(f'Economic Shock Analysis Dashboard\n{results.shock_event.description}', 
                fontsize=16, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


# Utility function for quick visualization
def quick_visualize(graph: CausalEconomicGraph, results: PropagationResults = None) -> None:
    """
    Quick visualization of graph and results (if provided).
    
    Args:
        graph: CausalEconomicGraph to visualize
        results: Optional PropagationResults to include
    """
    if results is None:
        plot_causal_network(graph, figsize=(10, 6))
    else:
        create_results_dashboard(results, graph, figsize=(15, 10))