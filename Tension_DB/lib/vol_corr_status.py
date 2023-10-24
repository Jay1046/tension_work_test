import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def get_vol_corr(df_audio):

    df_wo_eps = df_audio[df_audio['word'] != '<eps>']
    df_wo_eps["size_delta"] =np.abs(np.insert(np.diff(df_wo_eps["size"]), 0, 0).tolist())

    scaler=MinMaxScaler()
    df_wo_eps.loc[:, ["size", "size_delta"]] = scaler.fit_transform(df_wo_eps[["size","size_delta"]])
    corr = df_wo_eps['size'].corr(df_wo_eps['size_delta'], method='pearson')

    return corr


def get_vol_corr_status(df_audio):
    unique_lecs = df_audio["lecture"].unique()

    lec_dict = {"lecture":[], "correlation":[]}
    for lec in unique_lecs:
        lecture = df_audio[df_audio["lecture"] == lec]
        corr = get_vol_corr(lecture)
        lec_dict["lecture"].append(lec)
        lec_dict["correlation"].append(corr)

    return pd.DataFrame(lec_dict)

