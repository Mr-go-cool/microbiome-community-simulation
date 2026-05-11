import pandas as pd

# load cleaned file
df = pd.read_csv("E1_abundance_clean.csv")

# keep only non-zero abundance
df = df[df["abundance"] > 0]

# re-normalize again
df["abundance"] = df["abundance"] / df["abundance"].sum()

# save
df.to_csv("E1_abundance_final.csv", index=False)

print(df.head())
print("Number of taxa =", len(df))
print("Sum =", df["abundance"].sum())
