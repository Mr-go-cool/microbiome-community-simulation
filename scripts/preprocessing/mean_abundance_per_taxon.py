import pandas as pd

# load file
df = pd.read_csv("otu_table_Strain_Enterotype_DMM1_relative_abundance.csv")

# remove SampleID column
df = df.drop(columns=["SampleID"])

# take mean across all samples (this = one enterotype)
mean_abundance = df.mean(axis=0)

# convert to dataframe
mean_df = mean_abundance.reset_index()
mean_df.columns = ["taxon", "abundance"]

# normalize (important)
mean_df["abundance"] = mean_df["abundance"] / mean_df["abundance"].sum()

# save
mean_df.to_csv("E1_abundance.csv", index=False)

print(mean_df.head())
print("Sum =", mean_df["abundance"].sum())
