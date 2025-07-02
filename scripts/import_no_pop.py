import pandas as pd

# https://www.ssb.no/en/statbank/table/06913/tableViewLayout1/

no_pop_raw = pd.read_excel('data/raw/no_pop_raw.xlsx', skiprows=2)
no_pop_raw.head()

no_pop_raw_totals = no_pop_raw.sum(numeric_only=True).reset_index()
no_pop_raw_totals.head()
no_pop_raw_totals.rename(columns={'index': 'Year', 0: 'Pop'}, inplace=True)

no_pop_raw_totals['Pop_thousands'] = (no_pop_raw_totals['Pop'] / 1000).round()

# Export
no_pop_raw_totals.to_csv('data/clean/population_no.csv') # population January
