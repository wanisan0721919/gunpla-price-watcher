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

# Amazonにアクセス
driver.get("https://www.amazon.co.jp/")

# ページタイトルを表示
print(f"Page title: {driver.title}")

# WebDriverWaitを設定して要素が表示されるのを待つ
wait = WebDriverWait(driver, 10)

# 商品タイトルのXPathを指定
title_xpath = "//*[@id='title_feature_div']//span[@id='productTitle']"

# 商品タイトルを取得
try:
    product_title = wait.until(EC.presence_of_element_located((By.XPATH, title_xpath)))
    print(f"商品タイトル: {product_title.text}")
except Exception as e:
    print(f"エラーが発生しました: {e}")

# WebDriverを終了
driver.quit()
