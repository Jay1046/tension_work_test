query = {
    "create" : 
        {
            "input" : '''
            DROP TABLE IF EXISTS tension.lectures;
            CREATE TABLE tension.lectures(
                lecture VARCHAR(20) not null primary key,
                word    VARCHAR(30) not null,
                time_start INT not null,
                time_end   INT not null,
                size       FLOAT not null,
                pitch_avg  FLOAT not null
            ) 
            ''',
            "output" : '''
            DROP TABLE IF EXISTS tension.results;
            CREATE TABLE tension.results(
                subject                 VARCHAR(20) not null primary key,
                MilkT_speech_amt        FLOAT not null,
                MilkT_speech_spd        FLOAT not null,
                MilkT_formal_prop       FLOAT not null,
                MilkT_pause_length      FLOAT not null,
                MilkT_vol_corr          FLOAT not null,
                Compare_speech_amt      FLOAT not null,
                Compare_speech_spd      FLOAT not null,
                Compare_formal_prop     FLOAT not null,
                Compare_pause_length    FLOAT not null,
                Compare_vol_corr        FLOAT not null
            )
            '''
        }
        ,

    "select" : 
        {
            "all" : '''
                SELECT *
                FROM tension.lectures;
            ''',

            "results" : '''
                SELECT *
                FROM tension.results;
            '''
            
        
        }
    
}