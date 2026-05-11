import pandas as pd

# ----------------------------
# Load diet
# ----------------------------
diet = pd.read_csv("mediterranean_FINAL.csv")

# ----------------------------
# Prebiotic inputs
# ----------------------------
prebiotics = {
    "EX_glc_D_m": 20,
    "EX_fru_m": 10,
    "EX_inulin_m": 10,
    "EX_pect_m": 10
}

# ----------------------------
# Add or update
# ----------------------------
for rxn, flux in prebiotics.items():

    if rxn in diet["reaction"].values:
        print(f"⚠️ Updating {rxn}")
        diet.loc[diet["reaction"] == rxn, "flux"] = flux
    else:
        print(f"➕ Adding {rxn}")
        diet = pd.concat([
            diet,
            pd.DataFrame({"reaction": [rxn], "flux": [flux]})
        ], ignore_index=True)

# ----------------------------
# Save
# ----------------------------
diet.to_csv("mediterranean_synbiotic.csv", index=False)

print("✅ Diet ready")
