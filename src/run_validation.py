from models.validation.validation import validate_all_models
from models.utils.data_fetcher import DataFetcher

if __name__ == "__main__":
    fetcher = DataFetcher("all")

    print(validate_all_models())
