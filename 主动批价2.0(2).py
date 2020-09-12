# coding: utf8
import time
import pandas as pd
import numpy as np
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from openpyxl import load_workbook
from selenium.webdriver.common.keys import Keys

# 记录网页、账号
_name = '****'
_psd = '****'
standard_price_url = r'http://ramp.ziroom.com/#/login'
book = load_workbook('未调整明细.xlsx')
writer = pd.ExcelWriter('未调整明细.xlsx', engine='openpyxl')
writer.book = book  #将文件中的信息缓存到变量中，此时原始文件是空的

def go_to_page():
    """
    打开网页、登录并进入调价界面
    """
    driver.get(standard_price_url)
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="app"]/div/div/div/'
                                                                                   'form/div[1]/div/div/input')))
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="app"]/div/div/div/form/div[1]/div/div/input').send_keys(_name)
    driver.find_element_by_xpath('//*[@id="app"]/div/div/div/form/div[2]/div/div/input').send_keys(_psd)
    driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div/button').click()

    xpath0 = '//*[@id="app"]/div/section/aside/div/ul/span[2]/li/div/span'  # 调价管理的xpath
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, xpath0)))
    driver.find_element_by_xpath(xpath0).click()
    time.sleep(0.5)

    xpath1 = '//*[@id="app"]/div/section/aside/div/ul/span[2]/li/ul/span[1]/li/div'  # 调价申请的xpath
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, xpath1)))
    driver.find_element_by_xpath(xpath1).click()
    time.sleep(0.5)

    xpath2 = '//*[@id="app"]/div/section/aside/div/ul/span[2]/li/ul/span[1]/li/ul/span[3]/li/div'  # 出房价调价的xpath
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath2)))
    driver.find_element_by_xpath(xpath2).click()
    time.sleep(0.5)

    xpath3 = '//*[@id="app"]/div/section/aside/div/ul/span[2]/li/ul/span[1]/li/ul/span[3]/li/ul/span[1]/a/li'  # 房源列表的xpath
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath3)))
    driver.find_element_by_xpath(xpath3).click()
    time.sleep(0.5)

    jsxx = '//*[@id="app"]/div/section/section/main/div[2]/div/div/div[1]/div[1]/span'
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, jsxx)))
    print("STEP1:调价界面加载完毕")


def is_exist_from_xpath(xpath):
    """
    60秒时间刷出xpath的信息
    """
    max_attempt = 60
    attempt = 1
    while True:
        try:
            reu = driver.find_element_by_xpath(xpath)
            break
        except:
            time.sleep(1)
            if attempt > max_attempt:
                reu = False
                break
            attempt += 1
    return reu


def chrome():
    """打开新的调价界面，关闭旧界面"""
    js = 'window.open("http://ramp.ziroom.com/#/pricemanagement/priceapplication/outprice/outpricehouses")'
    driver.execute_script(js)  # 打开新的标签页
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0])  # 切换到死机界面
    driver.close()  # 关闭死机界面
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0])  # 打开新界面驱动

# 正式开始工作
driver = webdriver.Chrome(r'C:\Program Files\chromeDriver\chromedriver.exe')  # 打开浏览器
driver.maximize_window()  # 最大化窗口
go_to_page()  # 打开网页、登录并进入调价界面

house_list = pd.read_excel(r'房源列表.xlsx')
dict = house_list.to_dict(orient='index')
print('STEP2:确认调价数量：' + str(len(dict)) + '\n')

return_message = pd.DataFrame(columns=['房源编号','房间编号','修正价格'])

i = 0
for i in range(len(dict)):
    house_code = dict[i]['房源编号']
    xiuzheng_price = dict[i]['修正价格']
    room_code = dict[i]['房间编号']
    log = {'房源编号': house_code, '房间编号': room_code, '修正价格': xiuzheng_price}
    current_time = time.time()

    print('正在调整第' + str(i + 1) + '个，' + '调整房源信息如下：')
    if room_code == '整租':
        pass
    elif room_code is np.nan:
        print('友家房源' + str(house_code) + '没写房间号，调整下一个\n')
        return_message = return_message.append(log, ignore_index=True)
        continue
    elif '0' in str(room_code):  # 有0就是str，没0就是int
        room_code = re.sub('[0]', '', str(room_code))
        room_code = int(room_code)
    print('房源编号：' + str(house_code) + '  ' + '房间编号：' + str(room_code) + '  ' + '修正价格：' + str(xiuzheng_price))

    house_code_input_xpath = '//*[@id="app"]/div/section/section/main/div[2]/div' \
                             '/div/div[2]/div/form/div/div[4]/div/div/div/input'  # 房源编号输入框
    if is_exist_from_xpath(house_code_input_xpath):
        print('[房源编号输入框]加载完毕')
        time.sleep(1)
    else:
        print('一分钟没加载出来[房源编号输入框],放弃，批下一个\n')
        return_message = return_message.append(log, ignore_index=True)
        chrome()
        continue
    time.sleep(0.5)
    driver.find_element_by_xpath(house_code_input_xpath).clear()  # 清空文本框
    time.sleep(0.5)
    driver.find_element_by_xpath(house_code_input_xpath).send_keys(house_code)
    driver.find_element_by_xpath('//*[@id="app"]/div/section/section/main/div[2]/div'
                                 '/div/div[2]/div/form/div/div[6]/div/div/button[1]').click()  # 查询按钮

    fangzu = 0
    button_target = ''
    xpath_list_one = './/*[@id="app"]/div/section/section/main/div[2]/div/div/div[3]/div[2]/div[1]/div[3]/table/tbody/tr[1]/td[1]/div'  # 第一个调价信息
    xpath_area = '//*[@id="app"]/div/section/section/main/div[2]/div/div/div[3]/div[2]/div[1]/div[3]/table/tbody'  # 房源列表块
    if is_exist_from_xpath(xpath_list_one):
        print('[房源列表]加载完毕')
        elements = driver.find_element_by_xpath(xpath_area)
        rows = elements.find_elements_by_tag_name('tr')  # 房源列表块中的行
        print('房源列表行数：' + str(len(rows)))
        room_code_list = driver.find_elements_by_xpath('//*[@id="app"]/div/section/section/main/div[2]/div'
                                                  '/div/div[3]/div[2]/div[1]/div[3]/table/tbody/tr/td[7]')  # 房间号列
        if room_code == '整租':
            button_target = driver.find_element_by_xpath('//*[@id="app"]/div/section/section/main/div[2]'
                                                         '/div/div/div[3]/div[2]/div[1]/div[3]/table/tbody'
                                                         '/tr/td[11]/div/a')  # 调价按钮
            fangzu = driver.find_element_by_xpath('//*[@id="app"]/div/section/section/main'
                                                  '/div[2]/div/div/div[3]/div[2]/div[1]'
                                                  '/div[3]/table/tbody/tr/td[9]/div').text.replace(',', '')  # 房租信息
            time.sleep(1)
            time.sleep(1)
        else:
            for j in range(len(rows)):
                room_code_target = int(driver.find_elements_by_xpath('//*[@id="app"]/div/section/section/main/div[2]'
                                                                     '/div/div/div[3]/div[2]/div[1]/div[3]/table/tbody'
                                                                     '/tr/td[7]/div')[j].text)
                print('正在匹配第' + str(j+1) +'条，房间号[' + str(room_code_target) + ']...  -> ', end='')

                if room_code_target == room_code:
                    print('匹配成功')
                    button_target = driver.find_element_by_xpath('//*[@id="app"]/div/section/section/main'
                                                                 '/div[2]/div/div/div[3]/div[2]/div[1]/div[3]'
                                                                 '/table/tbody/tr[' + str(j+1) + ']/td[11]/div/a')  #调价按钮
                    fangzu = driver.find_element_by_xpath('//*[@id="app"]/div/section/section/main/div[2]'
                                                          '/div/div/div[3]/div[2]/div[1]/div[3]/table/tbody'
                                                          '/tr[' + str(j+1) + ']/td[9]/div').text.replace(',','')  # 房租信息
                    time.sleep(1)
                    break
                else:
                    print('匹配失败')
                j += 1
    else:
        print('一分钟没加载出来[房源列表],放弃，批下一个\n')
        return_message = return_message.append(log, ignore_index=True)
        chrome()
        continue

    if int(fangzu) == xiuzheng_price:
        print('现在房源已经是期望价格，不再调整\n')
        chrome()
        continue
    else:
        button_target.click()

    house_code_inside_xpath = '//*[@id="app"]/div/section/section/main/div[2]/div/section/div[1]' \
                              '/div/section[1]/div[2]/div[1]/span[2]/span/span'  # 调价界面房源编号
    if is_exist_from_xpath(house_code_inside_xpath):
        print('[调价界面房源编号]加载完毕')
    else:
        print('一分钟没加载出来[调价界面房源编号],放弃，批下一个\n')
        return_message = return_message.append(log, ignore_index=True)
        chrome()
        continue
    house_code_inside = driver.find_element_by_xpath(house_code_inside_xpath).text
    assert house_code_inside == house_code, '房源编号不匹配'
    if room_code != '整租':
        room_code_inside_xpath = '//*[@id="app"]/div/section/section/main/div[2]/div/section/div[1]' \
                                 '/div/section[1]/div[3]/div[1]/span[2]'  # 调价界面房间号
        room_code_inside = int(driver.find_element_by_xpath(room_code_inside_xpath).text)
        assert room_code_inside == room_code, '房间号不匹配'

    xpath_button = '//*[@id="app"]/div/section/section/main/div[2]/div/section/div[@class="main-footer"]/button'  # 调整按钮
    if is_exist_from_xpath(xpath_button):
        print('[调整按钮]加载完毕')
    else:
        print('一分钟没加载出来[调整按钮],放弃，批下一个\n')
        return_message = return_message.append(log, ignore_index=True)
        chrome()
        continue
    driver.find_element_by_xpath(xpath_button).click()

    xpath_window = '//*[@id="app"]/div/section/section/main/div[2]/div/section/div[5]/div/div[1]/span'  # 浮窗
    price_input_box = '//*[@id="app"]/div/section/section/main/div[2]/div/section/div[5]/div' \
                      '/div[2]/div[1]/div[2]/div[2]/div/input'  # 价格输入框
    if is_exist_from_xpath(xpath_window):
        print('[价格输入框]加载完毕')
    else:
        print('一分钟没加载出来[价格输入框],放弃，批下一个\n')
        return_message = return_message.append(log, ignore_index=True)
        chrome()
        continue
    driver.find_element_by_xpath(price_input_box).send_keys(xiuzheng_price)

    reason_text_area = '//*[@id="app"]/div/section/section/main/div[2]/div/section/div[5]/div' \
                       '/div[2]/div[2]/div/textarea'  #调价原因输入框
    reason = '根据区域市场情况校正待租价格。。。。'
    if is_exist_from_xpath(reason_text_area):
        print('[调价原因输入框]加载完毕')
    else:
        print('一分钟没加载出来[调价原因输入框],放弃，批下一个\n')
        return_message = return_message.append(log, ignore_index=True)
        chrome()
        continue
    driver.find_element_by_xpath(reason_text_area).send_keys(reason)
    time.sleep(0.5)
    confirm_button = '//*[@id="app"]/div/section/section/main/div[2]/div/section/div[5]/div' \
                     '/div[2]/div[1]/div[2]/div[2]/button'  # 确认按钮
    driver.find_element_by_xpath(confirm_button).click()
    time.sleep(0.5)
    tijiao_button = '//*[@id="app"]/div/section/section/main/div[2]/div/section/div[5]/div' \
                    '/div[3]/div/button[2]'  # 提交按钮
    WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH, tijiao_button)))
    driver.find_element_by_xpath(tijiao_button).click()

    if is_exist_from_xpath(house_code_input_xpath):
        print('第' + str(i+1) + '个调整完毕')
        print('单个调价耗时：' + str(time.time() - current_time) + '\n\n')

    i += 1
return_message.to_excel(writer)
writer.save()

print('*' * 200 + '\n' + '*' * 200 + '\n' + '*' * 200)
print('全部调整完毕')
print('*' * 200 + '\n' + '*' * 200 + '\n' + '*' * 200)
driver.delete_all_cookies()  # 防止爬虫的运行时间太长，页面崩溃
driver.quit()
