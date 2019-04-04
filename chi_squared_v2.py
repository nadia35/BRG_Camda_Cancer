import pandas as pd

def reformat_sample_ID(sample_ID: str) -> str:
    """Reformat Sample IDs in mutation dataframe to match drug dataframe format. Drop additional "-01" at the end of every ID.

    Arguments:
        sample_ID {str} --

    Returns:
        str -- reformatted sample ID
    """
    new_ID = sample_ID[:12]
    return new_ID

# Load our mutation and drug dataframes
mutation = pd.read_csv("mutation_curated_wustl.gz", sep="\t")
drug = pd.read_csv("Drugs_Matched_Entries.tsv", sep="\t")

# Rename "sample" column in mutation dataframe to "SampleID" to match drug dataframe
mutation.rename(columns={"sample": "SampleID"}, inplace=True)

# Reformat SampleIDs in mutation dataframe
mutation["SampleID"] = mutation["SampleID"].apply(reformat_sample_ID)

# Create an empty dataframe, with one row for each sample ID, and one column for each gene
mutation_sample_ids = sorted(mutation['SampleID'].drop_duplicates())
genes = sorted(mutation['gene'].drop_duplicates())
mutation_bools = pd.DataFrame(index=mutation_sample_ids, columns=genes)
mutation_bools = mutation_bools.fillna(value=False)

# Create an empty dataframe, with one row for each sample ID, and one column for each drug
drug_sample_ids = sorted(drug['SampleID'].drop_duplicates())
drugs = sorted(drug['PreferredDrugName'].drop_duplicates())
drug_reactions = pd.DataFrame(index=drug_sample_ids, columns=drugs)
drug_reactions = drug_reactions.fillna(value='Not_administered')

# Iterate through the mutation dataframe, and for all samples that have a mutation for a gene, replace False with True in mutation_bools
for sample_id in mutation_sample_ids:
    slice = mutation.loc[mutation['SampleID'] == sample_id]
    for gene in slice['gene']:
        mutation_bools.at[sample_id, gene] = True

# Iterate through the drug dataframe, and for all samples that were given a particular drug, replace 'Not_administered' with what their response was.
for sample_id in drug_sample_ids:
    slice = drug.loc[drug['SampleID'] == sample_id]
    for drug_name in slice['PreferredDrugName']:
        reactions = drug.loc[(drug['SampleID'] == sample_id) & (drug['PreferredDrugName'] == drug_name)]['Response']
        if len(reactions) > 0:
            reaction = reactions.iloc[0] # What should we do when there's more than one reaction?
            drug_reactions.at[sample_id, drug_name] = reaction 

print(mutation_bools)
print(drug_reactions)

# Below is the first way I solved the problem, by iterating through the mutation_bools and drug_reactions dataframes
# However, because the majority of the entries stayed at False or 'Not_administered' respectively, this approach took forever and was a waste of time.

## For each sample ID in the mutation_bools dataframe, fill in a bool indicating whether it had at least one mutation for that gene
#for sample_id in mutation_bools.index:
#    for gene in mutation_bools.columns:
#        mutated = False
#        if len(mutation.loc[(mutation['gene'] == gene) & (mutation['SampleID'] == sample_id)]) > 0:
#            mutated = True
#        mutation_bools.at[sample_id, gene] = mutated
#        print(mutated)
#
## Fill in for each drug either what their response was, if they were given it, or if they weren't given it, a null indicator
#for sample_id in drug_reactions.index:
#    for drug_name in drug_reactions.columns:
#        reactions = drug.loc[(drug['SampleID'] == sample_id) & (drug['PreferredDrugName'] == drug_name)]['Response']
#        if len(reactions) > 0:
#            reaction = reactions.iloc[0] # What should we do when there's more than one reaction?
#            drug_reactions.at[sample_id, drug_name] = reaction 
#            print(reaction)

