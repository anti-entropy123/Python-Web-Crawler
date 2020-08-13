from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as WDW 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import threading
import selenium 
import time

chrome_options = Options()
chrome_options.add_argument('--start-maximized')  # 最大化
chrome_options.add_argument('blink-settings=imagesEnabled=false') # 禁止图片加载
waits = {}
new_window = 'window.open()'
reload_page = 'location.reload();'

# 存放链接地址
# ! 记得换链接的地址
# ! 记得换链接的地址
# ! 记得换链接的地址
links = [
    'http://shop.tfent.cn/Orders/buy.html?quantity=1&goods_id=111',
    'http://shop.tfent.cn/Orders/buy.html?quantity=1&goods_id=112',
    'http://shop.tfent.cn/Orders/buy.html?quantity=1&goods_id=113',
    'http://shop.tfent.cn/Orders/buy.html?quantity=1&goods_id=114',
    'http://shop.tfent.cn/Orders/buy.html?quantity=1&goods_id=115',
    'http://shop.tfent.cn/Orders/buy.html?quantity=1&goods_id=116',
    'http://shop.tfent.cn/Orders/buy.html?quantity=1&goods_id=117',
    ]

def click_buy_it(browser):
    wait = waits[browser]
    while True:
        try:
            buy = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'buyNow'))) # 如果超时的话, 可能是服务器崩溃导致卡了, 得刷新下
            # name = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'goodName')))
            if buy.get_attribute('onclick')==None:
                browser.execute_script(reload_page)
            else:
                ActionChains(browser).move_to_element(buy).move_by_offset(10,10).click().perform()
                pay_it_now(browser)
        except selenium.common.exceptions.TimeoutException:
            browser.execute_script(reload_page)

def pay_it_now(browser):
    wait = waits[browser]
    while True:
        browser.get(links[0])
        try:
            pay = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'支付')]")))
            ActionChains(browser).move_to_element(pay).move_by_offset(10,10).click().perform()
        except selenium.common.exceptions.TimeoutException:
            pass

def home_page(browser):
    browser.get('http://shop.tfent.cn/GoodsCategory/stationery')
    browser.delete_all_cookies()
    # ! 记得更换cookie !!!!!
    # ! 记得更换cookie !!!!!
    # ! 记得更换cookie !!!!!    
    browser.add_cookie({
        'name': 'PHPSESSID',
        'value': 'tob4n02v2pr7oq5n9hi3qplou4'
    })
    browser.get('http://shop.tfent.cn/GoodsCategory/stationery')

def create_new_page(browser, link):
    browser.execute_script(new_window)
    handle = browser.window_handles[-1]
    browser.switch_to_window(handle)
    browser.get(link)

if __name__ == "__main__":
    browsers = []
    for link in links[:1]:
        browser = webdriver.Chrome(chrome_options=chrome_options)
        waits[browser] = WDW(browser, 3)
        browsers.append(browser)
        home_page(browser)
        create_new_page(browser, link)

    for browser in browsers[:1]:
        threading.Thread(target=pay_it_now, args=(browser,)).start()
