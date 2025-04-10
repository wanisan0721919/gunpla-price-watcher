from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chromeオプション設定（ヘッドレス＋User-Agent対策）
chrome_options = Options()
chrome_options.add_argument("--headless")  # GUIを表示しない
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")

# WebDriver起動
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.amazon.co.jp/ガンプラストア-Amazon-co-jp/s?rh=n%3A4469780051%2Cp_6%3AAN1VRQENFRJN5")

print(f"Page title: {driver.title}")

wait = WebDriverWait(driver, 10)

try:
    # タイトルの相対XPath
    title_elements = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, '//h2[contains(@class,"a-size")]/a/span')
    ))

    # 価格の相対XPath
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
