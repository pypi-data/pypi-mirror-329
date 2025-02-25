import os 
from pathlib import Path

CUR_PATH = Path(__file__).resolve().parent

LOG_STORE_DIR = os.getenv('LOG_STORE_DIR', os.path.join(CUR_PATH, 'logs'))
ASSET_STORE_DIR = os.getenv('ASSETS_STORE_DIR', os.path.join(CUR_PATH, 'assets', 'custom')) #f'{CUR_PATH}/assets/custom')
MJB_PATH = os.getenv('ASSETS_STORE_DIR', os.path.join(CUR_PATH, 'assets', 'custom')) 