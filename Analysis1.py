# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 19:56:40 2025

@author: Asieh
"""

import pandas as pd
import numpy as np

df = pd.read_csv('data.csv')

df_congruent_main = df[((df['block']=='Main Block 1')|(df['block']=='Main Block 2')) & (df['congruency']=='C') & (df['is_catch']==False)]
df_incongruent_main = df[((df['block']=='Main Block 1')|(df['block']=='Main Block 2')) & (df['congruency']=='IC') & (df['is_catch']==False)]

