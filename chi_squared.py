import pandas as pd
import numpy as np
import re
import scipy.stats
import statsmodels.stats.multitest
import matplotlib.pyplot as plt
import math
import seaborn as sns


def reformat_sample_ID(sample_ID: str) -> str: 
    """Reformat Sample IDs in mutation dataframe to match drug dataframe format. Drop additional "-01" at the end of every ID.

    Arguments:
        sample_ID {str} -- 

    Returns:
        str -- reformatted sample ID
    """
    new_ID = sample_ID[:12]
    return new_ID

def get_chi_dataframe(gene, drug, filtered_patient_intersect):
    """Create a dataframe to run a chi squared test to see if there's a correlation between patient reaction to a drug, and whether a gene was mutated.

    Arguments:
        gene {str} -- the gene we want to analyze for
        drug {str} -- the drug we want to analyze for, from the PreferredDrugName column of filtered_patient_intersect
        filtered_patient_intersect {pandas DataFrame} -- dataframe with SampleID, gene, PreferredDrugName, and Response columns

    Returns:
        pandas DataFrame -- ready for chi squared test
    """
    num_patients = len(patient_intersect.SampleID.unique()) # Get the total number of unique SampleIDs in filtered_patient_intersect dataframe

    chi_dict = {} # This will be the template for the dataframe we return
    responses = patient_intersect.Response.unique() # Get a list of possible response types
    for response in responses:
        chi_dict[response] = [0, 0] # There will be a column for each response type, one row for number of cases that had that response, and a mutation in the specified gene, and another row for the number of cases that had that response, but no mutation

    for response in chi_dict.keys(): # For each response type
        # Pull all samples that have a mutation for that gene, and were given the specified drug, and had the specified response
        cases = filtered_patient_intersect.loc[(filtered_patient_intersect['gene'] == gene) & (filtered_patient_intersect['PreferredDrugName'] == drug) & (filtered_patient_intersect['Response'] == response)].drop_duplicates() 

        num_mutated = len(cases.index.values) # Get the number of samples that match those criteria

        chi_dict[response][0] = num_mutated 
        chi_dict[response][1] += num_patients - num_mutated

    chi_dict['mutated'] = ['yes', 'no'] # Add a column indicating what the row values indicate
    chi_df = pd.DataFrame(chi_dict)
    chi_df.set_index('mutated')
    chi_df.name = gene + ' with ' + drug # Name our dataframe
    return chi_df

# Load our mutation and drug dataframes
mutation = pd.read_csv("mutation_curated_wustl.gz", sep="\t")
drug = pd.read_csv("Drugs_Matched_Entries.tsv", sep="\t")


# Rename "sample" column in mutation dataframe to "SampleID" to match drug dataframe
mutation.rename(columns={"sample": "SampleID"}, inplace=True)

# Reformat SampleIDs
mutation["SampleID"] = mutation["SampleID"].apply(reformat_sample_ID)

# Get the intersection of the two dataframes on the SampleID
patient_intersect = mutation.merge(drug, on="SampleID") 
filtered_patient_intersect = patient_intersect[['SampleID', 'gene', 'PreferredDrugName', 'Response']].drop_duplicates()

# We will choose the genes based on those that are most commonly mutated among the samples.
mutated_gene = mutation[['SampleID', 'gene']].drop_duplicates() # Drop instances of multiple mutations in the same gene for one patient
mutation_freq = mutated_gene['gene'].value_counts()

genes_to_test = list(mutation_freq.head(15).index)

# We will hard-code which drugs to look at.
drugs_to_test = ['Tamoxifen Citrate']

df = get_chi_dataframe(genes_to_test[0], drugs_to_test[0], filtered_patient_intersect)

print(df.name)
print(df)
