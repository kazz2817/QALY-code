import numpy as np
import pandas as pd
from scipy.integrate import quad
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator
from scipy.interpolate import interp1d

######interest rate######
r = 0.01 

######life span######
age_min = 20
age_max = 110 

######Specify file location in XXX regarding survival rate######
df_S = (
    pd.read_csv('XXX', index_col=0)) 
data = df_S.to_numpy()
t_vals = df_S.index.values.astype(float)
a_vals = df_S.columns.astype(float)
data = df_S.to_numpy()
interp2d = RegularGridInterpolator(
    (t_vals, a_vals),    
    data,               
    bounds_error=False, 
    fill_value=0.0 
)

#######Specify file location in XXX regarding income######
df_y = (
    pd.read_csv('XXX', dtype={'age': float})
      .dropna(subset=['age'])
)
df_y['age'] = df_y['age'].astype(int)
df_y = df_y.set_index('age')

######Specify file location in XXX regarding consumption######
df_c = (
    pd.read_csv('XXX', dtype={'age': float})
      .dropna(subset=['age'])
)
df_c['age'] = df_c['age'].astype(int)
df_c = df_c.set_index('age')

######Specify file location in XXX regarding population######
df_pop = (
    pd.read_csv('XXX', dtype={'age': float})
      .dropna(subset=['age'])
)
df_pop['age'] = df_pop['age'].astype(int)
df_pop = df_pop.set_index('age')

######Specify file location in XXX regarding elasticity######
df_phi = pd.read_csv('').set_index('age')

######Obtain continuous values based on point in age######
def S(t, a):
    return float(interp2d([[t, a]]))
def yF(t):
    return np.interp(t, df_y.index, df_y['yF'])
def cF(t):
    return np.interp(t, df_c.index, df_c['cF'])
def pop(t):
    return np.interp(t, df_pop.index, df_pop['pop'])
def phi(t, s):
    if isinstance(s, int):
        s = f'phi{s}'
    return df_phi.at[t, s]

######Define QoL scenarios######
def H_SCN1(a):
    if a <= 50:
        return 1
    else:
        return 1 * 0.98 ** (a - 50)
def H_SCN2(a):
    if a <= 50:
        return 1.0
    else:
        return 0.99 ** (a - 50)
def H_SCN3(a):
    if a <= 30:
        return 1.0
    elif a <= 50:
        return 0.99 ** (a - 30)
    elif a <= 65:
        return 0.99 ** 20
    else:
        plateau = 0.99 ** 20
        return plateau * (0.99 ** (a - 70))
def H_SCN4(a):
    if a <= 60:
        return 1.0
    if a == 60:
        return 0.7
    else:
        return 0.7 * (0.99 ** (a - 61))

######Define function to calculate VSL-year######
def v(t,s):
    val= yF(t) + phi(t,s)* cF(t)
    return val

######VSL at each age is calculated by summing the VSL-years in an iterative calculation at each scenario######
vsl_by_a = {}
for s in range(1, 5):
  for t in range(age_min, age_max): 
   vsl_by_a[s,t]=0
for a in range(age_min, age_max):
  total=0   
  for t in range(age_min, age_max):
    if t >= a: 
     total += np.exp(-r*(t-a)) * v(t,1) * S(a, t)
  vsl_by_a[1,a] = total
total=0   
for a in range(age_min, age_max):
  total=0   
  for t in range(age_min, age_max):
    if t >= a: 
     total += np.exp(-r*(t-a)) * v(t,2) * S(a, t)
  vsl_by_a[2,a] = total
total=0   
for a in range(age_min, age_max):
  total=0   
  for t in range(age_min, age_max):
    if t >= a: 
     total += np.exp(-r*(t-a)) * v(t,3) * S(a, t)
  vsl_by_a[3,a] = total
total=0   
for a in range(age_min, age_max):
  total=0   
  for t in range(age_min, age_max):
    if t >= a: 
     total += np.exp(-r*(t-a)) * v(t,4) * S(a, t)
  vsl_by_a[4,a] = total

######Calculate VSL for one year of life expectancy at any given age to calculate LEV in each scenario######
vsl_by_b = {}
for s in range(1, 5):
  for t in range(age_min, age_max): 
   vsl_by_b[s,t]=0
totalplus=0
for a in range(age_min, age_max):
  totalplus=0  
  for t in range(age_min, age_max): 
      if t > a: 
       totalplus += np.exp(-r*(t-a)) * v(t,1) * S(a, t-1)
  vsl_by_b[1,a] = totalplus + v(a,1)
totalplus=0
for a in range(age_min, age_max):
  totalplus=0  
  for t in range(age_min, age_max): 
      if t > a: 
       totalplus += np.exp(-r*(t-a)) * v(t,2) * S(a, t-1)
  vsl_by_b[2,a] = totalplus + v(a,2)
totalplus=0
for a in range(age_min, age_max):
  totalplus=0  
  for t in range(age_min, age_max): 
      if t > a: 
       totalplus += np.exp(-r*(t-a)) * v(t,3) * S(a, t-1)
  vsl_by_b[3,a] = totalplus + v(a,3)

totalplus=0
for a in range(age_min, age_max):
  totalplus=0  
  for t in range(age_min, age_max): 
      if t > a: 
       totalplus += np.exp(-r*(t-a)) * v(t,4) * S(a, t-1)
  vsl_by_b[4,a] = totalplus + v(a,4)

######Calculate QALY based on the definition of LEV and the QoL in each scenario######
QALY = {}
for a in range(age_min, age_max):
 QALY[1,a] = (vsl_by_b[1,a] - vsl_by_a[1,a])/H_SCN1(a)
 QALY[2,a] = (vsl_by_b[2,a] - vsl_by_a[2,a])/H_SCN2(a)
 QALY[3,a] = (vsl_by_b[3,a] - vsl_by_a[3,a])/H_SCN3(a)
 QALY[4,a] = (vsl_by_b[4,a] - vsl_by_a[4,a])/H_SCN4(a)

######Store QALYs for graphical representation######
age_vals = list(range(age_min, age_max))
qaly1 = [QALY[(1, a)] for a in age_vals]
qaly2 = [QALY[(2, a)] for a in age_vals]
qaly3 = [QALY[(3, a)] for a in age_vals]
qaly4 = [QALY[(4, a)] for a in age_vals]

######Store QoL for graphical representation######
qol1 = [H_SCN1(a) for a in age_vals]
qol2 = [H_SCN2(a) for a in age_vals]
qol3 = [H_SCN3(a) for a in age_vals]
qol4 = [H_SCN4(a) for a in age_vals]

######Output QoL to figure######
plt.figure(figsize=(8, 5))
plt.plot(age_vals, qol1, label='Scenario 1')
plt.plot(age_vals, qol2, label='Scenario 2')
plt.plot(age_vals, qol3, label='Scenario 3')
plt.plot(age_vals, qol4, label='Scenario 4')
plt.xlabel('Age')
plt.ylabel('QoL') 
plt.ylim(0, 1.2)   
plt.title('QoL')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

######Output QALY to figure######
plt.figure(figsize=(8, 5))
plt.plot(age_vals, qaly1, label='Scenario 1')
plt.plot(age_vals, qaly2, label='Scenario 2')
plt.plot(age_vals, qaly3, label='Scenario 3')
plt.plot(age_vals, qaly4, label='Scenario 4')
plt.xlabel('Age')
plt.ylabel('QALY')
plt.ylim(0, 1400)   
plt.title('QALY by Age for Each Scenario')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

######Set propotion for each scenario to be used for policy analysis######
frac_scn={}
frac_scn[1]=0.7
frac_scn[2]=0
frac_scn[3]=0.15
frac_scn[4]=0.15

######Set QALY_base reference values######
qaly_base=500
ave_QALY={}

######Calculate a weighted average of QALYs according to the scenario's propotion settings######
for a in range(age_min, age_max): 
 ave_QALY[a]=0
 for s in range(1, 5):
  ave_QALY[a] += frac_scn[s]*QALY[s,a]

######Calculation of policy evaluation######
CR=0
for a in range(age_min, age_max): 
 CR += (qaly_base - ave_QALY[a])*pop(a)
print(CR)



