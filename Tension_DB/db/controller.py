from sqlalchemy import create_engine
import pandas as pd

def rdb_cursor_create(db_connector, _query):
    with db_connector as connected:
        cur = connected.conn.cursor()
        cur.execute(_query)
        connected.conn.commit()
        print("Table Created")

def rdb_cursor_extractor(db_connector, _query):
    with db_connector as connected:
        cur = connected.conn.cursor()
        cur.execute(_query)
        result = cur.fetchall()
    
    return result


def rdb_pandas_loader(db_connector, _name, df):
    
    engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'\
        .format(\
            user = db_connector.user
            , password = db_connector.password
            , host = db_connector.host
            , port = db_connector.port
            , database = db_connector.database)
            )
    
    
    df.to_sql(name=_name, con=engine, schema="tension", if_exists='replace', index=False)

    return print("Load completed")

def rdb_pandas_extractor(db_connector, _query):
    
    engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'\
        .format(\
            user = db_connector.user
            , password = db_connector.password
            , host = db_connector.host
            , port = db_connector.port
            , database = db_connector.database)
            )
    
    df = pd.read_sql(
        sql= _query,
        con = engine
        )

    return df