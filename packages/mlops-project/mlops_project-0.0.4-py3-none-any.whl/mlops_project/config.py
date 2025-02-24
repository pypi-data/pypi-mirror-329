from pathlib import Path

class Config:
    RAW_PRODUCTS_PATH = Path("../data/raw/mlops_url_dataset.csv")
    PROCESSED_PRODUCTS_PATH = Path("../data/processed/mlops_url_dataset.csv")
    PROCESSED_CATEGORIES_PATH = Path("../data/processed/ru_ecom_tree_category.csv")
