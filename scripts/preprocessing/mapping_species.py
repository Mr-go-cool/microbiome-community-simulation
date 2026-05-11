import pandas as pd
import os

df = pd.read_csv("E1_abundance_top200.csv")

model_path = "agora_database"
model_files = os.listdir(model_path)

def find_representative_model(taxon):
    matches = [m for m in model_files if taxon in m]
    if len(matches) > 0:
        return matches[0]   # pick first strain
    return None

df["file"] = df["taxon"].apply(find_representative_model)

# remove taxa with no model
df = df.dropna(subset=["file"])

# renormalize
df["abundance"] = df["abundance"] / df["abundance"].sum()

# rename for MICOM
df = df.rename(columns={"taxon": "id"})

df.to_csv("E1_micom_ready.csv", index=False)

print(df.head())
print("Number of taxa =", len(df))
