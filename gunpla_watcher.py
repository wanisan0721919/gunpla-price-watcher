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

# 商品ページにアクセス
driver.get("https://www.amazon.co.jp/RG-%E6%A9%9F%E5%8B%95%E6%88%A6%E5%A3%AB%E3%82%AC%E3%83%B3%E3%83%80%E3%83%A0UC-%E3%83%A6%E3%83%8B%E3%82%B3%E3%83%BC%E3%83%B3%E3%82%AC%E3%83%B3%E3%83%80%E3%83%A0-144%E3%82%B9%E3%82%B1%E3%83%BC%E3%83%AB-%E8%89%B2%E5%88%86%E3%81%91%E6%B8%88%E3%81%BF%E3%83%97%E3%83%A9%E3%83%A2%E3%83%87%E3%83%AB/dp/B08XWBS3WM/ref=sr_1_1?dib=eyJ2IjoiMSJ9.ydGC_Br1xhMandLowCJHyOTJDFXeRrf2UfWFUSFPF-6hQ6NeGOCrCpDMiP7A21Df_royV4Ace4QB-tV7Q5lMVh7kmDJJQ1g6H2vZyPwNiecSteZOGHPlt0rVZWyLu3o8pfSls-ecoLVA3O7VWYrerx3rAzNHNPLL-DaVr7qZvvp_ZC6Duk_KMQWd8lJNK_C1y4XVKfXJpunenThXhv6NzPScS0C7LMJWTCi6pMKS1ulSs4tCAyhyoSbrTb2dwmtRgVruE_u5NC3QHQyBKL-zS8GsbbS7bddke3C0L0lxklA.BVeOmAMFAzU9f5nEP8OjY-vhDtYA7XVMpmm6A-_6ODQ&dib_tag=se&m=AN1VRQENFRJN5&qid=1744251790&refinements=p_6%3AAN1VRQENFRJN5&s=hobby&sr=1-1")

# 価格の要素が表示されるのを待つ
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[2]'))
)

# 商品タイトルと価格を取得
product_title = driver.find_element(By.XPATH, '//*[@id="productTitle"]')
product_price = driver.find_element(By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[2]')

# 結果表示
print(f"商品名: {product_title.text}")
print(f"価格: ¥{product_price.text}")

# WebDriverを終了
driver.quit()
