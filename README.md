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
- `df_S`: Survival probability over age.
- `df_y`: Age-specific income (`yF`).
- `df_c`: Age-specific consumption (`cF`).
- `df_pop`: Age-specific population distribution.
- `df_phi`: Age-specific elasticity.
These are loaded using `pandas.read_csv()` and set to appropriate data types and indices.
---

#### 3. **Survival and Income Functions**
Interpolation functions are created:
- `S(t, a)`: Survival probability from age `a` to time `t`.
- `yF(t)`, `cF(t)`: Interpolated income and consumption at time `t`.
- `pop(t)`: Population at time `t`.
- `phi(t, s)`: Policy-dependent adjustment coefficients.

---

#### 4. **Health State Functions per Scenario**
Four health scenarios (SCN1 to SCN4) are modeled using different age-specific quality-of-life deterioration functions.

---

#### 5. **Net Present Value of VSL**
Two formulations of VSL are calculated for each scenario:
- `vsl_by_a`: Standard expected lifetime utility starting at age `a`.
- `vsl_by_b`: Utility gain from marginal life extension.

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
Weighted average QALYs across scenarios are computed using scenario fractions. The aggregate cost reduction (`CR`) is calculated relative to a base QALY level of 500.

---

"""

# Create a basic README.md content
readme_content = """
# QALY Estimation Based on VSL

This repository contains Python code for estimating the monetary value of a Quality-Adjusted Life Year (QALY) based on the Value of a Statistical Life (VSL), under different age-specific health deterioration scenarios.

## Requirements
- Python 3.x
- pandas
- numpy
- matplotlib
- scipy

## Files
- `main.py`: Main computational script.
- `income.csv`, `consumption.csv`, `population.csv`, `phi.csv`, `XXX`: Required data files.

## Usage
Update the file paths as needed and run the script:
```bash
python main.py
```

## Output
- Two figures: QoL by age and QALY by age for each scenario.
- Printed cost reduction value (`CR`) based on weighted QALY differences.

## License
MIT License
"""

# Display the contents
supplementary_df = pd.DataFrame([{
    "Section": "Supplementary Description",
    "Content": supplementary_description.strip()
}, {
    "Section": "README.md",
    "Content": readme_content.strip()
}])

import ace_tools as tools; tools.display_dataframe_to_user(name="Code Documentation Summary", dataframe=supplementary_df)
