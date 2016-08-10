import pandas as pd


a = pd.read_csv("public/_assets/zika.csv", thousands=",")

#convert to integers
a['locally_acquired_cases'] = a['locally_acquired_cases'].astype(float)
a['travel_associated_cases'] = a['travel_associated_cases'].astype(float)

#create new column
a['all_cases'] = a['locally_acquired_cases'] + a['travel_associated_cases']


a.to_csv("public/_assets/zika.csv", index=False)

a2 = pd.read_csv("public/_assets/zika.csv")
b_json = pd.read_json("data/data.json")
b_json.to_csv("public/_assets/location.csv", index=False)
b = pd.read_csv("public/_assets/location.csv")
merged = a2.merge(b, on='state')
merged.to_csv("public/_assets/zika_state_data.csv", index=False)

c = pd.read_csv("public/_assets/zika_total_cases.csv")

#adding commas
format_mapping={'In the 50 states and D.C.': '{:,}', 'In the U.S. territories': '{:,}'}
for key, value in format_mapping.items():
	c[key] = c[key].apply(value.format)

c.to_json("data/cases.json", orient="records")
