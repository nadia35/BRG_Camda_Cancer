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
mutation_bools = mutation_bools.fillna(value='_')

# Create an empty dataframe, with one row for each sample ID, and one column for each drug
drug_sample_ids = sorted(drug['SampleID'].drop_duplicates())
drugs = sorted(drug['PreferredDrugName'].drop_duplicates())
drug_reactions = pd.DataFrame(index=drug_sample_ids, columns=drugs)
drug_reactions = drug_reactions.fillna(value='_')

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

combined = mutation_bools.join(drug_reactions, how='inner')
print(combined)
