import pandas as pd
# https://pxdata.stat.fi/PxWeb/pxweb/en/StatFin/StatFin__vaerak/statfin_vaerak_pxt_11ra.px/table/tableViewLayout1/

fin_pop_raw = pd.read_csv('data/raw/fin_pop_raw.csv',skiprows=2)
fin_pop_raw.head()

fin_pop_melt = fin_pop_raw.drop(columns='Area').melt(id_vars=['Information'], var_name='Year', value_name='Pop')
fin_pop_melt.head()
fin_pop_melt['Pop_thousands'] = (fin_pop_melt['Pop']/1000).round()

fin_pop_melt.to_csv('data/clean/population_fin.csv')