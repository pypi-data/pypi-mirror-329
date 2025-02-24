import pandas as pd
import numpy as np
import os
from cmapPy.pandasGEXpress.parse_gct import parse
from rnanorm import TMM
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from inmoose.pycombat import pycombat_seq
import warnings



def read_data(path):
    """
    Format: supports txt, csv, gct input
    Input: gene expression matrix with gene symbol as the first column, samples in columns and gene symbols in rows. 
           Duplicated or missing genes are not allowed.
    Output: a pandas dataframe where gene symbols are the row index and samples are columns
    """
    # gct, txt, csv, first column as genes
    _, file_extension = os.path.splitext(path)
    if file_extension == '.txt':
        df = pd.read_table(path, sep = "\t", index_col=0) 

    elif file_extension == '.csv':
        df = pd.read_csv(path, index_col=0)

    elif file_extension == '.gct':
        df = parse(path)
        df = df.data_df

    else:
        raise TypeError(file_extension + " file is not supported")

    genes = df.index
    if genes.duplicated().any():
        dup_genes = genes[genes.duplicated()]
        warn = str("Duplicate genes: " + dup_genes.unique())
        warnings.warn(warn, category=UserWarning)
    
    if genes.isnull().any():
        warnings.warn("Exist NA's in the input genes", category=UserWarning)

    return (df)


def normalization(df = None, path = None, method = None, minmax = False, zscore = False, batch = None, batch_col = None): 
    """
    Perform normalization and batch effect correction to the input. The input must be a pandas dataframe or a valid path.
    Method: choose method from TMM, CPM, median ratio for read count data. Default to None for normalized gene expression.
    minmax: perform min-max normalization, set to False by default
    zscore: perform z-score normalization, set to False by default
    batch: a pandas dataframe having batch information for the gene expression data to perform batch effect correction, with row index as sample ID
    batch_col: column name of the batch information, must be a string
    """

    # read data from path if path exists
    if path is not None:
        df = read_data(path)
    else:
        if df is None:
            raise ValueError("Invalid input pandas dataframe and path")
        elif not isinstance(df, pd.DataFrame):
            raise TypeError("The input should be a pandas dataframe")

    # test whether the first column is genes
    first_col = df.iloc[:,0]
    has_letters = first_col.apply(lambda x: any(char.isalpha() for char in str(x)))
    if has_letters.all():
        df1 = df.copy()
        df1.index = first_col
        df1 = df1.iloc[:,1:]
    else:
        ind_letters = df.index.to_series().apply(lambda x: any(char.isalpha() for char in str(x)))
        if not ind_letters.any():
            raise ValueError("Index contains invalid gene name. Gene symbols must be in the first column or row index")
        else:
            df1 = df.copy()

    # fill NA's with 0 count
    df1 = df1.fillna(0)

    # read count normalization
    if method is not None:

        if method == 'TMM':
            # calculate TMM
            norm = TMM().fit(df1.T)
            gene_norm = norm.transform(df1.T)
            gene_norm = pd.DataFrame(gene_norm).T
            gene_norm.columns = df1.columns
            gene_norm.index = df1.index
            print("---------- data has been TMM normalized ----------")
        elif method == 'CPM':
            column_sums = df1.sum(axis=0)
            # calculate CPM
            gene_norm = (df1 / column_sums) * 1e6
            gene_norm.index = df1.index
            print("---------- data has been CPM normalized ----------")
        elif method == 'median ratio':
            # compute geometric means of each gene
            geo_means = np.exp(np.log(df1.replace(0, np.nan)).mean(axis=1))
            ratios = df1.div(geo_means, axis=0)
            # calculate the median of the ratios for each sample
            medratio = ratios.median(axis=0)
            medratio1 = medratio.replace(0, 1e-06)
            gene_norm = df1.div(medratio1, axis=1)
            gene_norm.index = df1.index
            print("---------- data has been median ratio normalized ----------")
        else:
            raise TypeError("Normalization method not supported")
        
    df_norm = gene_norm if 'gene_norm' in locals() else df1
    # remove incorrectly formatted rows
    df_norm = df_norm[~pd.to_datetime(df_norm.index, errors='coerce').notna()]

    # z-score normalization
    if zscore:
        scalar = StandardScaler()
        df_norm = pd.DataFrame(scalar.fit_transform(df_norm.T).T,  # Transpose to scale across rows (genes)
                                  index=df_norm.index, columns=df_norm.columns)
        print("---------- data has been z-score normalized ----------")

    # min-max normalization
    if minmax:
        min_max_scaler = MinMaxScaler(feature_range=(0, 1))  # Adjust range as needed
        df_norm = pd.DataFrame(min_max_scaler.fit_transform(df_norm.T).T,  # Transpose to scale across rows (genes)
                                        index=df_norm.index, columns=df_norm.columns)
        print("---------- data has been min-max normalized ----------")
    

    if batch is not None:
        if not isinstance(batch_col, str):
            raise TypeError("batch_col must be a string")
        # replace negative expression values to the absolute values
        df_norm = df_norm.abs()
        warnings.warn("Negative gene expression exists in the dataframe", category=UserWarning)

        # reorder batch by the order of the gene expression matrix columns
        common_ID = set(df_norm.columns) & set(batch.index)
        df_norm = df_norm[list(common_ID)]
        common_batch = batch.loc[list(common_ID),:]
        batch_ordered = common_batch.loc[df_norm.columns].reset_index()

        # remove batch with only one sample and raise warning
        unique_batch = batch_ordered[batch_col].value_counts()[batch_ordered[batch_col].value_counts() == 1].index
        
        if not unique_batch.empty:
            warnings.warn(f"The following batches with only one sample will be removed: {list(unique_batch)}")
            sample_id = batch[batch[batch_col].isin(unique_batch)].index
            single_batch_colname = list(set(sample_id) & set(df_norm.columns))
            batch_ordered = batch_ordered[~batch_ordered[batch_col].isin(unique_batch)]
            df_norm = df_norm.drop(columns = single_batch_colname)
        df_norm = pycombat_seq(df_norm, batch_ordered[batch_col])
        print("---------- batch effect removed ----------")
            
    return df_norm