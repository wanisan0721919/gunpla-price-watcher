import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By

# OSに応じて適切なブラウザパスを設定
if platform.system() == "Windows":
    BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # Windows用
else:
    BRAVE_PATH = "/usr/bin/google-chrome-stable"  # Linux環境でGoogle Chromeを使用

# Chromeオプション設定
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--headless")  # ヘッドレスモードを外す

# Braveのバイナリを指定
chrome_options.binary_location = BRAVE_PATH

# chromedriver_autoinstallerを使って対応するバージョンをインストール
chromedriver_autoinstaller.install()

# WebDriverを作成
driver = webdriver.Chrome(options=chrome_options)

# 任意の操作を実行
driver.get("https://www.amazon.co.jp/")  # 例としてAmazonにアクセス

# ページタイトルを表示
print("Page title:", driver.title)

# 商品名と価格を取得
product_titles = driver.find_elements(By.XPATH, "//span[contains(@class, 's-title')]")
product_prices = driver.find_elements(By.XPATH, "//span[contains(@class, 'a-price-whole')]")

# 結果を表示
for title, price in zip(product_titles, product_prices):
    print(f"商品名: {title.text}, 価格: ¥{price.text}")

# WebDriverを終了
driver.quit()
