
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import random
from selenium.webdriver.common.keys import Keys

# 1. Khai báo browser
browser = webdriver.Chrome()

# 2. Mở URL của post
browser.get("https://www.facebook.com/khiabongdane/posts/pfbid02fvf4S4MwL2HTeFdHt7ifEFhvA6tk7WZsK4pa8xT5u9Tgjg1uZgUAwpDnQdtVhWzAl")

# 2a. Điền thông tin vào ô user và pass

txtUser = browser.find_element(By.ID,"email")
txtUser.send_keys("email") # <---  Điền email/sdt

txtPass = browser.find_element(By.ID,"pass")
txtPass.send_keys("pass") # <--- Điền pass

# 2b. Submit form

txtPass.send_keys(Keys.ENTER)

sleep(18)
# 4a. Đổi chế độ lọc bình luận
showall_link = browser.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[2]/div[2]/div/div/div/span")
showall_link.click()
sleep(3)
# 4b. Lọc tất cả bình luận
showall_link2 = browser.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div[3]/div[1]/div/div[1]/span")
showall_link2.click()
sleep(10)
try:
    for i in range(3):
        showmore_link = browser.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[2]/div[4]/div[1]/div[2]")
        showmore_link.click()
        sleep(random.randint(5,10))
except:
    {

    }

# 5. Tìm tất cả các comment 

comment_list = browser.find_elements(By.XPATH,"//div[@dir='auto'][@style='text-align: start;']")

record = []
# Lặp trong tất cả các comments và lưu comment
for comment in comment_list:
    record.append(('',comment.text))
df = pd.DataFrame(data=record,columns=['Label','Comment'])
print(df.head())
df.to_csv('Dataset.csv',mode='a', encoding="utf-8-sig")

# 6. Đóng browser