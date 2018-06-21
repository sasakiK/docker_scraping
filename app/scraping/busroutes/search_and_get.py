#!/usr/bin/
# -*- coding: utf-8 -*-

import re
import time
import pandas as pd
# from selenium import webdriver
import selenium.webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


start_point = '常総市坂手町１０００－２'
end_point = '常総市内守谷町きぬの里１丁目５－６'

kw = start_point + " から " + end_point + " まで "

# iMPUCMhC5_G0-YuZOcjA1ZzM
# i9OQSA43qHmw-YuZOcjA1ZzM

url = 'https://www.google.co.jp/'

webdriver = selenium.webdriver
chop = webdriver.ChromeOptions()
chop.add_argument('--disable-gpu')
chop.add_argument('--no-sandbox')
driver = webdriver.Remote(command_executor='http://selenium:4444/wd/hub',
                          desired_capabilities=DesiredCapabilities.CHROME.copy())
driver.implicitly_wait(15)

driver.get(url)
print(driver.current_url)
time.sleep(5)

print('KW : ' + kw)
xpath = '//*[@id="lst-ib"]'
search = driver.find_element_by_xpath(xpath)
search.send_keys(kw)
time.sleep(5)

xpath = '//*[@id="sbtc"]/div[2]/div[2]/div[1]/div/ul/li[9]/div/span[1]/span/input'
button = driver.find_element_by_xpath(xpath)
button.click()
time.sleep(5)

xpath = '//*[@id="rso"]/div[1]/div/div[1]/div/div/h3/a'
first_url = driver.find_element_by_xpath(xpath)
print(first_url.get_attribute('href'))

driver.quit()
