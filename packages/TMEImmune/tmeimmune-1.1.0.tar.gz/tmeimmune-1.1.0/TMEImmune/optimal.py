import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from lifelines import KaplanMeierFitter
from lifelines.plotting import add_at_risk_counts
from lifelines import CoxPHFitter
from lifelines.statistics import logrank_test
from lifelines.utils import concordance_index
import pandas as pd
import numpy as np

def assign_type(score, upper_p, lower_p):
    if upper_p == lower_p:
        q = score.quantile(upper_p)
        def get_type(value):
            if value >= q:
                return 'H'
            else:
                return 'L'
    
    else:
        upper_q = score.quantile(upper_p)
        lower_q = score.quantile(lower_p)
        def get_type(value):
            if value >= upper_q:
                return 'H'
            elif value <= lower_q:
                return 'M'
            else:
                return 'L'
    
    return score.apply(get_type)



def optimal_ICI(df, response, score_name, name = None, roc = True):
    """
    Find the optimal score with the highest AUC for ICI response
    df: pandas dataframe with row index as sample ID, columns containing scores, ICI response ([R, NR] or [0, 1])
    response: column name of ICI response
    score_name: list of names of the score columns in df, or a string of name for only one score
    name: custom title name for figure
    output: a figure showing all ROC curves by scores, and return a dictionary with all scores and the corresponding AUC
    """

    # remove samples with no response status
    df1 = df[~df[response].isna()]
    if isinstance(score_name, str):
        score_name = [score_name]
    
    # transform the response column
    all_strings = df1[response].map(lambda x: isinstance(x, str)).all()
    if all_strings:
        df1[response] = df1[response].str.upper()
        if df1[response].isin(["R","NR"]).all():
            df1["binary_resp"] = df1[response].apply(lambda x: 1 if x == "R" else 0)
        else:
            raise ValueError("Unsupported response type")
    elif df1[response].isin([0,1]).all():
        df1["binary_resp"] = df1[response]
    else:
        raise ValueError("Unsupported response type")

    fig = plt.figure(figsize=(8, 6), dpi = 100)  # Create a figure for the plot
    plt.margins(x=0.05, y=0.05)
    legend_list = score_name
    auc_dict = {}

    for i in range(len(score_name)):
        # Remove rows with missing values in the current score column
        df2 = df1[~df1[score_name[i]].isna()]
        df2[score_name[i]] = df2[score_name[i]].astype(float)
        # Compute FPR, TPR, and thresholds for the ROC curve
        fpr, tpr, thresholds = roc_curve(
            df2['binary_resp'],
            df2[score_name[i]])
        
        # Compute the Area Under the Curve (AUC)
        roc_auc = auc(fpr, tpr)
        auc_dict[score_name[i]] = roc_auc
        
        # Plot the ROC curve
        if roc:
            plt.plot(fpr, tpr, lw=4, label=f'{legend_list[i]} ({roc_auc:.2f})')
            plt.title("ROC Curves for ICI Prediction", fontweight = "bold", fontsize = 16)
            plt.xlabel("False Positive Rates", fontweight = "bold", fontsize = 14)
            plt.ylabel("True Positive Rates", fontweight = "bold", fontsize = 14)
            plt.xticks(fontweight="bold", fontsize = 14)
            plt.yticks(fontweight="bold", fontsize = 14)

    # Plot the diagonal line (random classifier)
    if roc:
        plt.plot([0, 1], [0, 1], color='grey', lw=1, linestyle='--')

        # Set plot limits and labels
        plt.xlim([0.0, 1.03])
        plt.ylim([0.0, 1.1])
        plt.xticks(fontweight="bold", fontsize = 14)
        plt.yticks(fontweight="bold", fontsize = 14)

        if name is None:
            plt.title(f"ROC Curves", fontweight = "bold", fontsize = 16)
        else:
            plt.title(f"ROC Curves for {name}", fontweight = "bold", fontsize = 16) 

        plt.legend(loc="upper left", bbox_to_anchor=(0, 1), title = "AUC",
                   title_fontproperties={'weight': 'bold', 'size': 12}, 
                   prop = {'size':10, 'weight' : "bold"},
                   frameon = False)

    best_auc = max(auc_dict.values())
    optimal_score = [k for k, v in auc_dict.items() if v == best_auc]

    print(f"The optimal score for ICI response prediction: {optimal_score} with AUC = {round(best_auc, 4)}")

    return fig, auc_dict


def optimal_survival(df, delta, time, score_name, clinical_factors = None, upper_p = 0.75, lower_p = 0.25, name = None, km_curves = True, palette = ["#547AC0", "#898988", "#F6C957"]):
    """
    Compare score performance to survival prognosis using Cox-PH model. Each score is divided into three groups, and users can choose to add other clinical factors into the model to adjust for confounding variables.
    delta: column name for survival status. 1 as event (death) and 0 otherwise
    time: column name for survival time, should be float type
    score_name: list of names of the score columns in df, or a string of name for only one score
    clinical factors: list of column names of the other clinical factors added to the model
    upper_p, lower_p: the probabilities at which the upper and lower quantiles are calculated, by default 0.75 and 0.25, respectively
    name: custom title name for the figure
    km_curves: whether to display the Kaplan-Meier survival curve of the optimal score divided into three groups by upper_p and lower_p
    palette: palette for the K-M survival curves
    output: return a dictionary with all scores and their corresponding c-index
    """

    # only considers sample with known survival status and time
    df1 = df[~df[delta].isna()]
    df1 = df1[~df1[time].isna()]
    c_dict = {}

    # test if input values are valid
    if not df1[delta].isin([1,0]).all():
        raise ValueError("delta must be a column containing only 0 or 1")

    if isinstance(score_name, str):
        score_name = [score_name]
    
    if clinical_factors is not None:
        if isinstance(clinical_factors, str):
            clinical_factors = [clinical_factors]
        elif not isinstance(clinical_factors, list):
            raise TypeError("Invalid clinical factor input")
        
    # conduct Cox-PH model
    for score in score_name:
        if clinical_factors is None:
            df1[score] = df1[score].astype(float)
            c_ind = concordance_index(df1[time], df1[score], df1[delta])
        else:
            cph = CoxPHFitter()
            data = df[[delta, time, score] + clinical_factors]
            cph.fit(data, duration_col = time, event_col = delta)
            predicted_risk = cph.predict_partial_hazard(data)
            c_ind = concordance_index(data[time], predicted_risk, data[delta])
        
        c_dict[score] = c_ind
        
    # select the best method and highest c-index
    best_c = max(c_dict.values())
    optimal_score = [k for k, v in c_dict.items() if v == best_c]
    print(f"The optimal score for survival prognosis: {optimal_score} with c-index = {round(best_c, 4)}")

    # draw K-M survival curves
    if km_curves:
        fig, axs = plt.subplots(1, len(optimal_score), figsize=(8, 6*len(optimal_score)), 
                                dpi = 100) #constrained_layout=True, 

        if len(optimal_score) == 1:
            axs = [axs]
        for i in range(len(optimal_score)):
            # segment samples by score into three groups: high(H), and low(L)
            score_type = assign_type(df1[optimal_score[i]], upper_p, lower_p)
            df1['score_type'] = score_type
            kmf_H = KaplanMeierFitter()
            kmf_L = KaplanMeierFitter()
            kmf_H.fit(durations=df1[df1['score_type'] == 'H'][time], event_observed=df1[df1['score_type'] == 'H'][delta], label='H')
            kmf_H.plot_survival_function(show_censors = True, ci_show = False, linewidth=4, color = palette[0], ax = axs[i])
            # add the M group if there are two quantile probabilities
            if upper_p != lower_p:
                kmf_M = KaplanMeierFitter()
                kmf_M.fit(durations=df1[df1['score_type'] == 'M'][time], event_observed=df1[df1['score_type'] == 'M'][delta], label='M')
                kmf_M.plot_survival_function(show_censors = True, ci_show = False, linewidth=4, color = palette[2], ax = axs[i])

            kmf_L.fit(durations=df1[df1['score_type'] == 'L'][time], event_observed=df1[df1['score_type'] == 'L'][delta], label='L')
            kmf_L.plot_survival_function(show_censors = True, ci_show = False, linewidth=4, color = palette[1], ax = axs[i])
            # add risk table for high and low groups
            #add_at_risk_counts(kmf_H, kmf_L, ax=axs[i])

            # perform log-rank test
            df1[time] = pd.to_numeric(df1[time], errors='coerce')
            df1[delta] = pd.to_numeric(df1[delta], errors='coerce')
            results_HL = logrank_test(df1[df1['score_type'] == 'H'][time], df1[df1['score_type'] == 'L'][time], 
                                      event_observed_A=df1[df1['score_type'] == 'H'][delta], 
                                      event_observed_B=df1[df1['score_type'] == 'L'][delta])

            axs[i].margins(x=0.05, y=0.05)
            axs[i].text(0.5, 0.85, f"H vs L: P  = {round(results_HL.p_value,4)}", 
                        transform=axs[i].transAxes, verticalalignment='top', fontweight = 'bold', fontsize = 14)
            axs[i].text(0.5, 0.75, f"c-index = {round(best_c,4)}", transform=axs[i].transAxes, 
                        verticalalignment='top', fontweight = 'bold', fontsize = 14)
            
            if name is None:
                axs[i].set_title(f"K-M Curves for {optimal_score[i]}", fontweight = 'bold', fontsize = 16)
            else:
                axs[i].set_title(f"K-M Curves for {optimal_score[i]} in {name}", fontweight = 'bold', fontsize = 16)
            axs[i].set_xlabel(time, fontweight = 'bold', fontsize = 14)
            axs[i].set_ylabel("Survival Rate", fontweight = 'bold', fontsize = 14)

            # bold all axis
            xticks = axs[i].get_xticks()
            yticks = axs[i].get_yticks()
            xticks_rounded = np.round(xticks, decimals=0)
            yticks_rounded = np.round(yticks, decimals = 1)
            axs[i].set_xticklabels([f'{tick:.0f}' for tick in xticks_rounded], weight = 'bold', size = 14)
            axs[i].set_yticklabels([f'{tick:.1f}' for tick in yticks_rounded] ,weight = 'bold', size = 14)
            axs[i].legend(
                        loc="upper right", title="Group",
                        title_fontproperties={'weight': 'bold', 'size': 12},  # Bold legend title
                        prop={'size': 10, 'weight': "bold"}
                    )


    return fig, c_dict


def get_performance(df_score, metric, score_name, surv_col = None, surv_p = None, ICI_col = None, df_clin = None, clinical_factors = None, show_fig = True, name = None):
    """
    Compare score performance of ICI therapy or/and survival prognosis
    df_score: pandas dataframe containing scores with sample ID as row index
    metric: choose from ["survival", "ICI"]. Enter the full list if the user wants to compare both.
    surv_col: column names of the survival comparison, should be a list of [status, time]
    surv_p: quantile probability for score segmentation in K-M survival curves
    ICI_col: column name of the response column. If comparing both metrics, col = [metric1 col, metric2 col] corresponding to the method.
    score_name: list of names of the score columns in df, or a string of name for only one score
    df_clin: if the columns of survival or response are not in df_score, provide them as a column with sample ID as row index in the pandas dataframe
    clinical_factors: additional column names of factors adding into 
    show_fig: whether to show the ROC curves/K-M survival curves, default to True
    output: return a list of two dictionaries with all scores and their corresponding c-indices/AUCs
    """

    if isinstance(metric, str):
        metric = [metric]
    elif not isinstance(metric, list):
        raise TypeError("Invalid format, must be a list of metrics or a string of a single metric")
    
    df = df_score.copy()
    if df_clin is not None:
        df = df.merge(df_clin, left_index = True, right_index = True, how = "inner")
    
    # empty outcome list
    outcomes = []

    for m in metric:
        if m == "survival":
            # test whether the survival columns are valid
            if not isinstance(surv_col, list):
                raise TypeError("The input survival columns must be in a list")
            if len(surv_col)!= 2:
                raise ValueError("The input survival columns must only have status and time")
            # assigning delta and time to survival columns
            if df[surv_col[0]].dropna().isin([1,0]).all():
                delta = surv_col[0]
                time = surv_col[1]
            else:
                delta = surv_col[1]
                time = surv_col[0]

            # distinguish the upper and lower quantile probabilities and compute survival outcomes
            if surv_p is None:
                surv_out = optimal_survival(df, delta, time, score_name, clinical_factors = None, name = name, km_curves = show_fig)
            else:
                if isinstance(surv_p, float):
                    upper_p = surv_p
                    lower_p = surv_p
                elif not isinstance(surv_p, list):
                    raise TypeError("Invalid input format of quantile probabilities")
                else:
                    upper_p = max(surv_p)
                    lower_p = min(surv_p)
                surv_out = optimal_survival(df, delta, time, score_name, clinical_factors = None, upper_p = upper_p, lower_p = lower_p, name = name, km_curves = show_fig)
            outcomes.append(surv_out)
        # compute ICI outcome
        elif m == "ICI":
            if not isinstance(ICI_col, str):
                raise TypeError("The input ICI_col must be a string")
            elif ICI_col is None:
                raise ValueError("Must input a valid column for ICI therapy response")

            ICI_out = optimal_ICI(df, ICI_col, score_name, name = name, roc = show_fig)
            outcomes.append(ICI_out)

        else:
            raise ValueError("Invalid metric, must be survival or ICI")
        
    return outcomes
        
    