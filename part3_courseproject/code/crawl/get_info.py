import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from detect_alert import detect_alert

def get_info(browser,wait,DepCity,ArrCity,date):
    '''
    获取某日从某地到某地的机票页面源代码，提供给后续函数解析
    '''
    browser.get('https://www.ctrip.com/')

    # 从首页选择进入机票页面
    AirticketTag = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="searchBoxUl"]/li[2]')))
    time.sleep(2)
    browser.execute_script("arguments[0].click();", AirticketTag)

    # 选择日期
    DateTag = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="FD_StartDate"]')))
    time.sleep(2)
    DateTag.send_keys(date) 

    # 选择出发城市
    DepTag = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="FD_StartCity"]')))
    time.sleep(2)
    DepTag.clear()
    DepTag.send_keys(DepCity)

    # 选择到达城市
    ArrTag = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="FD_DestCity"]')))
    time.sleep(2)
    ArrTag.clear()
    ArrTag.send_keys(ArrCity)
    
    # 开始搜索
    SearchTag = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="FD_StartSearch"]')))
    time.sleep(2)
    SearchTag.click()
    #browser.execute_script("arguments[0].click();", SearchTag)

    # 检查警告信息
    detect_alert(browser)

    # 模拟下拉5次
    for i in range(5):
    	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    source = browser.page_source
    return source