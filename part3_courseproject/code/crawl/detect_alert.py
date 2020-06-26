import time

def detect_alert(browser):
    '''
    检测并处理可能存在的警告提示信息
    '''
    try:
        time.sleep(1)
        AlertTag = browser.find_element_by_class_name('btn-group')
        time.sleep(1)
        #browser.execute_script("arguments[0].click();", AlertTag)
        AlertTag.click()
    except:
        time.sleep(1)