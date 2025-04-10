import os
import logging
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
import platform
from time import sleep

# ログの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# ヘッドレスブラウザの自動化検出を回避するオプション
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# ユーザーエージェントを一般的なものに変更
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

# Braveのバイナリを指定（もしくはGoogle Chrome）
chrome_options.binary_location = BRAVE_PATH

# 対応するchromedriverを自動インストール
chromedriver_autoinstaller.install()

# WebDriver作成
driver = webdriver.Chrome(options=chrome_options)

def download_html(url):
    try:
        driver.get(url)
        sleep(5)  # ページが完全に読み込まれるまで待機
        html_content = driver.page_source
        # HTMLファイルとして保存
        filename = "amazon_page.html"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)
        logger.info(f"HTMLファイルを保存しました: {filename}")
        return filename
    except Exception as e:
        logger.error(f"HTMLの保存に失敗しました: {e}")
        return None

def extract_data_from_html(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
        
        # 商品タイトルの取得
        title_element = soup.find('span', {'id': 'productTitle'})
        title = title_element.get_text(strip=True) if title_element else '商品タイトルの取得に失敗'
        
        # 価格情報の取得
        price_element = soup.find('span', {'class': 'a-price-whole'})
        price = price_element.get_text(strip=True) if price_element else '価格情報が見つかりませんでした'
        
        # 画像URLの取得
        img_element = soup.find('img', {'id': 'landingImage'})
        img_url = img_element['src'] if img_element else '画像の取得に失敗'
        
        return title, price, img_url
    except Exception as e:
        logger.error(f"データの抽出に失敗しました: {e}")
        return 'データ抽出に失敗', 'データ抽出に失敗', 'データ抽出に失敗'

def main():
    url = 'https://www.amazon.co.jp/BANDAI-SPIRITS-%E3%83%90%E3%83%B3%E3%83%80%E3%82%A4-%E3%82%B9%E3%83%94%E3%83%AA%E3%83%83%E3%83%84-%E3%82%A2%E3%83%A1%E3%82%A4%E3%82%B8%E3%83%B3%E3%82%B0%E3%82%BA%E2%82%AC%E3%82%B3%E3%82%AD%E3%82%92%E3%82%B8%E3%83%91%E3%82%A4%E3%82%B0%E3%83%AB%E3%83%9E%E3%82%B8%E3%83%BC%E5%AF%92%E6%85%8B-%E3%82%AA%E3%82%B5%E3%83%96%E3%82%AB%E3%83%BB%E5%85%A8%E3%82%89%E9%9B%BB%E5%AD%90%CE%A9%E5%93%9A%E6%92%AC%E7%92%B0/dp/B08GYBQQVV'
    html_file = download_html(url)

    if html_file:
        title, price, img_url = extract_data_from_html(html_file)
        
        # 取得したデータの表示
        logger.info(f"商品タイトル: {title}")
        logger.info(f"価格: {price}")
        logger.info(f"画像URL: {img_url}")

if __name__ == "__main__":
    main()
