from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

# Braveブラウザの実行パス
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

# Chromeオプション設定
chrome_options = Options()
chrome_options.add_argument("--headless")  # ヘッドレスモード
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Braveのバイナリを指定
chrome_options.binary_location = BRAVE_PATH

# chromedriver_autoinstallerを使って対応するバージョンをインストール
chromedriver_autoinstaller.install()

# WebDriverを作成
driver = webdriver.Chrome(options=chrome_options)

# スクリプトの続きを記述...
