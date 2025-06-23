import requests
import json
from pyjstat import pyjstat
import pandas as pd

# Get info from their API
url = 'https://pxdata.stat.fi:443/PxWeb/api/v1/en/StatFin/rpk/statfin_rpk_pxt_13it.px'

# all the '13' offences are sexual offences
finn_13xx = {
  "query": [
    {
      "code": "Kunta",
      "selection": {
        "filter": "item",
        "values": [
          "SSS"
        ]
      }
    },
    {
      "code": "Rikosryhmä ja teonkuvauksen tarkenne",
      "selection": {
        "filter": "item",
        "values": [
          "231",
          "232",
          "233",
          "234",
          "235",
          "236",
          "236a1707",
          "237",
          "237a1707",
          "238",
          "239",
          "240",
          "240a1707"
        ]
      }
    }
  ],
  "response": {
    "format": "json-stat2"
  }
}

response = requests.post(url, json=finn_13xx)

# Check for success
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))  # Pretty print
else:
    print(f"Error: {response.status_code}")

# Convert response to JSON string (this is key!)
json_data = json.dumps(response.json())

# Parse with pyjstat
dataset = pyjstat.Dataset.read(json_data)

# Convert to pandas DataFrame
df_finn_13xx = dataset.write('dataframe')

print(df_finn_13xx.head())

df_finn_13xx.to_csv('data/raw/sexual_offences_fin.csv')

# Read the csv data
fn_csv = pd.read_csv('data/raw/sexual_offences_fin.csv')
fn_csv.head()
# shape of data seems ok based on current decision and DK's data

# Transform
fn_csv["Year"] = fn_csv["Month"].str.extract(r"(\d{4})").astype(int)
fn_group = fn_csv.groupby(['Offence group and specifier for criminal act', 'Year'])['value'].sum().reset_index()
fn_group.head()
fn_group['Offence group and specifier for criminal act'].unique()
fn_group['Offence group and specifier for criminal act'].nunique()

## Group the offences
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