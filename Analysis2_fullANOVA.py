"""
Created on Mon Apr 28 12:11:19 2025

@author: Asieh
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy import stats
from scipy.stats import chi2_contingency
# =============================================================================
df = pd.read_csv('data.csv')  

catch_trials = df[df['is_catch'] == True]   # I use catch trials to remove nonresponsive participants
# Outlier removal criteria:
# 1. Accuracy in catch trials is lower than 60% (less than 19 correct responses out of 32)
# 2. Accuracy in catch trials is less than 3 standard deviations below the mean accuracy across all subjects
# 3. Mean reaction time is more than 3 standard deviations above the mean reaction time of the sample
# I didn't remove outliers by myself. I trusted Valerii's
df_outliers = df[df['valid_subject'] == False]
outlier_ids = df_outliers['id'].unique()      # List of participants to exclude
# outlier_ids = catch_trials[catch_trials['outlier']]['id'].unique()

df_clean = df[~df['id'].isin(outlier_ids)]        # Remove outlier participants

# we only want main test trials (not catch trials)
df_test = df_clean[(df_clean['is_catch'] == False) & (df_clean['block'].str.contains('main', case=False))]

# Correct type of variables
df_test['n_agents'] = df_test['n_agents'].astype('category')
df_test['congruency'] = df_test['congruency'].astype('category')
df_test['group_alignment'] = df_test['group_alignment'].astype('category')

uniqueIDs = df_test['id'].unique()
n=0
FollowPercentage = np.empty([len(uniqueIDs),16])

for a in uniqueIDs:
    for b in np.arange(1,9):
        tempC = df_test[(df_test['id']==a) & (df_test['n_agents']==b) & (df_test['congruency']=='C')]
        Follow = sum(tempC['group_alignment']=='F')
        FollowPercentage[n,(b-1)] = sum(tempC['group_alignment']=='F')/len(tempC['group_alignment'])
        tempIC = df_test[(df_test['id']==a) & (df_test['n_agents']==b) & (df_test['congruency']=='IC')]
        Follow = sum(tempIC['group_alignment']=='F')
        FollowPercentage[n,(b+7)] = sum(tempIC['group_alignment']=='F')/len(tempIC['group_alignment'])
    n=n+1
    
FollowPercentageLong = FollowPercentage.reshape(-1,1)
ConformityArray = np.empty([len(FollowPercentageLong),3])
num_agents = np.transpose(np.matlib.repmat(np.matlib.repmat(np.arange(1,9),1,2),1,155)) 
congruency = np.transpose(np.matlib.repmat([np.array([1]*8+[0]*8)],1,155))
ConformityArray[:,0] = congruency[:,0]
ConformityArray[:,1] = num_agents[:,0]
ConformityArray[:,2] = FollowPercentageLong[:,0]
df_Conformity = pd.DataFrame(ConformityArray, columns=['congruency','num_agents','follow_percentage'])
df_Conformity['num_agents'] = df_Conformity['num_agents'].astype('category')
df_Conformity['congruency'] = df_Conformity['congruency'].astype('category')
# Two-way ANOVA for conformity
model_conformity = ols('follow_percentage ~ C(congruency) * C(num_agents)', data=df_Conformity).fit()
anova_table_conformity = sm.stats.anova_lm(model_conformity, typ=2)
print("\nTwo-way ANOVA for conformity:")
print(anova_table_conformity)
# Two-way ANOVA for RT
model_rt = ols('rt ~ C(n_agents) * C(congruency)', data=df_test).fit()
anova_table_rt = sm.stats.anova_lm(model_rt, typ=2)
print("\nTwo-way ANOVA for Response Time (RT):")
print(anova_table_rt)

# Chi2 test for Group Alignment
# Because group_alignment is categorical (F/NF), we'll use Chi2, but logistic is better.
df_test['group_alignment_binary'] = (df["group_alignment"] == "F").astype(bool) 


table = pd.crosstab(df_test['congruency'], df_test['group_alignment_binary'])
chi2, p, dof, expected = chi2_contingency(table)
print(f"Chi² = {chi2:.2f}, p = {p:.4f}")
