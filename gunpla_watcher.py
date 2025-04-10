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

# chromedriver_autoinstallerを使って対応するバージョンをインストール
chromedriver_autoinstaller.install()

# WebDriverを作成
driver = webdriver.Chrome(options=chrome_options)

# ガンプラストアページにアクセス
url = "https://www.amazon.co.jp/ガンプラストア-Amazon-co-jp/s?rh=n%3A4469780051%2Cp_6%3AAN1VRQENFRJN5"
driver.get(url)

# ページタイトルを表示
print(f"Page title: {driver.title}")

# WebDriverWaitを設定して要素が表示されるのを待つ
wait = WebDriverWait(driver, 10)

# 商品名と価格を取得
try:
    # 商品ごとに異なるXPathを指定して商品名を取得
    product_titles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='928891d6-63a0-4a13-bcff-82c2d4bbdbcd'] | //*[@id='140bcc6f-7cc9-45cb-987d-c9d8b00803c5']")))
    for title in product_titles:
        print(f"商品名: {title.text}")
except Exception as e:
    print(f"商品名の取得に失敗しました: {e}")

# 商品価格を取得
try:
    product_price = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='corePriceDisplay_desktop_feature_div']/div[1]/span[1]")))
    print(f"商品価格: {product_price.text}")
except Exception as e:
    print(f"価格の取得に失敗しました: {e}")

# WebDriverを終了
driver.quit()
