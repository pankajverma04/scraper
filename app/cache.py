import redis
from app.models import Product

class RedisCache:
    def __init__(self):
        self.client = redis.Redis(host="localhost", port=6379, db=0)

    def is_price_changed(self, product: Product) -> bool:
        cached_price = self.client.get(product.title)
        return cached_price is None or float(cached_price) != product.price

    def update_cache(self, product: Product):
        print("cache updated")
        self.client.set(product.title, product.price)
