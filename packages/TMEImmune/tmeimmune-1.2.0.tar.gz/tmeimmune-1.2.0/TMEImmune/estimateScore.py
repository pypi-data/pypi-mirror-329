import pandas as pd
import numpy as np


class ESTIMATE_signature:
    def __init__(self):
        self.sig = pd.DataFrame({"stromal": ["DCN",	"PAPPA",	"SFRP4",	"THBS2",	"LY86",	"CXCL14",	"FOXF1",	"COL10A1",	"ACTG2",	"APBB1IP",	"SH2D1A",	"SULF1",	"MSR1",	"C3AR1",	"FAP",	"PTGIS",	"ITGBL1",	"BGN",	"CXCL12",	"ECM2",	"FCGR2A",	"MS4A4A",	"WISP1",	"COL1A2",	"MS4A6A",	"EDNRA",	"VCAM1",	"GPR124",	"SCUBE2",	"AIF1",	"HEPH",	"LUM",	"PTGER3",	"RUNX1T1",	"CDH5",	"PIK3R5",	"RAMP3",	"LDB2",	"COX7A1",	"EDIL3",	"DDR2",	"FCGR2B",	"LPPR4",	"COL15A1",	"AOC3",	"ITIH3",	"FMO1",	"PRKG1",	"PLXDC1",	"VSIG4",	"COL6A3",	"SGCD",	"COL3A1",	"F13A1",	"OLFML1",	"IGSF6",	"COMP",	"HGF",	"GIMAP5",	"ABCA6",	"ITGAM",	"MAF",	"ITM2A",	"CLEC7A",	"ASPN",	"LRRC15",	"ERG",	"CD86",	"TRAT1",	"COL8A2",	"TCF21",	"CD93",	"CD163",	"GREM1",	"LMOD1",	"TLR2",	"ZEB2",	"C1QB",	"KCNJ8",	"KDR",	"CD33",	"RASGRP3",	"TNFSF4",	"CCR1",	"CSF1R",	"BTK",	"MFAP5",	"MXRA5",	"ISLR",	"ARHGAP28",	"ZFPM2",	"TLR7",	"ADAM12",	"OLFML2B",	"ENPP2",	"CILP",	"SIGLEC1",	"SPON2",	"PLXNC1",	"ADAMTS5",	"SAMSN1",	"CH25H",	"COL14A1",	"EMCN",	"RGS4",	"PCDH12",	"RARRES2",	"CD248",	"PDGFRB",	"C1QA",	"COL5A3",	"IGF1",	"SP140",	"TFEC",	"TNN",	"ATP8B4",	"ZNF423",	"FRZB",	"SERPING1",	"ENPEP",	"CD14",	"DIO2",	"FPR1",	"IL18R1",	"HDC",	"TXNDC3",	"PDE2A",	"RSAD2",	"ITIH5",	"FASLG",	"MMP3",	"NOX4",	"WNT2",	"LRRC32",	"CXCL9",	"ODZ4",	"FBLN2",	"EGFL6",	"IL1B",	"SPON1",	"CD200"],
    "immune" :["LCP2",	"LSP1",	"FYB",	"PLEK",	"HCK",	"IL10RA",	"LILRB1",	"NCKAP1L",	"LAIR1",	"NCF2",	"CYBB",	"PTPRC",	"IL7R",	"LAPTM5",	"CD53",	"EVI2B",	"SLA",	"ITGB2",	"GIMAP4",	"MYO1F",	"HCLS1",	"MNDA",	"IL2RG",	"CD48",	"AOAH",	"CCL5",	"LTB",	"GMFG",	"GIMAP6",	"GZMK",	"LST1",	"GPR65",	"LILRB2",	"WIPF1",	"CD37",	"BIN2",	"FCER1G",	"IKZF1",	"TYROBP",	"FGL2",	"FLI1",	"IRF8",	"ARHGAP15",	"SH2B3",	"TNFRSF1B",	"DOCK2",	"CD2",	"ARHGEF6",	"CORO1A",	"LY96",	"LYZ",	"ITGAL",	"TNFAIP3",	"RNASE6",	"TGFB1",	"PSTPIP1",	"CST7",	"RGS1",	"FGR",	"SELL",	"MICAL1",	"TRAF3IP3",	"ITGA4",	"MAFB",	"ARHGDIB",	"IL4R",	"RHOH",	"HLA-DPA1",	"NKG7",	"NCF4",	"LPXN",	"ITK",	"SELPLG",	"HLA-DPB1",	"CD3D",	"CD300A",	"IL2RB",	"ADCY7",	"PTGER4",	"SRGN",	"CD247",	"CCR7",	"MSN",	"ALOX5AP",	"PTGER2",	"RAC2",	"GBP2",	"VAV1",	"CLEC2B",	"P2RY14",	"NFKBIA",	"S100A9",	"IFI30",	"MFSD1",	"RASSF2",	"TPP1",	"RHOG",	"CLEC4A",	"GZMB",	"PVRIG",	"S100A8",	"CASP1",	"BCL2A1",	"HLA-E",	"KLRB1",	"GNLY",	"RAB27A",	"IL18RAP",	"TPST2",	"EMP3",	"GMIP",	"LCK",	"IL32",	"PTPRCAP",	"LGALS9",	"CCDC69",	"SAMHD1",	"TAP1",	"GBP1",	"CTSS",	"GZMH",	"ADAM8",	"GLRX",	"PRF1",	"CD69",	"HLA-B",	"HLA-DMA",	"CD74",	"KLRK1",	"PTPRE",	"HLA-DRA",	"VNN2",	"TCIRG1",	"RABGAP1L",	"CSTA",	"ZAP70",	"HLA-F",	"HLA-G",	"CD52",	"CD302",	"CD27"]})
    def get_signature_data(self):
        return self.sig


def ESTIMATEscore(df):
    """
    Compute the ESTIMATE immune and stromal score for the input gene expression matrix
    df: the input gene expression matrix dataframe where gene symbol as the first column or index
    index: whether gene symbol column is in the index. True if yes, and no other gene symbol column in the dataframe; otherwise no
    output: a pandas dataframe with three columns, 
            index: sample ID, 
            'EST_stromal': ESTIMATE stromal score; 
            'EST_immune': ESTIMATE immune score; 
            'estimate': ESTIMATE score
    """

    df_ranked = df.apply(pd.to_numeric).rank(axis = 0, method = "average")
    df_ranked.index = df.index
    df_normalized = 10000*df_ranked/df_ranked.shape[0]
    gene_set_names = ['stromal', 'immune']
    score = np.empty((df_ranked.shape[1], 2))

    common_genes = {}
    signature_data = ESTIMATE_signature()
    sig = signature_data.get_signature_data()
    for i in range(0,2):
    
        gene_set = sig.iloc[:,i]
        common = list(set(gene_set) & set(df.index))
        common_genes[gene_set_names[i]] = common

        if len(common) == 0: 
            print("There is no common genes with the input and the ", gene_set_names[i], " signature")
            continue

        # ssGSEA
        ES_vector = [0]*df_normalized.shape[1]
        for sample in range(0, df_normalized.shape[1]):
            ordered_genes = df_normalized.iloc[:,sample].sort_values(ascending = False)
            hit_ind = ordered_genes.index.isin(gene_set)
            no_hit_ind = 1- hit_ind
            ordered_genes1 = ordered_genes.pow(1./4)
            hit_exp = ordered_genes1[hit_ind]
            no_hit_penalty = np.cumsum(no_hit_ind/sum(no_hit_ind))
            hit_reward = np.cumsum((hit_ind*ordered_genes1)/sum(hit_exp))
            ES_vector[sample] = sum(hit_reward - no_hit_penalty)
        score[:, i] = ES_vector

    score = pd.DataFrame(score)
    score.index = df.columns
    score.columns = ["EST_stromal", "EST_immune"]
    score['estimate'] = score['EST_stromal'] + score['EST_immune']

    return score



def tumor_purity(platform, df):
    """
    When data comes from platform Affymetrix, provides an estimate of tumor purity
    output: numpy array
    """
    if platform != "Affymetrix":
        raise ValueError("Tumor purity is not available for this platform")
    else:
        score = ESTIMATEscore(df)
        purity = np.cos(0.6049872018 + 0.0001467884*score['estimate'])
        return purity
    

def common_genes(df):
    """
    Output the common genes of the input df and the ESTIMATE signatures
    """
    genes = df.iloc[:,0]
    signature_data = ESTIMATE_signature()
    sig = signature_data.get_signature_data()
    common_immune = list(set(sig['immune']) & set(genes))
    common_stromal = list(set(sig['stromal']) & set(genes))
    common = {'EST_immune': common_immune, 'EST_stromal': common_stromal}
    return common