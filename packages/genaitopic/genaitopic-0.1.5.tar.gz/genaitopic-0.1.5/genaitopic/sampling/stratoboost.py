"""
Module: getstrata
Provides functions for performing stratified sampling with bootstraps.
"""

from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd

def stratified_sampling_with_bootstraps(data, demographics_col, n, k, fraction, replacement=True):
    """
    Perform stratified sampling and create bootstrap samples for each stratum.
    
    Parameters:
        data (pd.DataFrame): Dataset.
        demographics_col (str): Column for stratification.
        n (int): Number of strata splits.
        k (int): Number of samples per stratum.
        fraction (float): Fraction of each stratum to sample.
        replacement (bool): Whether to sample with replacement.
    
    Returns:
        dict: Mapping of stratum IDs to lists of sampled DataFrames.
    """
    sss = StratifiedShuffleSplit(n_splits=n, test_size=fraction, random_state=42)
    strata = {}
    
    for stratum_id, (_, test_index) in enumerate(sss.split(data, data[demographics_col])):
        stratum_data = data.iloc[test_index]
        samples = []
        for _ in range(k):
            if replacement:
                sample = stratum_data.sample(n=len(stratum_data), replace=True)
            else:
                sample = stratum_data.sample(frac=fraction, random_state=42)
            samples.append(sample)
        strata[f'S{stratum_id + 1}'] = samples
    return strata
