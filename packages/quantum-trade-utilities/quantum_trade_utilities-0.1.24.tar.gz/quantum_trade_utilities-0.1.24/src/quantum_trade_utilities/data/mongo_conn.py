"""
MongoDB connection utility for Gilfoyle.
"""

from dotenv import load_dotenv
from pymongo import MongoClient
from quantum_trade_utilities.data.load_credentials import load_credentials
from quantum_trade_utilities.core.get_path import get_path
from quantum_trade_utilities.core.detect_os import detect_os

load_dotenv()


def mongo_conn(
    mongo_user: str = None,
    mongo_password: str = None,
    mongo_host: str = None,
    mongo_port: str = None,
    mongo_db: str = "stocksDB",
):
    """
    Connect to MongoDB.
    """

    if detect_os() == "MAC":
        mongo_host_loc = "mongo_ds_remote"
    else:
        mongo_host_loc = "mongo_ds_local"

    creds_path = get_path("creds")
    mongo_user, mongo_password, mongo_host, mongo_port = load_credentials(
        creds_path, mongo_host_loc
    )
    conn = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}?directConnection=true&serverSelectionTimeoutMS=2000&authSource=admin&appName=mongosh+2.3.2"
    # Connect to MongoDB
    client = MongoClient(conn)
    db = client[mongo_db]
    return db
