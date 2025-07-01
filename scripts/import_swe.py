# Libraries
import pandas as pd

# Read
swe_dict = pd.read_excel('data/raw/sexualoffences_swe.xls', sheet_name='Sheet2')
swe_dict.head()

swe_xlsx = pd.read_excel('data/raw/sexualoffences_swe.xls', skiprows=3)
swe_xlsx.tail()
swe_xlsx.dtypes
swe_xlsx.drop(columns='Unnamed: 1',inplace=True)
swe_xlsx.rename(columns={'Unnamed: 0':'Offence_swe'}, inplace=True)
## Join with english title
swe_raw = swe_xlsx.merge(swe_dict, left_on='Offence_swe', right_on='Danish')
swe_raw.head()
swe_raw.drop(columns=['Offence_swe','Danish'], inplace=True)
swe_raw.rename(columns={'English':'Offence'}, inplace=True)
swe_raw.dtypes
## Make numerics
cols_to_convert = swe_raw.columns[swe_raw.columns != 'Offence']
swe_raw[cols_to_convert] = swe_raw[cols_to_convert].apply(pd.to_numeric, errors='coerce')
## Drop all empty & totals
swe_non_na = swe_raw.dropna(axis=0, how='all', subset=swe_raw.select_dtypes(include='number').columns)
swe_non_na.head()
swe_non_na = swe_non_na.loc[swe_non_na['Offence'] != 'Chapter 6: Sexual offences']

## Make categories
def classify_offence(offence):
    offence = offence.lower()  

    if "rape" in offence:
        return "Rape / Aggravated Rape"
    elif "assault" in offence or "coercion" in offence:
        return "Sexual Assault / Abuse (Non-Rape)"
    elif "child" in offence and not "grooming" in offence:
        return "Child Sexual Offences"
    elif "descendant" in offence:
        return "Incest / Family-based Offences"
    elif "grooming" in offence:
        return "Grooming / Contact for Sexual Purposes"
    elif "harassment" in offence:
        return "Sexual Harassment / Public Decency / Non-Contact Offences"
    elif "purchase" in offence or "pimping" in offence:
        return "Exploitation / Commercial Sex (Prostitution, Pimping)"
    else:
        return "Uncategorized"
    
swe_non_na["Offence_group"] = swe_non_na["Offence"].apply(classify_offence)
swe_non_na.head()

## Melt
swe_melt = swe_non_na.drop(columns='Offence').melt(id_vars=['Offence_group'], var_name='Year', value_name='Offence_count')
swe_melt.head()
## Totals
swe_group  = swe_melt.groupby(['Offence_group', 'Year'])['Offence_count'].sum().reset_index()
swe_group.head()
swe_group.Offence_group.unique()

# Check
## For child
swe_raw_child = swe_raw.loc[(swe_raw['Offence'].str.contains('child')) & (~swe_raw['Offence'].str.contains('grooming'))]
swe_raw_child.head()
swe_raw_child_sum = swe_raw_child.sum(numeric_only=True)
## Compare
swe_group['Offence_count'].loc[swe_group['Offence_group']=='Child Sexual Offences'].values == swe_raw_child_sum.values
## For rape
swe_raw_rape = swe_raw.loc[swe_raw['Offence'].str.contains('rape')]
swe_raw_rape.head()
swe_group['Offence_count'].loc[swe_group['Offence_group']=='Rape / Aggravated Rape'].values == swe_raw_rape.sum(numeric_only=True).values
