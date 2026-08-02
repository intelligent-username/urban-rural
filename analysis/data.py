"""
Data Preparation: standardization, clipping, segmentation, etc. that happens prior to training in order to ensure numerical stability.
"""

from modulefinder import test

import numpy as np
import pandas as pd
from typing import tuple

def import_data(file_path: str = "") -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Imports data from a CSV file and returns it as 3 NumPy arrays.

    The first array is the training split the second is the validation split, and the third is the test split. They make up 90, 5, and 5 percent of the data respectively. The data is standardized before being split.

    WHEN USING THE MODEL, ensure the SAME pre-processing is applied to the raw inputs for unseen data. Don't pass raw user input into the model.

    """
    data = pd.read_csv(file_path)
    print("Succesfully imported data.")
    print("Data shape:", data.shape)
    print(f"So, we have {data.shape[0]} samples, each with {data.shape[1] - 1} features and 1 target.")
    print("Sample data:\n", data.head())


    print("Splitting data...")

    train, val, test = split_data(data)

    print("Standardizing...")

    train, val, test = standardize_data(train, val, test)

    print("Done. Start training!")

    return (train, test, val)

def standardize_data(train: pd.DataFrame, val: pd.DataFrame, test: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Standardizes the data in-place to have a mean of 0 and a standard deviation of 1. for numerical stability. Categorical columns are not standardized.
    Modifies the data in-place.
    """

    mu = train.mean(numeric_only=True)
    sigma = train.std(numeric_only=True)

    train[mu.index] = (train[mu.index] - mu) / sigma
    val[mu.index] = (val[mu.index] - mu) / sigma
    test[mu.index] = (test[mu.index] - mu) / sigma

    return (train, val, test)


def split_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Breaks data into training, valdation, and test sets. Returns a tuple of (train, val, test).
    """

    n = len(df)
    train_portion = int(0.9 * n)
    val_frac = train_portion + int(0.05 * n)

    rng = np.random.default_rng(seed=42)
    orders = rng.permutation(n)

    train = df.iloc[orders[:train_portion]]
    val = df.iloc[orders[train_portion:val_frac]]
    test = df.iloc[orders[val_frac:]]


    return (train, val, test)
