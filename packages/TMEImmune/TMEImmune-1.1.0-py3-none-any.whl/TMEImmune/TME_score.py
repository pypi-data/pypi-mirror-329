from TMEImmune import estimateScore, netbio, SIAscore
from TMEImmune import ISTME as ISM
import pandas as pd
import warnings

def get_score(df, method):
    """
    Compute TME scores for the input gene expression data.
    df: a pandas dataframe having gene symbol as the first column or row index
    method: TME scoring methods choosing from ESTIMATE, ISTME, NetBio, SIA. The method statement can be one method, or a list of multiple methods.
    Output: a pandas dataframe with sample ID as index, and columns are the computed scores
    """

    # test if input is a pandas dataframe
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas dataframe")


    # set gene symbol as row index if not the index column
    first_col = df.iloc[:,0]
    has_letters = first_col.apply(lambda x: any(char.isalpha() for char in str(x)))
    if has_letters.all():
        df1 = df.copy()
        df.index = first_col
        df = df.iloc[:,1:]
    else:
        ind_letters = df.index.to_series().apply(lambda x: any(char.isalpha() for char in str(x)))
        if not ind_letters.any():
            raise ValueError("Index contains invalid gene name. Gene symbols must be in the first column or row index")
        else:
            df1 = df.copy()

    # convert non-float values to float
    all_floats = df1.map(lambda x: isinstance(x, float)).all().all()
    if not all_floats:
        try:
            df1 = df1.astype(float)
        except ValueError:
            raise ValueError("Input contains non-float convertible values.")    

    # remove name missing genes
    if df1.index.isna().any():
        df1 = df1[df1.index.notna()]
        warnings.warn("Input dataframe index contains NA values", UserWarning)

    # for duplicated gene index, keep the first one
    if df1.index.duplicated().any():
        df1 = df1[~df1.index.duplicated(keep='first')]
        warnings.warn("Input dataframe contains duplicated indices", UserWarning)

    score_df = pd.DataFrame()
    score_df.index = df1.columns

    if isinstance(method, str):
        method = [method]
    
    for score in method:
        if score == "ESTIMATE":
            score_est = estimateScore.ESTIMATEscore(df1)
            score_df = pd.concat([score_df, score_est], axis=1)
        elif score == "ISTME":
            score_istme = ISM.istmeScore(df1)
            score_df = pd.concat([score_df, score_istme], axis = 1)
        elif score == "NetBio":
            score_nb = netbio.get_netbio(df1)
            score_df = pd.concat([score_df, score_nb], axis = 1)
        elif score == "SIA":
            score_sia = SIAscore.sia_score(df1)
            score_df = pd.concat([score_df, score_sia], axis = 1)
        else:
            raise ValueError("Invalid scoring method")
    
    return score_df