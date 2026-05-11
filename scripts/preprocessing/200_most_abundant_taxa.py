import pandas as pd

df = pd.read_csv("E1_abundance_final.csv")

# sort by abundance
df = df.sort_values(by="abundance", ascending=False)

# keep top 200 taxa
df = df.head(200)

# re-normalize
df["abundance"] = df["abundance"] / df["abundance"].sum()

# save
df.to_csv("E1_abundance_top200.csv", index=False)

print(df.head())
print("Number of taxa =", len(df))
print("Sum =", df["abundance"].sum())
