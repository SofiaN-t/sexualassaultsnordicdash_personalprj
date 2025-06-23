url = 'https://pxdata.stat.fi:443/PxWeb/api/v1/en/StatFin/rpk/statfin_rpk_pxt_13it.px'

finn_13xx_det = {
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
          "231T241",
          "231",
          "232",
          "232a1701",
          "232a1702",
          "232a1703",
          "232a1704",
          "232a1706",
          "232a1705",
          "232a17XX",
          "233",
          "234",
          "234a1701",
          "234a1702",
          "234a1703",
          "234a1704",
          "234a1706",
          "234a1705",
          "234a17XX",
          "235",
          "236",
          "236a1707",
          "237",
          "237a1707",
          "238",
          "239",
          "240",
          "240a1707",
          "241",
          "241a1707"
        ]
      }
    }
  ],
  "response": {
    "format": "json-stat2"
  }
}

response = requests.post(url, json=finn_13xx_det)

json_data = json.dumps(response.json())

# Parse with pyjstat
dataset = pyjstat.Dataset.read(json_data)

# Convert to pandas DataFrame
df_finn_13xx_det = dataset.write('dataframe')

print(df_finn_13xx_det.head())

df_finn_13xx_det.to_csv('data/raw/sexual_offences_fin_det.csv')
