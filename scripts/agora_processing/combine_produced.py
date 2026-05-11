import pandas as pd
import glob
import os

files = glob.glob("*_produced.csv")

data = {}

for f in files:
    df = pd.read_csv(f)
    microbe = f.replace("_produced.csv", "")
    
    mets = df["Name"].str.lower().tolist()
    
    for m in mets:
        if m not in data:
            data[m] = {}
        data[m][microbe] = 1

# convert to dataframe
combined = pd.DataFrame.from_dict(data, orient="index").fillna(0)

# reset index
combined.reset_index(inplace=True)
combined.rename(columns={"index": "Metabolite"}, inplace=True)

# save
combined.to_csv("combined_produced.csv", index=False)

print("combined_produced.csv created")
