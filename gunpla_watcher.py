import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime

# 商品URLリスト（必要に応じて追加）
product_urls = [
    "https://www.amazon.co.jp/dp/B0C9S6XZP2",
    "https://www.amazon.co.jp/dp/B0CF5QL1TK"
]

# 保存ディレクトリの作成
output_dir = "amazon_scrape_output"
os.makedirs(output_dir, exist_ok=True)

# ヘッドレスChrome設定
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36')

driver = webdriver.Chrome(options=options)

def extract_data_from_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # タイトル
    title_tag = soup.select_one("#productTitle")
    title = title_tag.get_text(strip=True) if title_tag else "タイトル取得失敗"

    # 価格：複数候補をチェック
    price_selectors = [
        "span.a-price-whole",
        "#priceblock_ourprice",
        "#priceblock_dealprice",
        "#price_inside_buybox",
        ".a-price > span"
    ]
    price = None
    for selector in price_selectors:
        tag = soup.select_one(selector)
        if tag:
            price = tag.get_text(strip=True)
            break
    if not price:
        price = "価格取得失敗"

    # メイン画像
    image_tag = soup.select_one("#landingImage") or soup.select_one("#imgTagWrapperId img")
    image_url = image_tag["src"] if image_tag else "画像取得失敗"

    return title, price, image_url

# 処理スタート
for idx, url in enumerate(product_urls):
    try:
        print(f"[INFO] 処理中: {url}")
        driver.get(url)
        time.sleep(random.uniform(3, 6))  # Bot対策のためランダムな待機

        # ページHTML取得
        html = driver.page_source

        # データ抽出
        title, price, image_url = extract_data_from_html(html)

        # HTML・スクショ保存
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_file = os.path.join(output_dir, f"product_{idx+1}_{ts}.html")
        img_file = os.path.join(output_dir, f"product_{idx+1}_{ts}.png")

        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html)

        driver.save_screenshot(img_file)

        # 出力
        print(f"タイトル: {title}")
        print(f"価格   : {price}")
        print(f"画像URL: {image_url}")
        print("-" * 40)

    except Exception as e:
        print(f"[ERROR] 処理失敗: {e}")

driver.quit()
