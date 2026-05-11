import pandas as pd
import os
from micom import Community

# ----------------------------
# 1. Load diet (same for all)
# ----------------------------
diet = pd.read_csv("mediterranean_FINAL.csv")

# ----------------------------
# 2. Get all *_added.csv files
# ----------------------------
files = [f for f in os.listdir() if f.endswith("_added.csv")]

# ----------------------------
# 3. Loop through each file
# ----------------------------
for file in files:

    print(f"Running: {file}")

    # ----------------------------
    # 1. Load community
    # ----------------------------
    df = pd.read_csv(file)
    df["file"] = "agora_database/" + df["file"]

    # ----------------------------
    # 2. Build model (loads AGORA)
    # ----------------------------
    com = Community(df)

    # ----------------------------
    # 3. Filter metabolites
    # ----------------------------
    valid_exchanges = set(rxn.id for rxn in com.exchanges)
    diet_filtered = diet[diet["reaction"].isin(valid_exchanges)]

    print("Valid metabolites used:", len(diet_filtered))

    # safety check (same logic style as your later code)
    if len(diet_filtered) == 0:
        raise ValueError("No valid metabolites found in diet!")

    # ----------------------------
    # 4. Set medium
    # ----------------------------
    com.medium = diet_filtered.set_index("reaction")["flux"]

    # ----------------------------
    # 5. Run simulation
    # ----------------------------
    solution = com.cooperative_tradeoff(fluxes=True)

    # ----------------------------
    # 6. Save outputs
    # ----------------------------
    base = file.replace(".csv", "")

    solution.members.reset_index().to_csv(
        f"{base}_growth_rates.csv", index=False
    )

    with open(f"{base}_summary.txt", "w") as f:
        f.write(f"Community growth rate: {solution.growth_rate}\n")

    # ----------------------------
    # 7. Save fluxes
    # ----------------------------
    fluxes = solution.fluxes

    if fluxes is not None:
        exchange_fluxes = fluxes.loc[:, fluxes.columns.str.endswith("_m")]
        exchange_fluxes.to_csv(f"{base}_fluxes.csv")
        print("Fluxes saved")
    else:
        print("No fluxes returned")

    # ----------------------------
    print("Simulation complete!")
