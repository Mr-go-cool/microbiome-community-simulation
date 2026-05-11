import pandas as pd

# load your file
df = pd.read_csv("E1_abundance.csv")

# remove SGB part
df["taxon"] = df["taxon"].str.replace(r"_SGB.*", "", regex=True)

# group again (important: duplicates will merge)
df = df.groupby("taxon", as_index=False).sum()

# re-normalize
df["abundance"] = df["abundance"] / df["abundance"].sum()

# save cleaned file
df.to_csv("E1_abundance_clean.csv", index=False)

print(df.head())
print("Sum =", df["abundance"].sum())
