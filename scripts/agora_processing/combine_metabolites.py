import pandas as pd
import glob

files = glob.glob("*_all_metabolites.csv")

data = {}

for f in files:
    df = pd.read_csv(f)
    microbe = f.replace("_all_metabolites.csv", "")
    
    mets = df["Name"].str.lower().tolist()
    
    for m in mets:
        if m not in data:
            data[m] = {}
        data[m][microbe] = 1

combined = pd.DataFrame.from_dict(data, orient="index").fillna(0)

combined.reset_index(inplace=True)
combined.rename(columns={"index": "Metabolite"}, inplace=True)

combined.to_csv("combined_metabolites.csv", index=False)

print("combined_metabolites.csv created")
