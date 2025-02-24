import pandas as pd
import numpy as np

def sia_score(df, marker = "C1QA"): # C1QA, C1QB, C1QC
    """
    Compute the SIA score from the provided dataframe
    df: normalized gene expression matrix, with gene symbol as the first column or index
    index: whether gene symbols are the row indices of df
    marker: choose from C1QA, C1QB, C1QC as a biomarker for macrophages, by default the expression of C1QA
    """
    genes = df.index
    sig = ["CD8A", marker]
    # test if the two genes are in the dataframe
    if not all(i in list(genes) for i in sig):
        raise ValueError("Genes needed to get the SIA score do not exist in the input data")
    if any(df.loc[marker, :]) == 0:
        raise ValueError(f"Expression of {marker} is 0")

    sia_score = df.loc['CD8A', :]/df.loc[marker, :]

    sia = pd.DataFrame({"SIA":sia_score})
    sia.index = df.columns

    return sia
