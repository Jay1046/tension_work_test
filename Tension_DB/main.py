from db.conn import DBConnector
from db.controller import *
from db.queries import query


from lib.load import load_audio_df, merge_status
from lib import speech_status, formal_status, pause_time_status, vol_corr_status

from configs import DB_info

import warnings
warnings.filterwarnings(action="ignore")


def main():
    df_audio = rdb_pandas_extractor(
        db_connector = DBConnector(**DB_info["localhost_rdb_source"]),
        _query = query["select"]["all"]
    )
    print("Extract Completed")

    print("Calculating status begin...")
    df_speech_status = speech_status.get_speech_status(df_audio)
    df_formal_status = formal_status.get_formal_status(df_audio)
    df_pause_time_status = pause_time_status.get_pause_time_status(df_audio)
    df_vol_corr_status = vol_corr_status.get_vol_corr_status(df_audio)

    df_mid_status = merge_status(
        df_speech_status = df_speech_status,
        df_formal_status = df_formal_status,
        df_pause_time_status = df_pause_time_status,
        df_vol_corr_status = df_vol_corr_status,
        target="middle"
    )

    df_ele_status = merge_status(
        df_speech_status = df_speech_status,
        df_formal_status = df_formal_status,
        df_pause_time_status = df_pause_time_status,
        df_vol_corr_status = df_vol_corr_status,
        target="element"
    )
    print("Status's ready")

    rdb_pandas_loader(
        db_connector = DBConnector(**DB_info["localhost_rdb_target"]),
        _name = "results",
        df = df_mid_status
    )

    print("Load Completed")

if __name__ == "__main__":
    main()