import pandas as pd

# ----------------------------
# Load original community
# ----------------------------
df = pd.read_csv("E1_micom_ready.csv")

# ----------------------------
# Scale existing microbes
# ----------------------------
df["abundance"] *= 0.7

# ----------------------------
# Probiotic list (correct names)
# ----------------------------
probiotics = {
    "Bifidobacterium_longum_NCC2705": 0.04,
    "Bifidobacterium_breve_UCC2003_NCIMB8807": 0.04,
    "Bifidobacterium_bifidum_PRL2010": 0.04,
    "Lactobacillus_rhamnosus_GG_ATCC_53103": 0.04,
    "Lactobacillus_acidophilus_NCFM": 0.04,
    "Lactobacillus_plantarum_WCFS1": 0.04,
    "Lactobacillus_reuteri_F275_JCM_1112": 0.04,
    "Lactobacillus_paracasei_subsp_paracasei_ATCC_25302": 0.04,
    "Faecalibacterium_prausnitzii_A2_165": 0.08
}

# ----------------------------
# Add or update
# ----------------------------
for microbe, value in probiotics.items():

    if microbe in df["id"].values:
        print(f"⚠️ Updating {microbe}")
        df.loc[df["id"] == microbe, "abundance"] += value
    else:
        print(f"➕ Adding {microbe}")
        df = pd.concat([
            df,
            pd.DataFrame({
                "id": [microbe],
                "abundance": [value],
                "file": [microbe + ".mat"]
            })
        ], ignore_index=True)

# ----------------------------
# Normalize (CRITICAL)
# ----------------------------
df["abundance"] = df["abundance"] / df["abundance"].sum()

# ----------------------------
# Save
# ----------------------------
df.to_csv("E1_synbiotic_community.csv", index=False)

print("✅ Done")
print("Total:", df["abundance"].sum())
