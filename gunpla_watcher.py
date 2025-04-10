from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # ←追加

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0")

# ★ 自動でChromeDriverを適切なバージョンで取得して使う
# バージョンを明示指定（Chrome 135 に対応するドライバー）
service = Service(ChromeDriverManager(version="135.0.7049.84").install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.amazon.co.jp/ガンプラストア-Amazon-co-jp/s?rh=n%3A4469780051%2Cp_6%3AAN1VRQENFRJN5")

wait = WebDriverWait(driver, 10)

try:
    title_elements = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, '//h2[contains(@class,"a-size")]/a/span')
    ))

    price_elements = driver.find_elements(
        By.XPATH, '//span[contains(@class,"a-offscreen")]'
    )

    for i in range(min(len(title_elements), len(price_elements))):
        title = title_elements[i].text
        price = price_elements[i].text
        print(f"{i+1}. 商品名: {title} / 価格: {price}")

except Exception as e:
    print(f"エラーが発生しました: {e}")

finally:
    driver.quit()
