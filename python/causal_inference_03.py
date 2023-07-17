#%%
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/s1ok69oo/causal_inference_100knock/main/data/causal_knock3.csv', index_col=0)
#%%
# naive
# 2018/04 - 2018/03
df.loc[201804, 'Kagoshima'] - df.loc[201803, 'Kagoshima'] # -264

#%%
# choose treatment group
import matplotlib.pyplot as plt
%matplotlib inline

plt.plot(df.index.astype('str'), df['Fukuoka'], label='Fukuoka')
plt.plot(df.index.astype('str'), df['Kumamoto'], label='Kumamoto')
plt.plot(df.index.astype('str'), df['Kagoshima'], label='Kagoshima')
plt.plot(df.index.astype('str'), df['Okinawa'], label='Okinawa')
plt.legend()
plt.ylim(1500, 5500)
plt.xticks(rotation=45)
plt.show()

"""
Kumamoto: has a parallel trend for Kagoshima
"""

#%%
# DID(aggregate)
d0 = df.loc[201803, 'Kagoshima'] - df.loc[201803, 'Kumamoto']
d1 = df.loc[201804, 'Kagoshima'] - df.loc[201804, 'Kumamoto']

d1 - d0 # 458
"""
we can estimate a causal impact: 458
"""

#%%
# DID(by regression)
import numpy as np

dummies = np.where(df.index>201803, 1, 0)

df_kagoshima = pd.DataFrame({'revenue': df['Kagoshima'],
                            'kagoshima_dummy': 1, 
                            'ad_dummy': dummies, 
                            'date': df.index})

df_kumamoto = pd.DataFrame({'revenue': df['Kumamoto'], 
                            'kagoshima_dummy': 0, 
                            'ad_dummy': dummies, 
                            'date': df.index})

df_reg = pd.concat([df_kagoshima, df_kumamoto])
df_reg['kagoshima_ad'] = df_reg['kagoshima_dummy']*df_reg['ad_dummy']
df_reg = pd.get_dummies(df_reg, columns=['date'], drop_first=True)
df_reg.head()

import statsmodels.api as sm

# covariate
X = df_reg.iloc[:, 1:]
X = sm.add_constant(X)

# target variable
y = df_reg.iloc[:, 0]

# output result
res = sm.OLS(y, X).fit()
print(res.summary())

#%%
# standard error of cluster ???
import statsmodels.formula.api as smf

formula = f"{df_reg.columns[0]} ~ {df_reg.columns[1]}"
for variable in df_reg.columns[2:]:
    formula += f" + {variable}"

res = smf.ols(formula=formula, data=df_reg).fit(cov_type='cluster', cov_kwds={'groups': df_reg['kagoshima_dummy']})
res.bse['kagoshima_ad']

#%%
# transform to logarithm
# covariate
X = df_reg.iloc[:, 1:]
X = sm.add_constant(X)

# target variable
y = np.log(df_reg.iloc[:, 0])

# output result
res = sm.OLS(y, X).fit()
print(res.summary())

"""
to use logarithm when we interpret a estimate as ratio.
kagoshima_ad        0.1682
above result, revenue is increased 16.82% by kagoshima_ad
"""
#%%
# estimate by Causal Impact
from causalimpact import CausalImpact

data = df[['Kagoshima', "Kumamoto"]].reset_index(drop=True)

pre_period = [0, 14]
post_period = [15, 23]

ci = CausalImpact(data, pre_period, post_period)
ci.run()
print(ci.summary())
"""
ad effect 652.63 (Absolute effect)
"""
#%%
ci.plot()
