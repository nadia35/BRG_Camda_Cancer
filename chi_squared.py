import pandas as pd
import numpy as np
import re
import scipy.stats
import statsmodels.stats.multitest
import matplotlib.pyplot as plt
import math
import seaborn as sns

# Load our mutation and drug dataframes
mutation = pd.read_csv('mutation_curated_wustl.gz', sep='\t')
drug = pd.read_csv('Drugs_Matched_Entries.tsv', sep='\t')

# Rename index column in mutation dataframe from 'sample' to 'SampleID' to match drug
mutation.rename(columns={'sample': 'SampleID'}, inplace=True)

print(mutation) # temp
print(drug) # temp

# Get the intersection of the two dataframes on the PatientID
# Right now this returns an empty dataframe, because we need to reformat the SampleIDs to batch between the two tables.
patient_intersect = mutation.merge(drug, on='SampleID') 

print(patient_intersect) # temp

# all below is temporary
mutation_samples = mutation['SampleID'].tolist()
drug_samples = drug['SampleID'].tolist()

print("starting sample compare...")
for sample in mutation_samples:
    if sample in drug_samples:
        print(sample)

print("finished sample compare.")
