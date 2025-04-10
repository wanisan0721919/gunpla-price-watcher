from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time

# Chromeのオプション設定
chrome_options = Options()
chrome_options.add_argument("--headless")  # ヘッドレスモード

# ChromeDriverのインストール
chromedriver_autoinstaller.install()

# WebDriverの作成
driver = webdriver.Chrome(options=chrome_options)

# 商品ページのURL（例: RG ガンダムUC）
url = "https://www.amazon.co.jp/dp/B08XWBS3WM"

# 商品ページを開く
driver.get(url)

# 少し待つ（ページ読み込みのため）
time.sleep(3)

# 商品タイトルの取得
try:
    title = driver.find_element(By.ID, "productTitle").text
    print(f"商品タイトル: {title}")
except Exception as e:
    print(f"商品タイトルの取得に失敗: {e}")

# 商品価格の取得
try:
    price = driver.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
    print(f"価格: {price}")
except Exception as e:
    print(f"価格情報が見つかりませんでした: {e}")

# 商品画像の取得
try:
    img_url = driver.find_element(By.ID, "landingImage").get_attribute("src")
    print(f"画像URL: {img_url}")
except Exception as e:
    print(f"画像の取得に失敗: {e}")

# WebDriverを終了
driver.quit()
