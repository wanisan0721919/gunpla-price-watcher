from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform

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

# Amazonガンプラページへアクセス
driver.get("https://www.amazon.co.jp/RG-%E6%A9%9F%E5%8B%95%E6%88%A6%E5%A3%AB%E3%82%AC%E3%83%B3%E3%83%80%E3%83%A0UC-%E3%83%A6%E3%83%8B%E3%82%B3%E3%83%BC%E3%83%B3%E3%82%AC%E3%83%B3%E3%83%80%E3%83%A0-144%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%AB-%E8%89%B2%E5%88%86%E3%81%91%E6%B8%88%E3%81%BF%E3%83%97%E3%83%A9%E3%83%A2%E3%83%87%E3%83%AB/dp/B08XWBS3WM")

# 商品がロードされるのを待機（最大30秒）
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="productTitle"]').get_attribute("value")
)
)

# 商品名の取得（get_attribute("value")を使用）
product_title = driver.find_element(By.XPATH, '//*[@id="productTitle"]').get_attribute("value")

# 商品価格の取得（テキストとして直接取得）
price_elements = driver.find_elements(By.XPATH, '//*[@class="a-price-whole"]')
if price_elements:
    product_price = price_elements[0].text
else:
    product_price = "価格情報が見つかりませんでした"

print(f"価格: {product_price}")

# 結果を表示
print(f"商品名: {product_title}")
print(f"価格: {product_price}")

# WebDriverを終了
driver.quit()
