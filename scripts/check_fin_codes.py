import pandas as pd
import numpy as np

fin_det = pd.read_csv('data/raw/sexual_offences_fin_det.csv')
fin_det.head()
fin_det.columns.values

fin_det = fin_det[['Month', 'Offence group and specifier for criminal act', 'value']]

fin_det_group = fin_det.groupby(['Month', 'Offence group and specifier for criminal act'])['value'].sum().reset_index()
fin_det_group.tail()

# Let's focus on 1304 to start with

df_subcodes = fin_det_group[fin_det_group["Offence group and specifier for criminal act"].str.match(r"1304a\d+")]
df_subcodes.tail()
df_subcodes_group = df_subcodes.groupby(['Month'])['value'].sum().reset_index()
df_subcodes_group.tail()

fin_det_group_04 = fin_det_group.loc[fin_det_group['Offence group and specifier for criminal act'].str.match(r"1304\s")]
fin_det_group_04.tail()

# Let's compare
df_comp = fin_det_group_04.merge(df_subcodes_group, on='Month', how='outer')
df_comp.tail()

df_comp['diff'] = df_comp['value_x'] - df_comp['value_y']
df_comp['flag'] = np.where(df_comp['diff']>1, '>1', '<=1')
df_comp_group = df_comp.groupby('flag')['flag'].count()
df_comp_group
df_comp.shape