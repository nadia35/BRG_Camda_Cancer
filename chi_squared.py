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
gene = input("Please indicate the desired gene. (For options, pass 'options'): ").upper()
while gene == 'OPTIONS':
    print(patient_intersect["gene"]) # Need to figure out how to get rid of duplicates
    gene = input("Please indicate the desired gene. (For options, pass 'options'): ").upper()

drug = input("Thank you. Please indicate the desired drug. (For options, pass 'options'): ").title()
while drug == 'Options':
    print(patient_intersect["PreferredDrugName"]) # Need to figure out how to get rid of duplicates
    drug = input("Please indicate the desired drug. (For options, pass 'options'): ").title()

print(gene, drug)
