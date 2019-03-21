import pandas as pd
import numpy as np
import re
import scipy.stats
import statsmodels.stats.multitest
import matplotlib.pyplot as plt
import math
import seaborn as sns

# Load our mutation and drug dataframes
mutation = pd.read_csv("mutation_curated_wustl.gz", sep="\t")
drug = pd.read_csv("Drugs_Matched_Entries.tsv", sep="\t")


# Rename "sample" column in mutation dataframe to "SampleID" to match drug dataframe
mutation.rename(columns={"sample": "SampleID"}, inplace=True)


def reformat_sample_ID(sample_ID: str) -> str: 
    """Reformat Sample IDs in mutation dataframe to match drug dataframe format. Drop additional "-01" at the end of every ID.

    Arguments:
        sample_ID {str} -- 

    Returns:
        str -- reformatted sample ID
    """
    new_ID = sample_ID[:12]
    return new_ID

mutation["SampleID"] = mutation["SampleID"].apply(reformat_sample_ID)


# Get the intersection of the two dataframes on the SampleID
patient_intersect = mutation.merge(drug, on="SampleID") 
filtered_patient_intersect = patient_intersect[['SampleID', 'gene', 'PreferredDrugName', 'Response']].drop_duplicates()

# We will choose the genes based on those that are most commonly mutated among the samples.
mutated_gene = mutation[['SampleID', 'gene']].drop_duplicates() # Drop instances of multiple mutations in the same gene for one patient
mutation_freq = mutated_gene['gene'].value_counts()

genes_to_test = list(mutation_freq.head(15).index)
print(genes_to_test)

# We will hard-code which drugs to look at.
drugs_to_test = ['Tamoxifen Citrate']

# For each gene/drug combination, create our chi squared test dataframe. Put all the dataframes in a dictionary. One dict for each gene, and each key is a drug name, and the value is a list, the first element being the input dataframe, and the remaining elements being the results of the test

template_chi_dict = {}
responses = patient_intersect.Response.unique()
for response in responses:
    template_chi_dict[response] = [0, 0]

prep_dict = {}
num_patients = len(patient_intersect.SampleID.unique())
print(num_patients)

for gene in genes_to_test:
    if gene in prep_dict.keys():
        raise ValueError('Duplicate genes in genes_to_test')
    prep_dict[gene] = {}
    for drug in drugs_to_test:
        if drug in prep_dict[gene].keys():
            raise ValueError('Duplicates in drugs_to_test')
        chi_dict = template_chi_dict.copy()
        for response in chi_dict.keys():
            cases = filtered_patient_intersect.loc[(filtered_patient_intersect['gene'] == gene) & (filtered_patient_intersect['PreferredDrugName'] == drug) & (filtered_patient_intersect['Response'] == response)].drop_duplicates()
            num_mutated = len(cases.index.values)
            chi_dict[response][0] += num_mutated # These numbers are incorrect...
            chi_dict[response][1] += num_patients - num_mutated
        chi_dict['is_mutated'] = ['yes', 'no']
        chi_df = pd.DataFrame(chi_dict)
        chi_df.name = gene + ' with ' + drug
        prep_dict[gene][drug] = chi_df

for gene in prep_dict.keys():
    print(gene)
    for drug in prep_dict[gene].keys():
        print(prep_dict[gene][drug].name)
        print(prep_dict[gene][drug])
