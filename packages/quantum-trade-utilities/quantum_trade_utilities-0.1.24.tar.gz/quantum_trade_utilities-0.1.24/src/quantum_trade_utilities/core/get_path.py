"""
Get the path for a given label.
"""
import os

from quantum_trade_utilities.core.detect_os import detect_os


def get_path(path_label: str):
    """
    Get the path for a given label.
    """
    if path_label == "creds":
        return os.getenv("APP_PATH_" + detect_os()) + "/_cred/creds.json"
    elif path_label == "job_ctrl":
        return os.getenv("APP_PATH_" + detect_os()) + "/_job_ctrl/load_ctrl.json"
    elif path_label == "bachman_rag":
        return os.getenv("APP_PATH_" + detect_os()) + "/_llm_cfg/bachman_rag.json"
    elif path_label == "log":
        return os.getenv("PROJ_PATH_" + detect_os()) + "/app.log"
    elif path_label == "env":
        return os.getenv("PROJ_PATH_" + detect_os()) + "/.env"
    elif path_label == "doc_workspace":
        return os.getenv("APP_PATH_" + detect_os()) + "/doc_workspace"
    else:
        return False
