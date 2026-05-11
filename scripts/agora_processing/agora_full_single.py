from cobra.io import load_matlab_model
import sys
import pandas as pd
import os

# ===== INPUT =====
model_path = sys.argv[1]
model_name = os.path.basename(model_path).replace(".mat", "")

# ===== LOAD MODEL =====
model = load_matlab_model(model_path)

# ===== BASIC INFO =====
total_rxns = len(model.reactions)
total_mets = len(model.metabolites)
total_genes = len(model.genes)

# ===== ALL DATA =====
all_mets = [(m.id, m.name) for m in model.metabolites]
all_rxns = [(r.id, r.reaction) for r in model.reactions]
all_genes = [(g.id,) for g in model.genes]

# ===== EXCHANGE REACTIONS =====
exchange_rxns = [rxn for rxn in model.reactions if rxn.id.startswith("EX_")]

# ===== RUN FBA =====
solution = model.optimize()
growth_rate = solution.objective_value

# ===== FLUX ANALYSIS =====
produced = []
consumed = []

for rxn in exchange_rxns:
    flux = solution.fluxes.get(rxn.id, 0)
    met = list(rxn.metabolites.keys())[0]

    if flux > 0:
        produced.append((met.id, met.name, flux))
    elif flux < 0:
        consumed.append((met.id, met.name, flux))

# ===== COUNTS =====
num_produced = len(produced)
num_consumed = len(consumed)

# ===== PRINT SUMMARY =====
print("\n===== MICROBE SUMMARY =====")
print("Model:", model_name)
print("Reactions:", total_rxns)
print("Metabolites:", total_mets)
print("Genes:", total_genes)
print("Exchange reactions:", len(exchange_rxns))
print("Produced metabolites:", num_produced)
print("Consumed metabolites:", num_consumed)
print("Growth rate:", growth_rate)

# ===== SAVE ALL FILES =====
pd.DataFrame(all_mets, columns=["ID", "Name"]).to_csv(f"{model_name}_all_metabolites.csv", index=False)
pd.DataFrame(all_rxns, columns=["ID", "Reaction"]).to_csv(f"{model_name}_all_reactions.csv", index=False)
pd.DataFrame(all_genes, columns=["Gene"]).to_csv(f"{model_name}_all_genes.csv", index=False)

pd.DataFrame(produced, columns=["ID", "Name", "Flux"]).to_csv(f"{model_name}_produced.csv", index=False)
pd.DataFrame(consumed, columns=["ID", "Name", "Flux"]).to_csv(f"{model_name}_consumed.csv", index=False)

# ===== SUMMARY FILE =====
summary = pd.DataFrame([{
    "Model": model_name,
    "Reactions": total_rxns,
    "Metabolites": total_mets,
    "Genes": total_genes,
    "Exchange_Reactions": len(exchange_rxns),
    "Produced_Count": num_produced,
    "Consumed_Count": num_consumed,
    "Growth_Rate": growth_rate
}])

summary.to_csv(f"{model_name}_summary.csv", index=False)

print("\nFiles saved:")
print(f"{model_name}_all_metabolites.csv")
print(f"{model_name}_all_reactions.csv")
print(f"{model_name}_all_genes.csv")
print(f"{model_name}_produced.csv")
print(f"{model_name}_consumed.csv")
print(f"{model_name}_summary.csv")
