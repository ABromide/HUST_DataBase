import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from detect_alert import detect_alert

def change_depcity_get_info(browser,wait,depcity,date):
    '''
    重新搜索离开城市时获取页面源代码
    '''
    CityTag = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="dcity0"]')))
    time.sleep(2)
    CityTag.clear()
    CityTag.send_keys(depcity)

    SearchTag = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="searchModify"]/div[3]/a[1]')))
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