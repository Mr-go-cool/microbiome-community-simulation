import pandas as pd

# -----------------------------
# ALL PROBIOTICS (MASTER LIST)
# -----------------------------

probiotics = [
    {"id": "Bifidobacterium_longum", "file": "Bifidobacterium_longum_NCC2705.mat"},
    {"id": "Lactobacillus_brevis", "file": "Lactobacillus_brevis_ATCC_367.mat"},
    {"id": "Lactobacillus_reuteri", "file": "Lactobacillus_reuteri_DSM_20016.mat"},
    {"id": "Lactobacillus_acidophilus", "file": "Lactobacillus_acidophilus_NCFM.mat"},
    {"id": "Lactobacillus_paracasei", "file": "Lactobacillus_paracasei_subsp_paracasei_ATCC_25302.mat"},
    {"id": "Lactobacillus_salivarius", "file": "Lactobacillus_salivarius_salivarius_UCC118.mat"},
    {"id": "Bifidobacterium_breve", "file": "Bifidobacterium_breve_UCC2003_NCIMB8807.mat"},
    {"id": "Lactobacillus_johnsonii", "file": "Lactobacillus_johnsonii_NCC_533.mat"},
    {"id": "Lactobacillus_fermentum", "file": "Lactobacillus_fermentum_ATCC_14931.mat"},
    {"id": "Bacillus_subtilis", "file": "Bacillus_subtilis_str_168.mat"},
    {"id": "Lactobacillus_rhamnosus", "file": "Lactobacillus_rhamnosus_GG_ATCC_53103.mat"},
    {"id": "Bifidobacterium_animalis", "file": "Bifidobacterium_animalis_lactis_BB_12.mat"},
    {"id": "Lactobacillus_plantarum", "file": "Lactobacillus_plantarum_WCFS1.mat"},
    {"id": "Streptococcus_thermophilus", "file": "Streptococcus_thermophilus_LMD_9.mat"},
    {"id": "Bifidobacterium_bifidum", "file": "Bifidobacterium_bifidum_PRL2010.mat"},
    {"id": "Lactobacillus_amylovorus", "file": "Lactobacillus_amylovorus_GRL_1112.mat"},
    {"id": "Lactobacillus_delbrueckii", "file": "Lactobacillus_delbrueckii_subsp_bulgaricus_ATCC_11842.mat"},
    {"id": "Lactobacillus_helveticus", "file": "Lactobacillus_helveticus_DPC_4571.mat"}
]


TOTAL_PROBIOTIC_ABUNDANCE = 0.2   # 20% of community
EACH_ABUNDANCE = TOTAL_PROBIOTIC_ABUNDANCE / len(probiotics)

# -----------------------------
# 2. Load baseline
# -----------------------------
df = pd.read_csv("E1_micom_ready.csv")

# normalize first
df["abundance"] = df["abundance"] / df["abundance"].sum()

# -----------------------------
# 3. Remove existing probiotics (avoid duplicates)
# -----------------------------
existing_ids = [p["id"] for p in probiotics]
df = df[~df["id"].isin(existing_ids)]

# -----------------------------
# 4. Scale remaining microbes
# -----------------------------
df["abundance"] *= (1 - TOTAL_PROBIOTIC_ABUNDANCE)

# -----------------------------
# 5. Add probiotics
# -----------------------------
new_rows = []

for p in probiotics:
    row = {
        "id": p["id"],
        "abundance": EACH_ABUNDANCE,
        "file": p["file"]
    }

    # handle extra columns safely
    for col in df.columns:
        if col not in row:
            row[col] = None

    new_rows.append(row)

probiotic_df = pd.DataFrame(new_rows)[df.columns]

df = pd.concat([df, probiotic_df], ignore_index=True)

# -----------------------------
# 6. Final normalization safety
# -----------------------------
df["abundance"] = df["abundance"] / df["abundance"].sum()

# -----------------------------
# 7. Save
# -----------------------------
df.to_csv("Blend_6_probiotics_added.csv", index=False)

print("✅ Multi-probiotic community ready")
print(df.tail())

# debug check
print("\nProbiotics added:")
print(df[df["id"].isin(existing_ids)])

print("\nTotal sum:", df["abundance"].sum())



#Want unequal proportions?
#probiotics = [
#    {"id": "Bifidobacterium_longum_NCC2705", "file": "...", "abundance": 0.1},
#    {"id": "Lactobacillus_rhamnosus_GG", "file": "...", "abundance": 0.07},
#    {"id": "Bacteroides_fragilis_YCH46", "file": "...", "abundance": 0.03}
#]
