import pandas as pd

df = pd.read_csv("mediterranean_diet.csv")
df.columns = ["reaction", "flux"]

# convert [e] ? _m
df["reaction"] = (
    df["reaction"]
    .str.replace("[e]", "_m", regex=False)
)

df.to_csv("mediterranean_FINAL.csv", index=False)

print(df.head())