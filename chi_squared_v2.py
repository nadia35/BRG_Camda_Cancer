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

# For each sample ID, fill in a bool indicating whether it had a mutation for that gene
# How do we interpret if it had multiple mutations for one gene?

# Create an empty dataframe, with one row for each sample ID, and one column for each drug

# Fill in for each drug either what their response was, if they were given it, or if they weren't given it, a null indicator

print(mutation)
print(drug)
