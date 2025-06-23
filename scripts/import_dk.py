# Libraries
import pandas as pd

# Read
dk_xlsx = pd.read_excel('data/raw/Nof_reported_sexualoffences_dk.xlsx',skiprows=2)
dk_xlsx.head()
dk_raw = dk_xlsx.rename(columns={dk_xlsx.columns[1]:'Offence_type'}).drop(columns=[dk_xlsx.columns[0]])
dk_raw.head()

# Transform
## Pivot
dk_melt = dk_raw.melt(id_vars="Offence_type", var_name="YearQ", value_name="Offence_count")
dk_melt.head()

## Remove totals
dk_melt.shape
dk_melt = dk_melt.loc[dk_melt['Offence_type']!='Sexual offenses, total']
dk_melt.shape

## Add years & totals
dk_melt["Year"] = dk_melt["YearQ"].str.extract(r"(\d{4})").astype(int)
dk_year = dk_melt.groupby(['Offence_type', 'Year'])['Offence_count'].sum().reset_index()
dk_year.head()

##
dk_year.Offence_type.unique(); dk_year.Offence_type.nunique()
# nof=14

## Check some categories around years of change
dk_year.loc[(dk_year['Offence_type']=='Heterosexual offence against a child under 12 (Repealed in 2013)') & (dk_year['Year']>=2013)]
# Changes seem to be recorded after 2013
dk_year.loc[(dk_year['Offence_type']=='Sexual offence against a child under 12 (New from 2013)') & (dk_year['Year']<=2013)]
# No, actually we have values for both. Change registered in July. Probably this is reflected in the Q data

## Let's make categories
# Categories for now: 
# 1. Rape/Aggravated rape / Attempted Rape 
# 2. Sexual Assault / Abuse (Non-Rape)
# 3. Child Sexual Offences
# 4. Incest / Family-based Offences
# 5. Grooming / Contact for Sexual Purposes
# 6. Sexual Harassment / Public Decency / Non-Contact Offences
# 7. Exploitation / Commercial Sex (Prostitution, Pimping)

def classify_offence(offence):
    offence = offence.lower()  

    if "rape" in offence:
        return "Rape / Aggravated Rape"
    elif (("heterosexual offence" in offence or "homosexual offence" in offence or "any other kind of sexual offence" in offence) and 'child' not in offence):
        return "Sexual Assault / Abuse (Non-Rape)"
    elif "child" in offence:
        return "Child Sexual Offences"
    elif "incest" in offence:
        return "Incest / Family-based Offences"
    elif "grooming" in offence:
        return "Grooming / Contact for Sexual Purposes"
    elif "public decency" in offence or "groping" in offence or "indecent exposure" in offence:
        return "Sexual Harassment / Public Decency / Non-Contact Offences"
    elif "prostitution" in offence:
        return "Exploitation / Commercial Sex (Prostitution, Pimping)"
    else:
        return "Uncategorized"
    
dk_year["Offence_group"] = dk_year["Offence_type"].apply(classify_offence)
dk_year.head()

# Totals
dk_df = dk_year.groupby(['Offence_group', 'Year'])['Offence_count'].sum().reset_index()
dk_df.head()

# Check
dk_year.loc[
    ((dk_year["Offence_type"]=='Any other kind of heterosexual offence (Repealed in 2013)') |
    (dk_year["Offence_type"]=='Any other kind of homosexual offence (Repealed in 2013)') | 
    (dk_year["Offence_type"]=='Any other kind of sexual offence (New from 2013)')) &
    (dk_year['Year']==2015)
    ]
dk_df.loc[
    (dk_df['Offence_group']=='Sexual Assault / Abuse (Non-Rape)') &
    (dk_df['Year']==2015)
]

dk_df.to_csv('data/clean/dk_clean.csv')