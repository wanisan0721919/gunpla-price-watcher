import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import platform
import chromedriver_autoinstaller
from bs4 import BeautifulSoup

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

        # ページの読み込みを待つ
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "productTitle"))
        )

        # ページのHTMLを取得して保存
        page_source = driver.page_source
        with open("amazon_page.html", "w", encoding="utf-8") as file:
            file.write(page_source)
        logging.info("ページのHTMLを保存しました")

        # BeautifulSoupでHTML解析
        soup = BeautifulSoup(page_source, "html.parser")

        # 商品タイトルの取得
        title = soup.find("span", {"id": "productTitle"})
        if title:
            title = title.text.strip()
        else:
            title = "商品タイトルの取得に失敗"
            logging.error("商品タイトルの取得に失敗")
        
        # 価格情報の取得
        price = soup.find("span", {"class": "a-price-whole"})
        if price:
            price = price.text.strip()
        else:
            price = "価格情報が見つかりませんでした"
            logging.error("価格情報が見つかりませんでした")
        
        # 商品画像の取得
        image_url = soup.find("img", {"id": "landingImage"})
        if image_url:
            image_url = image_url["src"]
        else:
            image_url = "画像の取得に失敗"
            logging.error("画像の取得に失敗")

        # 結果の出力
        print(f"商品タイトル: {title}")
        print(f"価格: {price}")
        print(f"画像URL: {image_url}")

    except TimeoutException:
        logging.error("ページの読み込みに時間がかかりすぎました")
    finally:
        driver.quit()

if __name__ == "__main__":
    # 監視したいAmazonのURLを設定
    url = "https://amzn.to/4cwpLBY"
    fetch_gunpla_info(url)
