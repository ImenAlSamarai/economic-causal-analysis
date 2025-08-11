# Examples

This directory contains demonstration scripts showcasing the Economic Causal Analysis System's capabilities.

## 🚀 Quick Start

Run all examples:
```bash
cd examples
./run_demo.sh
```

## 📊 Available Examples

### 1. Basic Demo (`basic_demo.py`)
**Purpose**: Demonstrates core functionality with a simple economic model
- Creates a 5-variable economic system
- Shows shock propagation through the economy
- Federal funds rate shock affecting GDP, unemployment, and inflation
- **Runtime**: ~30 seconds
- **Good for**: First-time users, understanding basic concepts

**Key features demonstrated:**
- Graph creation and validation
- Variable and relationship management
- Shock propagation with temporal dynamics
- Results analysis and visualization

### 2. Federal Reserve Policy Analysis (`federal_reserve_analysis.py`)
**Purpose**: Sophisticated analysis of monetary policy using different causal mechanisms
- **Linear mechanisms**: Traditional monetary transmission
- **Threshold mechanisms**: Interest rate policy effectiveness
- **Exponential mechanisms**: Consumer confidence cascades
- **Saturation mechanisms**: Okun's law implementation

**Economic relationships modeled:**
- Fed Funds Rate → GDP Growth (threshold effect)
- Unemployment → GDP Growth (Okun's law with saturation)
- Fed Funds Rate → Inflation (linear relationship)  
- GDP Growth → Consumer Confidence (exponential cascading)

**Key insights:**
- Small rate changes (< 0.25%) have minimal immediate impact
- Large rate changes trigger significant amplified responses
- Consumer confidence exhibits cascading behavior
- Unemployment effects saturate at extreme levels

### 3. Shock Propagation Demo (`shock_propagation_demo.py`)
**Purpose**: Advanced counterfactual analysis with multi-period dynamics
- Emergency rate hike scenario (2σ shock)
- 12-period propagation simulation
- Convergence analysis and stability testing
- Peak effect timing and cumulative impact measurement

**Advanced features demonstrated:**
- Multi-period shock propagation
- Uncertainty quantification
- Convergence detection
- Systemic risk assessment
- Peak effect analysis

## 🎯 Running Individual Examples

### Basic Demo
```bash
python examples/basic_demo.py
```
**Expected output:** System validation, shock simulation, and results summary

### Federal Reserve Analysis
```bash
python examples/federal_reserve_analysis.py
```
**Expected output:** Comparison of policy scenarios with different mechanism types

### Shock Propagation Demo
```bash
python examples/shock_propagation_demo.py
```
**Expected output:** Time-series analysis of economic shock propagation

## 📈 Understanding the Output

### Typical Output Structure:
```
🏦 Economic System Analysis
==================================================
📊 Creating Economic Variables:
   ✓ fed_funds_rate: 2.5% (policy)
   ✓ gdp_growth: 2.1% (endogenous)
   ...

🔗 Creating Causal Relationships:
   ✓ Fed Funds Rate -> GDP Growth (threshold)
   ✓ Unemployment -> GDP Growth (saturation)
   ...

🎯 Scenario Analysis:
   📈 Small rate increase: +0.25%
   📈 Large rate increase: +0.75%
   
🎉 Analysis Complete!
```

### Key Metrics to Watch:
- **Peak Effects**: Maximum impact timing and magnitude
- **Convergence**: Whether system reaches new equilibrium
- **Cumulative Impact**: Total economic effect over time
- **Threshold Activation**: When policy mechanisms engage

## 🔧 Customization

### Modify Economic Variables:
```python
# Adjust base economic conditions
gdp_growth = EconomicVariable(
    name="GDP_growth",
    current_value=3.0,  # Change baseline
    uncertainty=0.5,    # Adjust uncertainty
    bounds=(-3, 6)      # Set realistic bounds
)
```

### Create New Shock Scenarios:
```python
# Custom shock event
oil_crisis = ShockEvent(
    variable_name="oil_price",
    magnitude=3.0,      # 3 standard deviation shock
    duration=6,         # Persistent for 6 periods
    decay_rate=0.2,     # 20% decay per period
    description="Oil supply disruption"
)
```

### Add New Mechanisms:
```python
# Custom threshold for policy effectiveness
policy_mechanism = CausalMechanism(
    MechanismType.THRESHOLD,
    {"threshold": 0.5, "scale_factor": 3.0},
    description="Large policy changes required for impact"
)
```

## 📚 Educational Use

These examples are designed for:
- **Economics students**: Understanding causal modeling
- **Policy analysts**: Exploring intervention effects
- **Researchers**: Learning advanced simulation techniques
- **Developers**: Integration patterns and API usage

## 🤝 Contributing Examples

To add a new example:
1. Create descriptive filename (e.g., `climate_economics_demo.py`)
2. Include comprehensive docstring with purpose and key features
3. Follow existing output format for consistency
4. Update this README with description
5. Test with `python validate_system.py` to ensure compatibility

---

**Need help?** Check the main README.md for detailed API documentation and theoretical foundations.