import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# OSに応じて適切なブラウザパスを設定
if platform.system() == "Windows":
    BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # Windows用
else:
    BRAVE_PATH = "/usr/bin/google-chrome-stable"  # Linux環境でGoogle Chromeを使用

# Chromeオプション設定
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")  # ヘッドレスモード

# Braveのバイナリを指定
chrome_options.binary_location = BRAVE_PATH

# --user-data-dirを追加していないか確認（削除）
# chrome_options.add_argument("--user-data-dir=/path/to/some/directory")  # この行があった場合、削除またはコメントアウト

# chromedriver_autoinstallerを使って対応するバージョンをインストール
chromedriver_autoinstaller.install()

# WebDriverを作成
driver = webdriver.Chrome(options=chrome_options)

# 任意の操作を実行
driver.get("https://www.amazon.co.jp/")  # 例としてAmazonにアクセス

# ページタイトルを表示
print("Page title:", driver.title)

# 商品名と価格を取得する前に、要素がロードされるのを待つ
wait = WebDriverWait(driver, 10)  # 最大10秒間待機
product_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 's-title')]")))
product_prices = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'a-price-whole')]")))

# 結果を表示
for title, price in zip(product_titles, product_prices):
    print(f"商品名: {title.text}, 価格: ¥{price.text}")

# WebDriverを終了
driver.quit()
