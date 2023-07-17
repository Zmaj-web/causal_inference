#%%
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/s1ok69oo/causal_inference_100knock/main/data/causal_knock4.csv')
#%%
from dowhy import CausalModel
from IPython.display import Image, display

# DAG
model = CausalModel(
    data=df, 
    treatment='T', 
    outcome='Y', 
    common_causes='X'
    )

model.view_model()
display(Image(filename="causal_model.png"))

#%%
# visualize data
import matplotlib.pyplot as plt
%matplotlib inline

plt.scatter(x=df['X'], y=df['Y'], alpha=0.4)
plt.axvline(100, alpha=0.7, color='red', linestyle="dashed")
plt.xlim(0, None)
plt.ylim(0, None)
plt.xlabel('cumulative points')
plt.ylabel('sales')
plt.show()

#%%
# naive
y_under = df[df['X']<100]
y_over = df[df['X']>=100]

y_over['Y'].mean() - y_under['Y'].mean() # 1857.7437743774376

#%%
# non-parametric
y_x99 = df[df['X']==99]
y_x100 = df[df['X']==100]

y_x100['Y'].mean() - y_x99['Y'].mean() # 1347.3333333333335


#%%
# non-parametric with band width = 5
h = 5
y_under5 = df[(df['X']<=99)&(df['X']>=99-h)]
y_over5 = df[(df['X']>=100)&(df['X']<=100+h)]

y_over5['Y'].mean() - y_under5['Y'].mean() # 1228.9499999999998

#%%
# non-parametric with band width = 30
h = 30
y_under30 = df[(df['X']<=99)&(df['X']>=99-h)]
y_over30 = df[(df['X']>=100)&(df['X']<=100+h)]

y_over30['Y'].mean() - y_under30['Y'].mean() # 1453.2319327731093

"""
This result is near naive estimate,
so band width is too large.
"""

#%%
# parametric (regression)
import statsmodels.api as sm

X = df[['X', 'T']]
X = sm.add_constant(X)

y = df['Y']

res = sm.OLS(y, X).fit()
print(res.summary())
"""
t coef 1037.8711
std err 119.526

R-squared:                       0.846
Adj. R-squared:                  0.844
F-statistic:                     539.94
AIC:                             2979
BIC:                             2989
"""

#%%
# parametric (regression, ANCOVA)
import statsmodels.api as sm

df['X_times_T'] = df['X']*df['T']
X = df[['X', 'T', 'X_times_T']]
X = sm.add_constant(X)

y = df['Y']

res = sm.OLS(y, X).fit()
print(res.summary())
"""
t coef 2168.5000
std err 271.368
X_times_T coef -11.4556
std err 2.496
-> t + 100*X_times_T, coef 1023

R-squared:                       0.861
Adj. R-squared:                  0.859
F-statistic:                     403.6
AIC:                             2960
BIC:                             2973
"""

#%%
# RDD estimate (cutoff 100)
res.params['T'] + 100*res.params['X_times_T'] # 1022.9410064664532
