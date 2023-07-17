#%%
import pandas as pd

df_rct = pd.read_csv('https://raw.githubusercontent.com/s1ok69oo/causal_inference_100knock/main/data/causal_knock2_rct.csv')

df_reg = pd.read_csv('https://raw.githubusercontent.com/s1ok69oo/causal_inference_100knock/main/data/causal_knock2_reg.csv')

#%%
# estimate ATE (true ATE)
df_rct_t1 = df_rct[df_rct['t']==1]
df_rct_t0 = df_rct[df_rct['t']==0]

df_rct_t1['y'].mean() - df_rct_t0['y'].mean() # 901.4170602945262

#%%
# delete covariate not to use it
df = df_reg.drop('x3', axis=1)

#%%
# draw a DAG
import matplotlib.pyplot as plt
import networkx as nx
%matplotlib inline

G = nx.DiGraph()
G.add_edges_from([('x0', 'x1'), ('x1', 't'), ('x1', 'y'), ('t', 'x2'), ('t', 'y'), ('x2', 'y')])

nx.draw_networkx(G, node_color='#ABE1FA')
plt.show()

#%%
# regression all covariates
import statsmodels.api as sm

# covariate
X = df[['t', 'x0', 'x1', 'x2']]
X = sm.add_constant(X)

# target variable
y = df['y']

# output results
res = sm.OLS(y, X).fit()
print(res.summary())

"""
t coef 1201.7260
std err 38.252
R-squared 0.429
Adj. R-squared: 0.428
F-statistic: 375.1
AIC: 3.225e+04
BIC: 3.227e+04

this model is so-so.
we need to improve more!
"""

#%%
# regression to use a part of covariates (delete x0 since need not to use a covariate)
# covariate
X = df[['t', 'x1', 'x2']]
X = sm.add_constant(X)

# target variable
y = df['y']

# output results
res = sm.OLS(y, X).fit()
print(res.summary())
"""
same results to use all covariates,

so we do not have to always delete covariate.
"""

#%%
# regression to use a part of covariates (delete x2 since this covariate is mediator.)
# covariate
X = df[['t', 'x1']]
X = sm.add_constant(X)

# target variable
y = df['y']

# output results
res = sm.OLS(y, X).fit()
print(res.summary())
"""
t coef 851.8932
std err 44.412
R-squared 0.156
Adj. R-squared: 0.155
F-statistic: 184.4
AIC: 3.202e+04
BIC: 3.204e+04
"""

#%%
# regression to use only treatment covariates
# covariate
X = df[['t']]
X = sm.add_constant(X)

# target variable
y = df['y']

# output results
res = sm.OLS(y, X).fit()
print(res.summary())
"""
t coef 743.5676
std err 42.405
R-squared 0.133
Adj. R-squared: 0.133
F-statistic: 307.5
AIC: 3.308e+04
BIC: 3.308e+04

This model has a missing variable bias,
where necessary variables are missing.
Note that a missing variable bias can lead to inconsistency in the OLS estimator.
"""


#%%
# regression to use interaction term
# covariate
_df = df.copy()
_df['t*x1'] = _df['t'] * _df['x1']
X = _df[['t', 'x1', 't*x1']]
X = sm.add_constant(X)

# target variable
y = _df['y']

# output results
res = sm.OLS(y, X).fit()
print(res.summary())
"""
t coef 640.0696
std err 120.688
R-squared 0.157
Adj. R-squared: 0.156
F-statistic: 124.3
AIC: 3.302e+04
BIC: 3.305e+04

"""

#%%
# visualize a result to estimate
# covariate
X = df[['t', 'x1']]
X = sm.add_constant(X)

# target variable
y = df['y']

# output results
res = sm.OLS(y, X).fit()

# visualize
cols = X.columns
plt.bar(x=cols, height=res.params, yerr=res.bse, capsize=6, alpha=0.4)
plt.ylim(0, 1000)
plt.show()
