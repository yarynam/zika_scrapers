import pandas as pd
import glob

read_files = glob.glob("data/*")

for f in read_files:

    name_string = f.replace('.csv', '')
    name_string = name_string.split('_') # get data
    month = name_string[1]
    day = name_string[2]
    date = month + "-" + day

    a = pd.read_csv(f, thousands=",")
    #convert to integers
    a[a.columns[1]] = a[a.columns[1]].astype(float)
    a[a.columns[2]] = a[a.columns[2]].astype(float)
    a[date] = a[a.columns[1]] + a[a.columns[2]]
    a.drop(a.columns[[1,2]], axis=1, inplace=True)

    a.to_csv("all_cases_data/zika_" + date +  ".csv", index=False)


read_all_files = glob.glob("all_cases_data/*")
df = pd.DataFrame({'state' : []})
df.to_csv("all_cases_data/all_clean.csv", index=False)

for k in read_all_files:
    b = pd.read_csv(k, thousands=",")
    c = pd.read_csv("all_cases_data/all_clean.csv", thousands=",")
    merged = pd.merge(b, c, on='state', how='outer')
    merged.fillna(0, inplace=True)
    merged.to_csv("all_cases_data/all_clean.csv",index=False)


cleandata = pd.read_csv("all_cases_data/all_clean.csv", thousands=",").transpose()
cleandata.to_csv("all_cases_data/all_clean.csv",header=False)

df = pd.read_csv("all_cases_data/all_clean.csv", thousands=",")
df.columns = [x.strip().replace(' ', '_') for x in df.columns]
df["us_territories"] = df["American_Samoa"] + df["Puerto_Rico"] + df["US_Virgin_Islands"]
df["us_50_states"] = df.sum(axis=1) - df["us_territories"]*2
df1 = df[['state','us_territories','us_50_states']]
df1.to_csv("all_cases_data/all_clean.csv",index=False)
