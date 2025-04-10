import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

# OSに応じて適切なブラウザパスを設定
if platform.system() == "Windows":
    BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # Windows用
else:
    BRAVE_PATH = "/usr/bin/brave-browser"  # Linux用（GitHub Actions環境）

# Chromeオプション設定
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# ヘッドレスモードを使わない場合はコメントアウト
# chrome_options.add_argument("--headless")  # ヘッドレスモード

# Braveのバイナリを指定
chrome_options.binary_location = BRAVE_PATH

# chromedriver_autoinstallerを使って対応するバージョンをインストール
chromedriver_autoinstaller.install()

# WebDriverを作成
driver = webdriver.Chrome(options=chrome_options)

# 任意の操作を実行
driver.get("https://www.amazon.co.jp/")  # 例としてAmazonにアクセス
print(driver.title)  # ページタイトルを表示

# スクリプトの続きを記述...
