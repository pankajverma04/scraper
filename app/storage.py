import json
from app.models import Product

class JSONStorage:
    FILE_PATH = "products.json"

    def save_product(self, product: Product):
        data = self._load_data()
        data.append(product.dict())
        self._save_data(data)

    def _load_data(self):
        try:
            with open(self.FILE_PATH, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _save_data(self, data):
        with open(self.FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)
