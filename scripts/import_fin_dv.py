import requests
import json
from pyjstat import pyjstat


# taken from https://pxdata.stat.fi/PxWeb/pxweb/en/StatFin/StatFin__rpk/statfin_rpk_pxt_13rd.px/table/tableViewLayout1/
# domestic violence

url = 'https://pxdata.stat.fi:443/PxWeb/api/v1/en/StatFin/rpk/statfin_rpk_pxt_13rd.px'

# what's the keyword?
finn_dv = {
  "query": [
    {
      "code": "Uhrin ja epäillyn suhde",
      "selection": {
        "filter": "item",
        "values": [
          "SSS",
          "51T56_60_70_75",
          "51T56",
          "60_70",
          "75",
          "11T42_80T99",
          "11T13",
          "21T23",
          "41_42",
          "30_31_80T82",
          "99"
        ]
      }
    },
    {
      "code": "Hyvinvointialue",
      "selection": {
        "filter": "item",
        "values": [
          "SSS"
        ]
      }
    },
    {
      "code": "Uhrin ikä",
      "selection": {
        "filter": "item",
        "values": [
          "0-6",
          "0-17",
          "7-12",
          "13-17",
          "18-",
          "18-20",
          "21-29",
          "30-39",
          "40-49",
          "50-59",
          "60-69",
          "70-",
          "X"
        ]
      }
    },
    {
      "code": "Uhrin sukupuoli",
      "selection": {
        "filter": "item",
        "values": [
          "1",
          "2",
          "X"
        ]
      }
    }
  ],
  "response": {
    "format": "json-stat2"
  }
}

response = requests.post(url, json=finn_dv)

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
df_finn_dv = dataset.write('dataframe')

print(df_finn_dv.head())
