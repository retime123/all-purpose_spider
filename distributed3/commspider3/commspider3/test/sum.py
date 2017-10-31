from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time


driver = webdriver.Chrome()


driver.get('https://www.qichacha.com/user_login')
time.sleep(8)
# wait = WebDriverWait(driver, 5)
driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div[1]/div[1]').click()

# source = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#nc_2_n1z")))
# target = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#text-blue")))

# action = ActionChains(driver)
# action.drag_and_drop(source, target).perform()


#
# element = self.br.find_element_by_class_name("gt_slider_knob")
# # click_and_hold(on_element=None) ——点击鼠标左键，不松开
# # perform() ——执行链中的所有动作
# # move_to_element(to_element) ——鼠标移动到某个元素
# ActionChains(self.br).move_to_element(to_element=element).perform()
# ActionChains(self.br).click_and_hold(on_element=element).perform()

# 输入账户名
driver.find_element_by_name("nameNormal").send_keys("17365365260")
# 输入密码
driver.find_element_by_name("pwdNormal").send_keys("hgcheng123456789")
element = driver.find_element_by_id("nc_2_n1z")
ActionChains(driver).click_and_hold(on_element=element).perform()
ActionChains(driver).move_by_offset(xoffset=260, yoffset=260).perform()
time.sleep(8)
cookie= driver.get_cookies()
print(cookie)
# driver.close()

'''[{'domain': 'www.qichacha.com', 'httpOnly': True, 'name': 'acw_tc', 'path': '/', 'secure': False, 'value': 'AQAAALn8bS4BAw8ArMittG8o1KULeYfK'}, {'domain': 'www.qichacha.com', 'expiry': 1540531121, 'httpOnly': False, 'name': '_umdata', 'path': '/', 'secure': False, 'value': '85957DF9A4B3B3E88698EDA55671785AB87A64056395F7DDF1DDFFDD68521E29812E1B19B064D83CCD43AD3E795C914CDE81D1064F31644576F46E2225ADBCE2'}, {'domain': 'www.qichacha.com', 'httpOnly': False, 'name': 'PHPSESSID', 'path': '/', 'secure': False, 'value': 'tcv5vgrdiuabm2ocop05hj3ul6'}, {'domain': 'www.qichacha.com', 'expiry': 1824355118, 'httpOnly': False, 'name': '_uab_collina', 'path': '/', 'secure': False, 'value': '150899511852888912646105'}, {'domain': '.qichacha.com', 'expiry': 1540531118, 'httpOnly': False, 'name': 'zg_did', 'path': '/', 'secure': False, 'value': '%7B%22did%22%3A%20%2215f571e35673ba-0350748f5656db-464c0328-144000-15f571e3568431%22%7D'}, {'domain': '.qichacha.com', 'expiry': 1540531118, 'httpOnly': False, 'name': 'zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f', 'path': '/', 'secure': False, 'value': '%7B%22sid%22%3A%201508995118448%2C%22updated%22%3A%201508995118453%2C%22info%22%3A%201508995118451%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%7D'}, {'domain': '.qichacha.com', 'expiry': 1524719918, 'httpOnly': False, 'name': 'UM_distinctid', 'path': '/', 'secure': False, 'value': '15f571e3677429-0a7dc5179fd01d-464c0328-144000-15f571e36783fb'}, {'domain': 'www.qichacha.com', 'expiry': 1524719918, 'httpOnly': False, 'name': 'CNZZDATA1254842228', 'path': '/', 'secure': False, 'value': '630312526-1508992116-%7C1508992116'}]
'''