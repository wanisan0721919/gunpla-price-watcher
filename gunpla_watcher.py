import os
import logging
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
import platform
from time import sleep
import time


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
    url = 'https://www.amazon.co.jp/dp/B07VJYZF9T'  # 実際のURLに変更してください
    html_file = download_html(url)

    if html_file:
        title, price, img_url = extract_data_from_html(html_file)
        
        # 取得したデータの表示
        logger.info(f"商品タイトル: {title}")
        logger.info(f"価格: {price}")
        logger.info(f"画像URL: {img_url}")

        # GitHub Actionsの場合、アーティファクトとしてアップロード
        # アーティファクトアップロード部分
        if os.environ.get("GITHUB_ACTIONS"):
            from github_actions import upload_artifact
            upload_artifact(html_file)

if __name__ == "__main__":
    main()
