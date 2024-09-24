from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from undetected_chromedriver import Chrome, ChromeOptions
import tls_client
import random
import time
import pandas as pd
from pprint import pprint
import logging
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import json
from input_files.utils import load_items

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

cookies = ""




def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
    ]
    return random.choice(user_agents)

class SeleniumScraper:
    def __init__(self):
        self.cookies = ""
        self.data = []
        self.reviews = {}
        self.driver = None
        self.token = ""

    def __enter__(self):
        self.initialize_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_spider()

    def initialize_driver(self):
        try:
            chrome_options = ChromeOptions()
            chrome_options.add_argument(f'user-agent={get_random_user_agent()}')
            self.driver = Chrome(driver_executable_path=ChromeDriverManager().install(), options=chrome_options)
        except WebDriverException as e:
            logging.error(f"Failed to initialize driver: {e}")
            raise
    
    def get_cookies(self):
        url = "https://www.eldorado.ru"
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[id="TabAbout"]'))
        )
        self.cookies = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in self.driver.get_cookies()])
    
    def get_token(self):
        url = "https://www.eldorado.ru/_ajax/spa/auth/getToken.php"
        headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': self.cookies,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }

        session = tls_client.Session(client_identifier="chrome_108")
        response = session.get(url, headers=headers)

        self.token = response.json().get("token")

    def start_requests(self, items):
        print("Solving captcha...")
        print(f"First product link: {items[0]['product_link']}")
        self._solve_captcha_once(items[0]["product_link"])
        input("Press Enter to continue after solving the captcha...")
        
        products_with_ids = []
        
        for item in items:
            try:
                product_id = self.get_product_id(item)
                if product_id == -1 or product_id == "избранное":
                    item = self._default_review(item)
                    item['product_id'] = 0
                    products_with_ids.append(item)
                    print(f"Review for {item['product_link']}: {item}")
                    continue
                item['product_id'] = product_id
                products_with_ids.append(item)
            except Exception as e:
                logging.error(f"Error processing URL {item['product_link']}: {e}")
        
        with open('products_with_ids.json', 'w') as file:
            json.dump(products_with_ids, file, indent=4)

    def get_product_id(self, item):
        print(f"Getting product ID for URL: {item['product_link']}")
        self.driver.get(item['product_link'])
        
        if "Нет в наличии" in self.driver.page_source:
            return -1
        elif "Такого не нашлось" in self.driver.page_source:
            return -1

        selector = '[id="TabAbout"] div:nth-child(3) button'
        product_id_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        product_id_element = product_id_element.text
        print(f"Product ID Element: {product_id_element}")
        product_id = product_id_element.split()[-1]
        print(f"Product ID: {product_id}")
        return product_id
    

    def get_all_reviews(self, item, product_id):
        current_page = 1
        while True:
            time.sleep(random.uniform(0.5, 2.5))
            reviews_response = self._requests(product_id, current_page)
            
            if reviews_response:
                total_reviews = reviews_response.get("totalReviewsCount", 0)
                total_pages = (total_reviews // 10) + (1 if total_reviews % 10 > 0 else 0)
                
                reviews = reviews_response.get("reviews", [])
                
                for review in reviews:
                    self._extract_reviews(item, review)
                
                if current_page >= total_pages:
                    break
                
                current_page += 1
                time.sleep(random.uniform(1, 5))
            

    def _extract_reviews(self, item, review):
        review_data = item.copy()
        review_data.update({
            "data_author": review.get("author", {}).get("name", "Unknown"),
            "data_published_date": review.get("datetime", "Unknown"),
            "data_content": review.get("message", "No message"),
            "data_ratings": review.get("rating", 0),
            "url_status": "Data Extracted"
        })
        self.data.append(review_data)
        logging.info(f"Review extracted for {item['product_link']}")
    
    def _default_review(self, item):
        review_data = item.copy()
        review_data.update({
            "data_author": "",
            "data_published_date": "",
            "data_content": "",
            "data_ratings": "",
            "url_status": "Not found"
        })
        self.data.append(review_data)
        logging.info(f"Product not found for:  {item['product_link']}")
        return review_data

    def _solve_captcha_once(self, url):
        try:
            self.driver.get(url)
            self._wait_for_captcha()
            logging.info("Cookies saved after solving captcha.")
        except WebDriverException as e:
            logging.error(f"Error during captcha solving: {e}")
            raise

    def _wait_for_captcha(self):
        try:
            captcha = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.CheckboxCaptcha"))
            )
            if captcha:
                logging.info("Captcha detected. Please solve it manually.")
                WebDriverWait(self.driver, 300).until_not(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.CheckboxCaptcha'))
                )
                logging.info("Captcha solved. Resuming scraping...")
        except TimeoutException:
            logging.info("No captcha detected.")
        except Exception as e:
            logging.error(f"Error waiting for captcha: {e}")

    def save_to_excel(self):
        if self.data:
            pprint(self.data)
            df = pd.DataFrame(self.data)
            excel_filename = 'scraped_data.xlsx'
            try:
                df.to_excel(excel_filename, index=False)
                logging.info(f"Data saved to {excel_filename}")
            except Exception as e:
                logging.error(f"Failed to save data to Excel: {e}")
        else:
            logging.warning("No data to save.")

    def close_spider(self):
        self.save_to_excel()
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    print("Starting scraping...")
    items = load_items()
    # items = [{"product_link": "https://www.eldorado.ru/cat/detail/kofemashina-krups-quattro-force-evidence-ea891810/"}]
    with SeleniumScraper() as scraper:
        scraper.start_requests(items)
