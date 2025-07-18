# QALY-code
import pandas as pd
from IPython.display import display

This code estimates the monetary value of a Quality-Adjusted Life Year (QALY) derived from the Value of a Statistical Life (VSL) under different QoL scenarios. The computational steps are as follows:

---

#### 1. **Parameter and Age Range Setup**
- Set Interest rate
- Set Age range
---

#### 2. **Data Loading**
- `df_S`: Survival rate over age.
- `df_y`: Age-specific income (`yF`).
- `df_c`: Age-specific consumption (`cF`).
- `df_pop`: Age-specific population distribution.
- `df_phi`: Age-specific elasticity.
These are loaded using `pandas.read_csv()` and set to appropriate data types and indices.
---

#### 3. **Functions**
Interpolation functions are created:
- `S(t, a)`: Survival probability from age `a` and `t`.
- `yF(t)`, `cF(t)`: Interpolated income and consumption at age `t`.
- `pop(t)`: Population at age `t`.
- `phi(t, s)`: elasticity of substitution at age `t` in scenario `s`.
---

#### 4. **QoL scenatio setting**
Four scenarios (SCN1 to SCN4) are modeled using different age-specific QoL.

---

#### 5. **VSL Caluculation**
Two formulations of VSL are calculated for each scenario:
- `vsl_by_a`: VSL at given age `a` for each scenario.
- `vsl_by_b`: VSL for one year of life expectancy at given age `a` for each scenario.
---

#### 6. **Monetary Value of a QALY**
QALY is computed by taking the difference between `vsl_by_b` and `vsl_by_a`, normalized by the quality of life (QoL) at each age.

---

#### 7. **Visualization**
Two plots are generated:
- QoL vs. Age for each scenario.
- QALY vs. Age for each scenario.
---

#### 8. **Population-weighted Average QALY and Cost Reduction**
Weighted average QALYs across scenarios are computed using scenario fractions. The aggregate cost reduction (`CR`) is calculated relative to a base (reference) QALY level.

---

"""

# Create a basic README.md content
readme_content = """
# QALY Estimation Based on VSL

This repository contains Python code for estimating the monetary value of a Quality-Adjusted Life Year (QALY) based on the Value of a Statistical Life (VSL), under different age-specific health deterioration scenarios.

## Requirements
- Python 3.12.1
- pandas
- numpy
- matplotlib
- scipy

## Files
- `QALY.py`: Main computational script.
- Required data files related to Income, Consumption, Survival rate, and elasticity.

## Output
- Two figures: QoL by age and QALY by age for each scenario.
- Printed cost reduction value (`CR`) based on weighted QALY differences.


# Display the contents
supplementary_df = pd.DataFrame([{
    "Section": "Supplementary Description",
    "Content": supplementary_description.strip()
}, {
    "Section": "README.md",
    "Content": readme_content.strip()
}])

import ace_tools as tools; tools.display_dataframe_to_user(name="Code Documentation Summary", dataframe=supplementary_df)
