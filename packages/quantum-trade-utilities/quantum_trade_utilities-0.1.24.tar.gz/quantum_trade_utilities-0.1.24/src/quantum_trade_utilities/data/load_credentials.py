"""
Load Alpaca API credentials from JSON file.
"""
import json
from dotenv import load_dotenv

load_dotenv()


def load_credentials(file_path, data_type):
    """
    Load Alpaca API credentials from JSON file.
    """

    if data_type == "alpaca_paper_trade":
        with open(file_path, "r", encoding="utf-8") as file:
            creds = json.load(file)
        alpaca_creds = creds["alpaca_paper_api"]
        return (
            alpaca_creds["API_KEY"],
            alpaca_creds["API_SECRET"],
            alpaca_creds["PAPER_URL"],
        )

    elif data_type == "alpaca_live_trade":
        with open(file_path, "r", encoding="utf-8") as file:
            creds = json.load(file)
        alpaca_creds = creds["alpaca_live_api"]
        return (
            alpaca_creds["API_KEY"],
            alpaca_creds["API_SECRET"],
            alpaca_creds["LIVE_URL"],
        )

    elif data_type == "alpaca_news":
        with open(file_path, "r", encoding="utf-8") as file:
            creds = json.load(file)
        news_creds = creds["alpaca_news_api"]
        return (
            news_creds["API_KEY"],
            news_creds["API_SECRET"],
        )

    elif data_type == "fmp_api_findata":
        with open(file_path, "r", encoding="utf-8") as file:
            creds = json.load(file)
        fmp_creds = creds["fmp_api_findata"]
        return (
            fmp_creds["API_KEY"],
            fmp_creds["BASE_URL"],
        )

    elif data_type == "fmp_api_findata_v4":
        with open(file_path, "r", encoding="utf-8") as file:
            creds = json.load(file)
        fmp_creds = creds["fmp_api_findata_v4"]
        return (
            fmp_creds["API_KEY"],
            fmp_creds["BASE_URL"],
        )

    elif data_type == "fmp_api_gov":
        with open(file_path, "r", encoding="utf-8") as file:
            creds = json.load(file)
        fmp_creds = creds["fmp_api_gov"]
        return (
            fmp_creds["API_KEY"],
            fmp_creds["BASE_URL"],
        )

    elif data_type == "fmp_api_hist":
        with open(file_path, "r", encoding="utf-8") as file:
            creds = json.load(file)
        fmp_creds = creds["fmp_api_hist"]
        return (
            fmp_creds["API_KEY"],
            fmp_creds["BASE_URL"],
        )

    if data_type == "hendricks_api":
        with open(file_path, "r", encoding="utf-8") as file:
            creds = json.load(file)
        hendricks_creds = creds["hendricks_api"]
        return (hendricks_creds["API_KEY"],)

    if data_type == "gilfoyle_api":
        with open(file_path, "r", encoding="utf-8") as file:
            creds = json.load(file)
        gilfoyle_creds = creds["gilfoyle_api"]
        return (gilfoyle_creds["API_KEY"],)

    if data_type == "mongo_ds_remote":
        with open(file_path, "r", encoding="utf-8") as file:
            creds = json.load(file)
        mongo_creds = creds["mongo_ds_remote"]
        return (
            mongo_creds["MONGO_USER"],
            mongo_creds["MONGO_PASSWORD"],
            mongo_creds["MONGO_HOST"],
            mongo_creds["MONGO_PORT"],
        )

    if data_type == "mongo_ds_local":
        with open(file_path, "r", encoding="utf-8") as file:
            creds = json.load(file)
        mongo_creds = creds["mongo_ds_local"]
        return (
            mongo_creds["MONGO_USER"],
            mongo_creds["MONGO_PASSWORD"],
            mongo_creds["MONGO_HOST"],
            mongo_creds["MONGO_PORT"],
        )

    if data_type == "reddit_api":
        with open(file_path, "r", encoding="utf-8") as file:
            creds = json.load(file)
        reddit_creds = creds["reddit_api"]
        return (
            reddit_creds["CLIENT_ID"],
            reddit_creds["CLIENT_SECRET"],
            reddit_creds["USER_AGENT"],
            reddit_creds["REDDIT_USER"],
            reddit_creds["REDDIT_PWD"],
        )
    
    if data_type == "qdrant_ds":
        with open(file_path, "r", encoding="utf-8") as file:
            creds = json.load(file)
        qdrant_creds = creds["qdrant_ds"]
        return (
            qdrant_creds["QDRANT_HOST"],
            qdrant_creds["QDRANT_PORT"],
        )
    
    if data_type == "vllm_ds":
        with open(file_path, "r", encoding="utf-8") as file:
            creds = json.load(file)
        vllm_creds = creds["vllm_ds"]
        return (
            vllm_creds["VLLM_HOST"],
            vllm_creds["VLLM_PORT"],
        )
    
    if data_type == "groq_api":
        with open(file_path, "r", encoding="utf-8") as file:
            creds = json.load(file)
        groq_creds = creds["groq_api"]
        return (
            groq_creds["API_KEY"]
        )
    
    if data_type == "huggingface_api":
        with open(file_path, "r", encoding="utf-8") as file:
            creds = json.load(file)
        huggingface_creds = creds["huggingface_api"]
        return (
            huggingface_creds["API_KEY"],
        )

    if data_type == "bachman_api":
        with open(file_path, "r", encoding="utf-8") as file:
            creds = json.load(file)
        bachman_creds = creds["bachman_api"]
        return (
            bachman_creds["API_KEY"],
        )

    else:
        raise ValueError(f"Invalid data type: {data_type}")
