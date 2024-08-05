# 爬取ig關鍵字圖片

from selenium import webdriver
import time
# Explicit Waits
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Keys 模擬鍵盤
from selenium.webdriver.common.keys import Keys
# 路徑
import os
# 下載爬到的資料
import wget

driver = webdriver.Chrome()
driver.get("https://www.instagram.com/")

# 等待網頁載入
# 等到name屬性值為username的HTML標籤出現，才繼續執行其他動作
username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "username"))
)
password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "password"))
)

# 抓取登入按鈕
login = driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[3]/button')


# 清空輸入框預設值
username.clear()
password.clear()

# 輸入帳號密碼
username.send_keys("你的帳號")
password.send_keys("你的密碼")

# 點擊登入按鈕
login.click()

# 登入後等待頁面跳轉到 詢問開啟通知 出現的頁面
wait = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]'))
)

# 點擊 稍後再說 按鈕
wait.click()

# 等待頁面跳轉到 搜尋輸入框 出現的頁面
search = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0_n/"]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/nav/div/header/div/div/div[1]/div/div/div/div/div/input'))
)

keyword = "#想要搜尋的關鍵字"

# 於搜尋框中輸入關鍵字
search.send_keys(keyword)
time.sleep(1)
# 按下ENTER 2次 搜尋
search.send_keys(Keys.RETURN)
time.sleep(1)
search.send_keys(Keys.RETURN)

# 等待搜尋結果出現
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'FFVAD'))
)

# 視窗捲到底 讓更多圖片被載入 捲5次
for i in range(5):
    # 執行js程式碼
    # 將視窗捲到 x座標為0 y座標為視窗高度處(原點位於視窗左上角)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 等到更多圖片被載入
    time.sleep(5)

# 抓取圖片
imgs = driver.find_element(By.CLASS_NAME,'FFVAD')

# 存放下載下來的圖片之資料夾
path = os.path.join(keyword)
# 以搜尋關鍵字為資料夾名稱，建立資料夾
os.mkdir(path)

count = 0
for img in imgs:
    # 路徑 檔案名稱
    save_as = os.path.join(path, keyword + str(count) + '.jpg')
    # 下載(圖片網路位置，圖片要下載到本機哪裡)
    wget.download(img.get_attribute("src"), save_as)
    count += 1


time.sleep(120)