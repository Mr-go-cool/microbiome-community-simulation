import pandas as pd
from micom import Community

# ----------------------------
# 1. Load input data
# ----------------------------
df = pd.read_csv("E1_micom_ready.csv")
df["file"] = "agora_database/" + df["file"]

# ----------------------------
# 2. Build community model
# ----------------------------
com = Community(df)

# ----------------------------
# 3. Load Mediterranean diet
# ----------------------------
diet = pd.read_csv("mediterranean_FINAL.csv")

# ----------------------------
# 4. FILTER valid metabolites
# ----------------------------
valid_exchanges = set(rxn.id for rxn in com.exchanges)

diet = diet[diet["reaction"].isin(valid_exchanges)]

print("Valid metabolites used:", len(diet))
print("Example:\n", diet.head())

# safety check
if len(diet) == 0:
    raise ValueError("No valid metabolites found in diet!")

# ----------------------------
# 5. SET DIET
# ----------------------------
com.medium = diet.set_index("reaction")["flux"]

# ----------------------------
# 6. Run simulation (WITH FLUX)
# ----------------------------
solution = com.cooperative_tradeoff(fluxes=True)

# ----------------------------
# 7. Save growth rates
# ----------------------------
result = solution.members.copy().reset_index()
result.to_csv("E1_growth_rates_mediterranean.csv", index=False)

# ----------------------------
# 8. Save summary
# ----------------------------
with open("E1_summary_mediterranean.txt", "w") as f:
    f.write(f"Community growth rate: {solution.growth_rate}\n")

# ----------------------------
# 9. Flux analysis (FIXED)
# ----------------------------
fluxes = solution.fluxes

if fluxes is not None:
    # only take medium fluxes (_m)
    exchange_fluxes = fluxes.loc[:, fluxes.columns.str.endswith("_m")]
    exchange_fluxes.to_csv("E1_fluxes_mediterranean.csv")
    print("Fluxes saved")
else:
    print("No fluxes returned")

# ----------------------------
# DONE
# ----------------------------
print(" Mediterranean simulation complete!")
print("Files saved:")
print("- E1_growth_rates_mediterranean.csv")
print("- E1_summary_mediterranean.txt")
print("- E1_fluxes_mediterranean.csv")