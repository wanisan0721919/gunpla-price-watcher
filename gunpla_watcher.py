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

# 任意の商品ページにアクセス
driver.get("https://www.amazon.co.jp/dp/B01N5IB20Q")  # 例としてガンプラの商品ページURL

# 商品タイトルが読み込まれるのを待機（最大30秒）
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="productTitle"]'))
)

# 商品名を取得
product_title = driver.find_element(By.XPATH, '//*[@id="productTitle"]').text
print(f"商品名: {product_title}")

# WebDriverを終了
driver.quit()
