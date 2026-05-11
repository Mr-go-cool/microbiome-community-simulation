import pandas as pd

df = pd.read_csv("E1_abundance_final.csv")

# softer filtering for AGORA2
df = df[df["abundance"] > 1e-7]

# re-normalize
df["abundance"] = df["abundance"] / df["abundance"].sum()

df.to_csv("E1_abundance_filtered.csv", index=False)

print(df.head())
print("Number of taxa =", len(df))
print("Sum =", df["abundance"].sum())
