import pandas as pd
from pathlib import Path
from .config import Config

def load_data(file_path: Path = Config.RAW_PRODUCTS_PATH) -> pd.DataFrame:
    '''Функция загрузки данных из csv-файла.'''
    return pd.read_csv(file_path)