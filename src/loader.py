import os
import pandas as pd


class DataFileNotFound(Exception):
    #wyprintuje jesli nie bedzie zadnego file
    pass

class InvalidSchemaError(Exception):
    #wyrzuc jesli csv nie ma wymaganych kolumn
    pass

class Loader:

    def __init__(self, data_dir="../data"):
        self.data_dir = data_dir
        self.path_products = os.path.join(self.data_dir, "products.csv")
        self.path_customers = os.path.join(self.data_dir, "customers.csv")
        self.path_sales = os.path.join(self.data_dir, "sales.csv")

    def _ensure_exist(self, path):
        if not os.path.exists(path):
            raise DataFileNotFound(f"Expected file not found: {path}")

    def _read_csv(self, path):
        try:
            df = pd.read_csv(path)
            return df
        except FileNotFoundError:
            raise DataFileNotFound(f"File not found: {path}")
        except pd.errors.EmptyDataError:
            raise InvalidSchemaError(f"File is empty or has no rows: {path}")
        except pd.errors.ParserError as e:
            raise InvalidSchemaError(f"CSV parser error in : {path} -> {e}")

    def _validate_columns(self, df, required_columns, filename):
        missing = [c for c in required_columns if c not in df.columns]
        if missing:
            raise InvalidSchemaError(f"File {filename} is missing columns: {missing}")

    def load_products(self):
        self._ensure_exist(self.path_products)
        df = self._read_csv(self.path_products)
        self._validate_columns(df, ["product_id", "product_name", "category", "price"], "products.csv")
        return df

    def load_customers(self):
        self._ensure_exist(self.path_customers)
        df = self._read_csv(self.path_customers)
        self._validate_columns(df, ["customer_id", "customer_name", "region", "age"], "customers.csv")
        return df

    def load_sales(self):
        self._ensure_exist(self.path_sales)
        df = self._read_csv(self.path_sales)
        self._validate_columns(df, ["sale_id", "product_id", "customer_id", "units", "date"], "sales.csv")
        return df

    def load_all(self):
        products = self.load_products()
        customers = self.load_customers()
        sales = self.load_sales()
        return products, customers, sales

