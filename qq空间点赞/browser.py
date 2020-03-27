# code=utf-8

from selenium.webdriver.chrome.options import Options
from selenium import webdriver 
import time

chrome_options = Options()
# 如果是无界面的浏览 
# chrome_options.add_argument('--headless')
chrome = webdriver.Chrome(chrome_options=chrome_options)  #浏览器驱动

you_qq_number = 1348****580   # 你的QQ号
you_qq_password = "you don't know" #你的密码
friends_qq_number = 1076014015     # 你想给点赞的好友的q号
number_of_like = 0           # 记录点了多少赞

# 将find_element_by_xpath()方法封装, 作用是可以反复查找那些因为加载延迟而无法定位的元素, 避免因为这些情况导致程序崩溃
def locate(xpath):
    times = 1
    while True:
        try:    
            return chrome.find_element_by_xpath(xpath)
        except:
            print("第"+str(times)+"次定位"+xpath+"失败")
            times = times + 1
            time.sleep(1)

# 将视角锁定到这个元素上, 不然可能无法点击
def view_to_element(element):
    chrome.execute_script("arguments[0].scrollIntoView();",element)

# 模拟点赞
def click_like(number):
    xpath = "//*[@id='host_home_feeds']/li["+str(number)+"]"
    view_to_element(locate(xpath)) 
    if number==1 and locate(xpath+"/div[1]").get_attribute("class") == 'f-single-top':
        # 存在置顶说说时
        xpath += "/div[4]/div[1]/p/a[3]"
    else:
        xpath += "/div[3]/div[1]/p/a[3]"
    if locate(xpath).get_attribute('data-clicklog') == "like":            
        locate(xpath+"/i").click()
        global number_of_like
        number_of_like += 1
        print("the number of clicking like is : "+str(number_of_like))

# 初始化
def initial():
    # 开启页面
    chrome.get("https://user.qzone.qq.com/"+str(you_qq_number) +"/main")
    chrome.maximize_window()
    chrome.implicitly_wait(30)

    # 帐号密码登陆
    chrome.switch_to.frame("login_frame")
    chrome.find_element_by_link_text("帐号密码登录").click()

    chrome.find_element_by_id("u").send_keys(you_qq_number)
    chrome.find_element_by_id("p").send_keys(you_qq_password)
    chrome.find_element_by_id("login_button").click()

    time.sleep(5)
    locate("//*[@id='id_photowall_closetips']/s").click()
    locate("//a[//*[@id='qz_notification']/a[2]]").click()    

    chrome.get("https://user.qzone.qq.com/"+str(friends_qq_number) +"/main")
    time.sleep(5)
    #if you_qq_number != friends_qq_number:
        # 关掉烦人的弹窗
        # chrome.find_element_by_xpath("//*[@id='friendship_promote_layer']/table/tbody/tr[1]/td[2]/a").click()
    chrome.switch_to.frame(locate("//*[@id='app_canvas_frame']"))
    chrome.switch_to.frame(locate("//*[@id='frameFeedList']"))

# 遍历说说, 并且下拉加载更多
def start_to_like(number):
    for x in range(number):
        try:
            chrome.find_element_by_xpath("//*[@id='host_home_feeds']/li["+str(x+1)+"]")
        except:
            view_to_element(locate("//*[@id='ICFeedsTipMsg']"))
        click_like(x+1)
# 主函数
def main():
    initial()
    start_to_like(1000)
    print("click like complete")
    time.sleep(30)
    # chrome.quit()

if __name__ == "__main__":
    main()
