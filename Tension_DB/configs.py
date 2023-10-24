import os 
from dotenv import load_dotenv

load_dotenv()

DB_info = {
    "localhost_rdb_source" : {
        "host": os.environ.get("HOST"),
        "port" : os.environ.get("PORT"),
        "user" : os.environ.get("USER"),
        "password" : os.environ.get("PASSWORD"),
        "database" : os.environ.get("DATABASE"),
        "location" : os.environ.get("LOCATION_SOURCE")
    },

    "localhost_rdb_target" : {
        "host": os.environ.get("HOST"),
        "port" : os.environ.get("PORT"),
        "user" : os.environ.get("USER"),
        "password" : os.environ.get("PASSWORD"),
        "database" : os.environ.get("DATABASE"),
        "location" : os.environ.get("LOCATION_TARGET")
    }

    }