from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from undetected_chromedriver import Chrome, ChromeOptions
import time
import pandas as pd
from pprint import pprint
import logging
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

from input_files.utils import load_items


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SeleniumScraper:
    def __init__(self, driver):
        self.driver = driver
        self.cookies = {}
        self.data = []
        self.reviews = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_spider()

    @staticmethod
    def initialize_driver():
        try:
            chrome_options = ChromeOptions()
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36')
            return Chrome(driver_executable_path=ChromeDriverManager().install(), options=chrome_options)
        except WebDriverException as e:
            logging.error(f"Failed to initialize driver: {e}")
            raise

    def start_requests(self, items):
        if not items:
            logging.warning("No items to process.")
            return

        try:
            logging.info("Solving captcha...")
            logging.info(f"First product link: {items[0]['product_link']}")
            self._solve_captcha_once(items[0]["product_link"])
            input("Press Enter to continue after solving the captcha...")
        except Exception as e:
            logging.error(f"Error during start_requests: {e}")
            return

        for item in items:
            try:
                self.get_product_reviews(item)
            except Exception as e:
                logging.error(f"Error processing URL {item['product_link']}: {e}")

    def get_product_reviews(self, item):
        try:
            self._load_product_page(item["product_link"], item)
            self._click_reviews_button(item)
            self._load_all_reviews()
            self._extract_reviews(item)
        except Exception as e:
            logging.error(f"Error fetching product reviews: {e}")

    def _load_product_page(self, url, item):
        try:
            self.driver.get(url)
            
            if "Такого не нашлось" in self.driver.page_source:
                logging.warning(f"Product not found for {url}")
                self._handle_missing_reviews(item, status="Not Found")
                raise  Exception("Product not found")
        except WebDriverException as e:
            logging.error(f"Failed to load product page {url}: {e}")

    def _click_reviews_button(self, item):
        try:
            reviews_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="fI gI fT"]'))
            )
            reviews_button.click()
            time.sleep(10)
        except TimeoutException:
            logging.warning(f"Reviews button not found for {item['product_link']}")
            self._handle_missing_reviews(item)

    def _handle_missing_reviews(self, item, status="No Reviews"):
        item["data_author"] = ""
        item["data_published_date"] = ""
        item["data_content"] = ""
        item["data_ratings"] = ''
        item["url_status"] = status
        logging.info(f"No reviews found for {item['product_link']}")
        self.data.append(item)

    def _load_all_reviews(self):
        while True:
            try:
                show_more_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="tz zz Bz wz"]'))
                )
                show_more_button.click()
                time.sleep(2)
            except TimeoutException:
                logging.info("No more reviews to load.")
                break

    def _extract_reviews(self, item):
        try:
            reviews = self.driver.find_elements(By.CSS_SELECTOR, '[class="LX"]')
            if not reviews:
                logging.warning(f"No reviews found for {item['product_link']}")
                self._handle_missing_reviews(item)
                return

            for review in reviews:
                try:
                    author = review.find_element(By.CSS_SELECTOR, 'span[class="PX"]').text
                    published_date = review.find_element(By.CSS_SELECTOR, 'span[class="SX"]').text
                    content = review.find_element(By.CSS_SELECTOR, '[class="TX"]').text
                    ratings = len(review.find_elements(By.XPATH, './/img[@class="nC" and contains(@src, "star.c1826360.svg")]'))
                    
                    
                    item["data_author"] = author
                    item["data_published_date"] = published_date
                    item["data_content"] = content
                    item["data_ratings"] = ratings
                    item["url_status"] = "Data Extracted"
                    logging.info(f"Extracted review for {item['product_link']}")
                    print(item)
                    self.data.append(item.copy())
                except NoSuchElementException as e:
                    logging.error(f"Failed to extract review element: {e}")
        except Exception as e:
            logging.error(f"Error extracting reviews: {e}")

    def _solve_captcha_once(self, url):
        try:
            self.driver.get(url)
            self._wait_for_captcha()
            self.cookies = {cookie['name']: cookie['value'] for cookie in self.driver.get_cookies()}
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


if __name__ == "__main__":
    try:
        items = [item for item in load_items()]
        driver = SeleniumScraper.initialize_driver()
        with SeleniumScraper(driver) as scraper:
            scraper.start_requests(items)
    except Exception as e:
        logging.error(f"An error occurred during scraping: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
