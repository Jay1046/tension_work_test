import pandas as pd


def load_audio_df(excel_path):
    xls = pd.ExcelFile(excel_path)

    data_frames = []

    for i in range(len(xls.sheet_names)):
        df = pd.read_excel(excel_path, sheet_name=xls.sheet_names[i])
        df['강좌'] = sheet_name=xls.sheet_names[i]
        data_frames.append(df)

    df_combined = pd.concat(data_frames)
    df_combined.drop(['Unnamed: 0'], axis=1, inplace=True)
    df_combined = df_combined[["강좌", "인식단어", "시작(msec)", "끝(msec)", "크기", "피치평균"]]
    df_combined = df_combined.rename({"강좌":"lecture", "인식단어":"word","시작(msec)":"time_start", "끝(msec)":"time_end", "크기":"size","피치평균":"pitch_avg"}, axis=1)
    
    return df_combined


def merge_status(df_speech_status, df_formal_status, df_pause_time_status, df_vol_corr_status, target="middle"):

    df_tmp1 = pd.merge(df_speech_status, df_formal_status, on="lecture")
    df_tmp2 = pd.merge(df_pause_time_status, df_vol_corr_status, on="lecture")
    df_status = pd.merge(df_tmp1, df_tmp2, on="lecture")

    if target == "middle":
    
        milkt = df_status[df_status["lecture"].str.contains("중학_밀크티")]
        compare = df_status[df_status["lecture"].str.contains("중학_엠베스트")]
        subject_list = milkt["lecture"].apply(lambda x: x[-2:]).unique()


    elif target == "element":
        milkt = df_status[df_status["lecture"].str.contains("초등_밀크티")]
        compare = df_status[df_status["lecture"].str.contains("초등_엘리하이")]
        subject_list = milkt["lecture"].apply(lambda x: x[-2:]).unique()

    df_status = pd.DataFrame(
        {
            "lecture" : subject_list,
            "MilkT_speech_amt" : milkt["speech_amt"].tolist(),
            "MilkT_speech_spd" : milkt["speech_spd"].tolist(),
            "MilkT_formal_prop" : milkt["formal_prop"].tolist(),
            "MilkT_pause_length" : milkt["eps_length_mean"].tolist(),
            "MilkT_vol_corr" : milkt["correlation"].tolist(),
            "Compare_speech_amt" : compare["speech_amt"].tolist(),
            "Compare_speech_spd" : compare["speech_spd"].tolist(),
            "Compare_formal_prop" : compare["formal_prop"].tolist(),
            "Compare_pause_length" : compare["eps_length_mean"].tolist(),
            "Compare_vol_corr" : compare["correlation"].tolist(),

            
        }
    )

    return df_status

