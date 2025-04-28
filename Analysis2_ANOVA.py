import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy import stats

# Load your data
df = pd.read_csv('data.csv')  # <-- update with your actual file name
# 1. Remove participants who failed catch trials
# Define catch trial subset
catch_trials = df[df['is_catch'] == True]

# You can define "failed" catch trials however you want.
# Here, let's say a participant is an outlier if their RTs on catch trials are 2 SDs slower/faster than average
catch_rt_mean = catch_trials['rt'].mean()
catch_rt_std = catch_trials['rt'].std()

# Detect participants with weird catch trial responses
catch_trials['outlier'] = ((catch_trials['rt'] < (catch_rt_mean - 2*catch_rt_std)) | 
                           (catch_trials['rt'] > (catch_rt_mean + 2*catch_rt_std)))

df_outliers = df[df['valid_subject'] == False]

outlier_ids = df_outliers['id'].unique()
# List of participants to exclude
# outlier_ids = catch_trials[catch_trials['outlier']]['id'].unique()

print(f"Removing {len(outlier_ids)} participants who failed catch trials.")

# Remove outlier participants
df_clean = df[~df['id'].isin(outlier_ids)]

# 2. Filter only test trials (not catch trials)
df_test = df_clean[(df_clean['is_catch'] == False) & (df_clean['block'].str.contains('main', case=False))]

# 3. Set correct types
df_test['n_agents'] = df_test['n_agents'].astype('category')
df_test['congruency'] = df_test['congruency'].astype('category')
df_test['group_alignment'] = df_test['group_alignment'].astype('category')

# 4. Two-way ANOVA for RT
model_rt = ols('rt ~ C(n_agents) * C(congruency)', data=df_test).fit()
anova_table_rt = sm.stats.anova_lm(model_rt, typ=2)
print("\nTwo-way ANOVA for Response Time (RT):")
print(anova_table_rt)

# 5. Two-way ANOVA for Group Alignment
# Because group_alignment is categorical (F/NF), we'll use logistic regression
# Alternatively, you could encode F=1, NF=0 and treat it like a linear model, but logistic is better.
# df_test['group_alignment_binary'] = df_test['group_alignment'].map({'F': 1, 'NF': 0})
df_test['group_alignment_binary'] = (df["group_alignment"] == "F").astype(int) 
model_ga = ols('group_alignment_binary ~ C(n_agents) * C(congruency)', data=df_test).fit()
anova_table_ga = sm.stats.anova_lm(model_ga, typ=2)
print("\nTwo-way ANOVA (Linear Model) for Group Alignment:")
print(anova_table_ga)