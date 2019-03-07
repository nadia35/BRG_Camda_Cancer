import pandas as pd
import numpy as np
import re
import scipy.stats
import statsmodels.stats.multitest
import matplotlib.pyplot as plt
import math
import seaborn as sns

# Load our mutation and drug dataframes
mutation = pd.read_csv('mutation_curated_wustl', sep='\t')
drug = pd.read_csv('Drugs_Matched_Entries.tsv', sep='\t')

# Rename index column in mutation dataframe from 'sample' to 'SampleID' to match drug

# Get the intersection of the two dataframes on the PatientID
patient_intersect = mutation.merge(drug, on='SampleID')
