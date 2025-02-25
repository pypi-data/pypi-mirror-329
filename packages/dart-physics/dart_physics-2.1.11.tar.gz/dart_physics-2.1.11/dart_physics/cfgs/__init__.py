from pathlib import Path
import os

CURR_PATH = Path(__file__).resolve().parent

def get_config_path(task_name: str) -> str:
    """
    Get path to config file for task.
    """
    return os.path.join(CURR_PATH, f"{task_name}.yaml")