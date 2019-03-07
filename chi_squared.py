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

# Rename 'sample' column in mutation dataframe to 'SampleID' to match drug dataframe
mutation.rename(columns={'sample': 'SampleID'}, inplace=True)

# Reformat Sample IDs in mutation dataframe to match drug dataframe format

def reformat_sample_ID(sample_ID): # TODO: is this actually the proper way to reformat these? Do we have some documentation we can check?
#    new_ID = sample_ID[:5] + sample_ID[6] + sample_ID[5] + sample_ID[7:12]
    new_ID = sample_ID[:12]
    return new_ID

print(mutation['SampleID'])

mutation['SampleID'] = mutation['SampleID'].apply(reformat_sample_ID)

print(mutation['SampleID'])

# Get the intersection of the two dataframes on the PatientID
patient_intersect = mutation.merge(drug, on='SampleID') 

print(patient_intersect)
