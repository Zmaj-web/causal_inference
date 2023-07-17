#%%
import pandas as pd
df = pd.read_csv('https://raw.githubusercontent.com/s1ok69oo/causal_inference_100knock/main/data/causal_knock1.csv')

#%%
from dowhy import CausalModel
from IPython.display import Image, display

data = df[['y', 't', 'x']]

# plot DAG
model = CausalModel(
    data=data, 
    treatment='t', 
    outcome='y', 
    effect_modifiers='x'
    )

model.view_model()
display(Image(filename="causal_model.png"))
#%%
df.head()
#%%

# E[y-x]
# naive results
df['y'].mean() - df['x'].mean() # -0.7999999999999989

#%%
# y1-y0
# ITE
df["y_t1"] - df["y_t0"]

#%%
# E[y1-y0]
# ATE average treatment effect(true results)
df['y_t1'].mean() - df['y_t0'].mean() # 4.966666666666667

#%%
# E[y1-y0|t=1]
# ATT
# ATT = ATE when treatments assign at random
df_t1 = df[df['t']==1]
df_t1['y_t1'].mean() - df_t1['y_t0'].mean() # 4.92

#%%
# E[y1-y0|x>10]
# CATE conditional ATE
df_over10 = df[df['x']>10]
df_over10['y_t1'].mean() - df_over10['y_t0'].mean() # 5.0

#%%
# check the covariate of distributions
# ->those distributions are at random, right?
# plot histogram
import matplotlib.pyplot as plt
%matplotlib inline

# Number of orders received in the previous season for sales
# with analysis reports
df_t1 = df[df['t']==1]
plt.hist(df_t1['x'], alpha=0.3, label='have report')

# Number of orders received in the previous season for sales
# without analysis report
df_t0 = df[df['t']==0]
plt.hist(df_t0['x'], alpha=0.3, label='have no report')

# plot
plt.legend()
plt.show()


#%%
# E[y1-y0]
# estimate ATE
df_t1 = df[df['t']==1]
df_t0 = df[df['t']==0]

df_t1['y'].mean() - df_t0['y'].mean() # 4.434285714285714

#%%
# t-test
# H0:E[y1]=E[y0]
# H1:E[y1]>E[y0]
# alpha:0.05
from scipy import stats

t, p = stats.ttest_ind(df_t1['y'], df_t0['y'], alternative='greater')
print(f"p-value: {p}") # p-value: 0.00738068613529863

"""
Since the p-value is smaller than 0.05,
the null hypothesis can be rejected
and interpreted as

'the analysis report has a positive effect
on the number of sales orders received'.

"""