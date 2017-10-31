from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def driver_se(url):
    driver = webdriver.Chrome()
    driver.get(str(url))
    driver.delete_all_cookies()
    c2 ={'PHPSESSID':'acbqhgcbrbkg5lrn1qii86qpk1'}
    driver.add_cookie(c2)

    time.sleep(8)
    element = driver.find_element_by_id("nc_1_n1z")
    ActionChains(driver).click_and_hold(on_element=element).perform()
    ActionChains(driver).move_by_offset(xoffset=260, yoffset=260).perform()
    time.sleep(1)
    driver.find_element_by_id("verify").click()
    time.sleep(1)
    driver.close()


driver_se('http://www.qichacha.com/index_verify?type=companysearch&back=/search?key=%E4%B8%8A%E6%B5%B7%E7%BF%BC%E5%8B%8B')

