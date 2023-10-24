import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_pause_time(df_audio):
    
    df_audio['eps_length'] = df_audio['time_end'] - df_audio['time_start']
    df_audio = df_audio[df_audio['word'] != '<eps>']
    mean_eps = df_audio['eps_length'].mean()

    return mean_eps

def get_pause_time_status(df_audio):
    
    unique_lecs = df_audio["lecture"].unique()

    lec_dict = {"lecture":[], "eps_length_mean":[]}
    for lec in unique_lecs:
        lecture = df_audio[df_audio["lecture"] == lec]
        pause_time = get_pause_time(lecture)
        lec_dict["lecture"].append(lec)
        lec_dict["eps_length_mean"].append(pause_time)

    return pd.DataFrame(lec_dict)

def pause_length_plt(df):
    plt.bar(df['lecture'], df['MilkT_pause_length'], width=0.4, label='MilkT_pause_length', align='center')
    plt.bar(df['lecture'], df['Compare_pause_length'], width=0.4, label='Compare_pause_length', align='edge')
    plt.legend()
    plt.xlabel('lecture')
    plt.ylabel('pause_length')
    return plt.title