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


# Reformat Sample IDs in mutation dataframe to match drug dataframe format. Drop additional "-01" at the end of every ID.
def reformat_sample_ID(sample_ID): 
    new_ID = sample_ID[:12]
    return new_ID

mutation["SampleID"] = mutation["SampleID"].apply(reformat_sample_ID)


# Get the intersection of the two dataframes on the SampleID
patient_intersect = mutation.merge(drug, on="SampleID") 

# We want to create a dataframe where, for a particular gene and drug, each entry is the number of people of a particular genotype (either mutated or non-mutated) who had that particular drug reaction. Thus, the columns will correspond to the different reactions, and the rows will correspond to the genotype--one row for mutated, and one for non-mutated.

# How are we going to get user input? Probably too complicated to make a Python package. Terminal input?
gene = ''

while gene == '':
    input_gene = input("Please enter gene for analysis: ").upper()
    if input_gene in patient_intersect['gene'].values:
        gene = input_gene
    elif input_gene == "OPTIONS":
        for gene_opt in sorted(set(patient_intersect['gene'].values)):
            print(gene_opt)
    else:
        print("Gene not found in dataframe. Pass 'options' to view options.")

drug = ''

while drug == '':
    input_drug = input("Please enter drug for analysis: ").title()
    if input_drug in patient_intersect['PreferredDrugName'].values:
        drug = input_drug
    elif input_drug == "Options":
        for drug_opt in sorted(set(patient_intersect['PreferredDrugName'].values)):
            print(drug_opt)
    else:
        print("Drug not found in dataframe. Pass 'options' to view options.")

print(gene, drug)
