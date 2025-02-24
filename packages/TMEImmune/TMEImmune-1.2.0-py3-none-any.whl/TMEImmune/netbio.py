import gseapy as gp
import pandas as pd
import requests
import numpy as np
import json

class nb_pathway():
    def __init__(self):
        url = "https://raw.githubusercontent.com/qiluzhou/TMEImmune/refs/heads/main/data/"
        self.coef = pd.read_csv(url + "coef_best_netbio.csv")
        response = requests.get(url + "gene_sets.json")
        if response.status_code == 200:
            self.gene_set = json.loads(response.text)
        else:
            print(f"Failed to retrieve the reactomr geneset: {response.status_code}")
    
    def get_nb_coef(self):
        return self.coef
    
    def reactome_geneset(self):
        return self.gene_set



def get_netbio(df):
    """
    Compute the NetBio score for the input gene expression matrix
    df: the input gene expression matrix dataframe where gene symbol as the first column or index
    index: whether gene symbol column is in the index. True if yes, and no other gene symbol column in the dataframe; otherwise no
    output: a pandas dataframe with one column, 
            index: sample ID, 
            'NetBio_score': NetBio score
    """

    # coefficients of netbio pathways
    nb_coef = nb_pathway().get_nb_coef()
    pathway = nb_coef['Variable'][1:]

    # get netbio reactome pathways and corresponding genesets
    gene_set_dict = nb_pathway().reactome_geneset()

    # perform ssgsea
    ssgsea_results = gp.ssgsea(
    data=df,
    gene_sets=gene_set_dict,  # Path to the gene set file
    min_size=0,
    outdir=None,  # Avoid file output
    verbose=True
    )
    nes_pivot = ssgsea_results.res2d.pivot(index='Term', columns='Name', values='NES')

    # find the common pathways of ssgsea results and the netbio pathways
    common_path = list(set(pathway) & set(nes_pivot.index))
    nes_common = nes_pivot.loc[list(common_path),:]
    nes_common = nes_common.astype(float)
    # replace NA with 0
    nes_common = nes_common.fillna(0)
    ptys = nes_common.index

    # extract coefficients of the common pathways
    nb_coef1 = nb_coef[nb_coef['Variable'].isin(common_path)]

    # arrange the coefficients as the same order as the ssgsea result dataframe
    nb_coef1['Variable'] = pd.Categorical(nb_coef1['Variable'], categories=list(ptys), ordered=True)
    nb_coef_sorted = nb_coef1.sort_values('Variable')
    coefficients = nb_coef_sorted['Coefficient']

    # calculate the netbio score
    intercept = nb_coef['Coefficient'][0]
    nb_score = np.dot(nes_common.T, coefficients) + intercept
    netbio = pd.DataFrame({"NetBio": nb_score.astype(float)})
    netbio.index = nes_pivot.columns

    return netbio