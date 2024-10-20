import requests
from bs4 import BeautifulSoup
from time import sleep
from typing import List, Optional
from app.models import Product

class Scraper:
    def __init__(self, storage, cache):
        self.storage = storage
        self.cache = cache

    def scrape_catalog(self, limit: int, proxy: Optional[str] = None) -> dict:    
        base_url = "https://dentalstall.com/shop/page/"
        scraped_count = 0

        for page in range(1, limit + 1):
            url = f"{base_url}{page}/"
            response = self._fetch_page(url, proxy)
            
            # print(response)

            if not response:
                continue  # Skip if fetch failed

            products = self._parse_products(response.content)
            for product in products:
                if not self.cache.is_price_changed(product):
                    print("price not updated")
                    continue

                self.storage.save_product(product)
                self.cache.update_cache(product)
                scraped_count += 1

        print(f"Scraped {scraped_count} products.")
        return {"scraped_count": scraped_count}

    def _fetch_page(self, url: str, proxy: Optional[str]) -> Optional[requests.Response]:    
        try:
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
            # print(response.content)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}, retrying in 5 seconds...")
            sleep(5)
            return None

    def _parse_products(self, content: bytes) -> List[Product]:  
        soup = BeautifulSoup(content, "html.parser")
        products = []

        for item in soup.select(".product-inner"):
            
            product_link = item.select_one("a")["href"]
            title = self._fetch_full_title(product_link)
            # print("Title Temp : ", title)

            # title = item.select_one(".woo-loop-product__title").text.strip()
            # print('title: ', title)
            
            price = float(item.select_one(".price").text.strip().split("₹")[1])
            # print('PRICE: ', price)   
                
            image_element = item.select_one(".mf-product-thumbnail img")

            image_url = image_element.get("data-lazy-src") or image_element.get("src")

            # if image_url:
            #     print(f"Image URL: {image_url}")
            # else:
            #     print("Image URL not found")
            

            product = Product(title=title, price=price, image_url="image_url")
            products.append(product)

        return products

    def _fetch_full_title(self, product_url):
        try:
            response = requests.get(product_url)
            product_soup = BeautifulSoup(response.content, "html.parser")

            title_element = product_soup.select_one(".product_title.entry-title")
            return title_element.text.strip() if title_element else "Title Not Found"
        
        except Exception as e:
            print(f"Error fetching full title from {product_url}: {e}")
            return "Title Not Found"