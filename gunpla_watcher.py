import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import platform
import chromedriver_autoinstaller

# ログ設定
logging.basicConfig(level=logging.INFO)

def create_driver():
    # OSに応じて適切なブラウザパスを設定
    if platform.system() == "Windows":
        BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    else:
        BRAVE_PATH = "/usr/bin/google-chrome-stable"

    # Chromeオプション設定
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")  # ヘッドレスモード

    # Braveのバイナリを指定（もしくはGoogle Chrome）
    chrome_options.binary_location = BRAVE_PATH

    # 対応するchromedriverを自動インストール
    chromedriver_autoinstaller.install()

    # WebDriver作成
    driver = webdriver.Chrome(options=chrome_options)

    return driver

def fetch_gunpla_info(url):
    driver = create_driver()
    
    try:
        # URLにアクセス
        driver.get(url)
        time.sleep(3)  # ページが完全にロードされるまで待機

        # 商品タイトルの取得
        try:
            title = driver.find_element(By.ID, "productTitle").text
            logging.info(f"商品タイトル: {title}")
        except NoSuchElementException:
            title = "商品タイトルの取得に失敗"
            logging.error("商品タイトルの取得に失敗")

        # 価格情報の取得
        try:
            price = driver.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
            logging.info(f"価格: {price}")
        except NoSuchElementException:
            price = "価格情報が見つかりませんでした"
            logging.error("価格情報が見つかりませんでした")

        # 商品画像の取得
        try:
            image_url = driver.find_element(By.ID, "landingImage").get_attribute("src")
            logging.info(f"画像URL: {image_url}")
        except NoSuchElementException:
            image_url = "画像の取得に失敗"
            logging.error("画像の取得に失敗")

        # 結果の出力
        print(f"商品タイトル: {title}")
        print(f"価格: {price}")
        print(f"画像URL: {image_url}")

    finally:
        driver.quit()

if __name__ == "__main__":
    # 監視したいAmazonのURLを設定
    url = "https://amzn.to/4cwpLBY"
    fetch_gunpla_info(url)
