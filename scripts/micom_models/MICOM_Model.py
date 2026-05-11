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
# 3. Run simulation WITH FLUXES
# ----------------------------
solution = com.cooperative_tradeoff(fluxes=True)

# ----------------------------
# 4. Save growth rates
# ----------------------------
result = solution.members.copy().reset_index()
result.to_csv("E1_growth_rates_try_2.csv", index=False)

# ----------------------------
# 5. Save summary
# ----------------------------
with open("E1_summary_try_2.txt", "w") as f:
    f.write(f"Community growth rate: {solution.growth_rate}\n")

# ----------------------------
# 6. Save fluxes (FIXED)
# ----------------------------
fluxes = solution.fluxes

if fluxes is not None:
    exchange_fluxes = fluxes.loc[:, fluxes.columns.str.startswith("EX_")]
    exchange_fluxes.to_csv("E1_fluxes_default_try_2.csv")
    print("✅ Fluxes saved")
else:
    print("⚠️ No fluxes returned")

# ----------------------------
# DONE
# ----------------------------
print("✅ Simulation complete!")
print("📂 Files saved:")
print("- E1_growth_rates__try_2.csv")
print("- E1_summary_try_2.txt")
print("- E1_fluxes_default_try_2.csv")
