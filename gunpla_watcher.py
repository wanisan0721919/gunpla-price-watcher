import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
driver.get("https://www.amazon.co.jp/ガンプラストア-Amazon-co-jp/s?rh=n%3A4469780051%2Cp_6%3AAN1VRQENFRJN5")

# ページが完全に読み込まれるのを待機（最大30秒）
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//h2[contains(@class,"a-size-base-plus a-spacing-none a-color-base a-text-normal")]'))
)

# ページが完全に読み込まれた後にスクロールを実行（ページの下まで）
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# 商品タイトルと価格のXPath
product_titles = driver.find_elements(By.XPATH, '//h2[contains(@class,"a-size-base-plus a-spacing-none a-color-base a-text-normal")]/span[1]')
product_prices = driver.find_elements(By.XPATH, '//span[contains(@class,"a-offscreen")]')

# 結果を表示
for title, price in zip(product_titles, product_prices):
    print(f"商品名: {title.text}, 価格: ¥{price.text}")

# WebDriverを終了
driver.quit()
