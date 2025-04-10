from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome ドライバのオプションを設定
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

# Chrome ドライバを起動
driver = webdriver.Chrome(options=chrome_options)

# Amazon のページを開く
url = "https://www.amazon.co.jp/ガンプラストア-Amazon-co-jp/s?rh=n%3A4469780051%2Cp_6%3AAN1VRQENFRJN5"
driver.get(url)

# ページタイトルを表示
print("Page title:", driver.title)

# 商品名の取得
try:
    product_titles = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//*[@id='928891d6-63a0-4a13-bcff-82c2d4bbdbcd']"))
    )
    for title in product_titles:
        print("商品名:", title.text)
except Exception as e:
    print("商品名の取得に失敗しました:", e)

# 価格の取得
try:
    price_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//*[@id='corePriceDisplay_desktop_feature_div']/div[1]/span[1]"))
    )
    for price in price_elements:
        print("価格:", price.text)
except Exception as e:
    print("価格の取得に失敗しました:", e)

# ブラウザを閉じる
driver.quit()
