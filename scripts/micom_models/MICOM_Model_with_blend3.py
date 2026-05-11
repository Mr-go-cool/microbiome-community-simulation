import pandas as pd
from micom import Community

# ----------------------------
# 1. Load community (BLEND 3)
# ----------------------------
df = pd.read_csv("E1_with_blend3.csv")
df["file"] = "agora_database/" + df["file"]

# ----------------------------
# 2. Build model
# ----------------------------
com = Community(df)

# ----------------------------
# 3. Load diet
# ----------------------------
diet = pd.read_csv("mediterranean_FINAL.csv")

# ----------------------------
# 4. Filter metabolites
# ----------------------------
valid_exchanges = set(rxn.id for rxn in com.exchanges)
diet = diet[diet["reaction"].isin(valid_exchanges)]

print("Valid metabolites:", len(diet))

# ----------------------------
# 5. Set medium
# ----------------------------
com.medium = diet.set_index("reaction")["flux"]

# ----------------------------
# 6. Run simulation
# ----------------------------
solution = com.cooperative_tradeoff(fluxes=True)

# ----------------------------
# 7. Save outputs
# ----------------------------
solution.members.reset_index().to_csv(
    "E1_growth_rates_blend3.csv", index=False
)

with open("E1_summary_blend3.txt", "w") as f:
    f.write(f"Community growth rate: {solution.growth_rate}\n")

if solution.fluxes is not None:
    solution.fluxes.loc[:, solution.fluxes.columns.str.endswith("_m")]\
        .to_csv("E1_fluxes_blend3.csv")

print("✅ Blend 3 simulation complete!")
