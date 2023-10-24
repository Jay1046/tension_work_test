# 발화량
import kss
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

import matplotlib.pyplot as plt
import seaborn as sns
plt.rc('font', family='Malgun Gothic')

def get_speech_amt(df):   
    new_df = df.copy()
    unique_lecs = new_df["lecture"].unique()

    lec_dict = {"lecture":[], "speech_amt":[]}
    for lec in unique_lecs:
        words = new_df[new_df["lecture"] == lec]["word"]
        sentences = kss.split_sentences(" ".join(words))
        
        total_min = ((new_df[new_df["lecture"] == lec]["time_end"].iloc[-1]) - (new_df[new_df["lecture"] == lec]["time_start"].iloc[0]) ) / 1000 / 60

        lec_dict["lecture"].append(lec)
        lec_dict["speech_amt"].append(len(sentences) / total_min)
    
    
    return pd.DataFrame(lec_dict)

# 발화속도
def get_speech_speed(df):   
    new_df = df.copy()
    unique_lecs = new_df["lecture"].unique()

    new_df["speech_length"] = (new_df["time_end"] - new_df["time_start"]) /1000
    new_df["speech_speed"] =  new_df["word"].apply(lambda x: len(x)) / new_df["speech_length"]
     
    lec_dict = {"lecture":[], "speech_spd":[]}
    for lec in unique_lecs:
        speed = np.mean(new_df[new_df["lecture"] == lec]["speech_speed"])

        lec_dict["lecture"].append(lec)
        lec_dict["speech_spd"].append(speed)
    
    
    return pd.DataFrame(lec_dict)




def get_speech_status(df_audio):


    df_wo_eps = df_audio[df_audio["word"] != "<eps>"]

    scaler = MinMaxScaler()
    df_wo_eps.loc[:, ["size","pitch_avg"]] = scaler.fit_transform(df_wo_eps[["size","pitch_avg"]])

    speech_amt = get_speech_amt(df_wo_eps)
    speech_speed = get_speech_speed(df_wo_eps)

    df_speech_status = speech_amt.merge(speech_speed, on="lecture")

    return df_speech_status



def plot_speech_info(df_status):
    idx = np.arange(len(df_status))
    w = 0.15

    plt.figure(figsize = (10, 5))
    plt.subplot(1,2,1)
    plt.bar(idx - 1 * w, df_status['MilkT_speech_amt'], width = w, label="MilkT", color="royalblue")
    plt.bar(idx, df_status['Compare_speech_amt'], width = w, label="Compare", color="orange")
    plt.xticks(ticks=idx, labels=df_status["lecture"])
    plt.title("발화량 비교")
    plt.legend()
    plt.ylabel("평균 발화량(분당 문장 수)")
    plt.xlabel("강의 과목")

    plt.subplot(1,2,2)
    plt.bar(idx - 1 * w, df_status['MilkT_speech_spd'], width = w, label="MilkT", color="royalblue")
    plt.bar(idx, df_status['Compare_speech_spd'], width = w, label="Compare", color="orange")
    plt.xticks(ticks=idx, labels=df_status["lecture"])
    plt.title("발화속도 비교")
    plt.legend()
    plt.ylabel("평균 발화속도(초당 음절 수)")
    plt.xlabel("강의 과목")