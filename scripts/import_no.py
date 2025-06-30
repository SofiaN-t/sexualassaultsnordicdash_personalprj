import pandas as pd
import numpy as np

# Read
no_xlsx = pd.read_excel('data\\raw\\sexualoffences_no.xlsx', skiprows=2)
no_xlsx.head()
no_xlsx.dtypes
no_xlsx.drop(columns='Unnamed: 0',inplace=True)
no_xlsx.rename(columns={'Unnamed: 1':'Offence'}, inplace=True)
no_nona = no_xlsx.copy().dropna(subset='Offence')

# Transform
## Let's simplify how the categories are written: to get rid of special symbol
conditions = [
    (no_nona['Offence'].str.startswith('¬ ', na=False)),
    (no_nona['Offence'].str.startswith('¬¬ ', na=False)),
    (no_nona['Offence'].str.startswith('¬¬¬ ', na=False)),
    (no_nona['Offence'].str.startswith('¬¬¬¬ ', na=False))
]
values = [1, 2, 3, 4]

# Identify the level & make helper column
no_nona['Offence_level'] = np.select(conditions, values)

# I want to keep only the higher level within each category
#  So, if every next row is one number greater than the previous, I want the previous row to be dropped
def keep_main_groups(df):
    df = df.copy()
    keep_mask = [False] * len(df)

    for i in range(len(df)):
        current_level = df.loc[i, "Offence_level"]
        # Check if any later row is a subgroup
        if i + 1 >= len(df) or df.loc[i + 1, "Offence_level"] <= current_level:
            keep_mask[i] = True

    return df[keep_mask]

no_main = keep_main_groups(no_nona)
no_main.head(); no_main.tail()

## Make categories
def classify_offence(offence):
    offence = offence.lower()  

    if "rape" in offence and not "child" in offence:
        return "Rape / Aggravated Rape"
    elif "child" in offence:
        return "Child Sexual Offences"
    elif "family" in offence:
        return "Incest / Family-based Offences"
    elif  (("sexual act" in offence or "sexual intercourse" in offence) and not "child" in offence):
        return  "Sexual Assault / Abuse (Non-Rape)"
    elif (("sexually abusive" in offence or "unspecified" in offence) and not "child" in offence):
        return "Sexual Harassment / Public Decency / Non-Contact Offences"
    else:
        return "Uncategorized"

no_main["Offence_group"] = no_main["Offence"].apply(classify_offence)
no_main.shape
no_main.head(13)
no_main[['Offence', 'Offence_group']]
no_main['Offence_group'].unique()

## Now, we will  make the years a column
no_melt = no_main.drop(columns=["Offence", "Offence_level"]).melt(id_vars=["Offence_group"], var_name="Year", value_name="Offence_count")
no_melt.head()

## And, sum the groups
df_no = no_melt.groupby(['Offence_group', 'Year'])['Offence_count'].sum().reset_index()
df_no.head()

# Check
## For child groups
no_xlsx_child = no_nona.drop(columns='Offence_level').loc[no_nona['Offence'].str.contains('child', case=False, na=False)]
no_xlsx_child.head()
no_child_sum = no_xlsx_child.sum(numeric_only=True)
no_child_sum
## Compare 
df_no["Offence_count"].loc[df_no['Offence_group']=='Child Sexual Offences'].values == no_child_sum.values
### Checks out

## For rape
no_xlsx_rape = no_xlsx.loc[((no_xlsx['Offence']=='¬¬¬¬ Rape, other or unspecified age') | 
                           (no_xlsx['Offence']=='¬¬¬¬ Aggravated rape, other or unspecified age') |
                           (no_xlsx['Offence']=='¬¬ Attempted rape'))
                           ].drop(columns='Offence')
# no_xlsx_rape.values.sum(axis=0)
df_no['Offence_count'].loc[df_no['Offence_group']=='Rape / Aggravated Rape'].values == no_xlsx_rape.values.sum(axis=0)
### Checks out

# Write
df_no.to_csv('data/clean/no_clean.csv')

