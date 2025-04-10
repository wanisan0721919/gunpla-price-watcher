from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import time
import requests
from bs4 import BeautifulSoup
import re

# Braveブラウザの実行パス
BRAVE_PATH = "/usr/bin/brave-browser"  # ここでBraveのパスを指定（例: Ubuntuの場合）

# アフィリエイトタグ
AFFILIATE_TAG = "infonatumi-22"

# 監視URL
URL = "https://www.amazon.co.jp/ガンプラストア-Amazon-co-jp/s?rh=n%3A4469780051%2Cp_6%3AAN1VRQENFRJN5"

# Chromeオプション設定
chrome_options = Options()
chrome_options.add_argument("--headless")  # ヘッドレスモード
chrome_options.add_argument("--no-sandbox")  # 安全でない操作を避ける
chrome_options.add_argument("--disable-dev-shm-usage")

# Braveのバイナリを指定
chrome_options.binary_location = BRAVE_PATH

# chromedriver_autoinstallerを使って対応するバージョンをインストール
chromedriver_autoinstaller.install()

# WebDriverを作成
driver = webdriver.Chrome(options=chrome_options)

# URLを開く
driver.get(URL)

# ページのHTMLを取得
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 商品ブロックを取得（セレクタは調整必要）
items = soup.select('.s-result-item')

for item in items:
    title_tag = item.select_one('h2 span')
    current_price_tag = item.select_one('.a-price .a-offscreen')
    original_price_tag = item.select_one('.a-text-price .a-offscreen')
    link_tag = item.select_one('h2 a')

    if not (title_tag and current_price_tag and original_price_tag and link_tag):
        continue

    title = title_tag.get_text(strip=True)
    current_price = int(re.sub(r'[^\d]', '', current_price_tag.text))
    original_price = int(re.sub(r'[^\d]', '', original_price_tag.text))
    asin_match = re.search(r'/dp/([A-Z0-9]{10})', link_tag['href'])
    asin = asin_match.group(1) if asin_match else None

    if current_price <= original_price and asin:
        print(f"? {title}")
        print(f"価格: ¥{current_price}（定価: ¥{original_price}）")
        print(f"https://www.amazon.co.jp/dp/{asin}/?tag={AFFILIATE_TAG}")
        print("-" * 40)

# ブラウザを閉じる
driver.quit()
