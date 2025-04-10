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
chrome_options.add_argument("--disable-gpu")  # GPUを無効化 (一部環境での安定性向上)
chrome_options.add_argument("--window-size=1920x1080")  # ウィンドウサイズを指定（エラー回避用）

# ユーザーエージェントを変更
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")

# Braveのバイナリを指定（もしくはGoogle Chrome）
chrome_options.binary_location = BRAVE_PATH

# 対応するchromedriverを自動インストール
chromedriver_autoinstaller.install()

# 古いchromedriverがインストールされている場合は削除
chromedriver_path = "/usr/local/bin/chromedriver"
if os.path.exists(chromedriver_path):
    os.remove(chromedriver_path)

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
    url = 'https://www.amazon.co.jp/BANDAI-SPIRITS-%E3%83%90%E3%83%B3%E3%83%80%E3%82%A4-%E3%82%B9%E3%83%94%E3%83%AA%E3%83%83%E3%83%84-%E3%82%A2%E3%83%A1%E3%82%A4%E3%82%B8%E3%83%B3%E3%82%B0%E3%82%BA%E3%82%B0/dp/B0DV371Z9P/?_encoding=UTF8&pd_rd_w=CFob6&content-id=amzn1.sym.bcc66df3-c2cc-4242-967e-174aec86af7a%3Aamzn1.symc.a9cb614c-616d-4684-840d-556cb89e228d&pf_rd_p=bcc66df3-c2cc-4242-967e-174aec86af7a&pf_rd_r=1SHZY3R56BF6XH1F4JCA&pd_rd_wg=fqpv8&pd_rd_r=9ac08d43-bee1-4746-87a4-819f2368455c&ref_=pd_hp_d_atf_ci_mcx_mr_ca_hp_atf_d'  # 実際のURLに変更してください
    html_file = download_html(url)

    if html_file:
        title, price, img_url = extract_data_from_html(html_file)
        
        # 取得したデータの表示
        logger.info(f"商品タイトル: {title}")
        logger.info(f"価格: {price}")
        logger.info(f"画像URL: {img_url}")

if __name__ == "__main__":
    main()
