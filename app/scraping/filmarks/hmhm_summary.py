
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

# remove unused string
def remove_string(input_text):
    m = re.split("の感想", input_text)
    return(m[0])

# make dummy of spoiler
def check_spoiler(input_text):
    if re.search("このレビューはネタバレを含みます", input_text) is not None:
        return 1
    else:
        return 0

if __name__ == '__main__':

    driver = webdriver.Remote(command_executor='http://selenium:4444/wd/hub',
                              desired_capabilities=DesiredCapabilities.CHROME.copy())
    review_df = pd.DataFrame(columns=["title", "summary"], index=[])


    print("PROCESS IS STARTING ------------------------------------")
    driver.get('https://hm-hm.net/suspense/%E4%BD%95%E8%80%85')

    # titleを取得
    title = driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/div[2]/h2/span').text


    new_review_df = pd.Series([title, remove_string(reviewer.text), date.text, rating.text, spoiler_dummy, review],index=review_df.columns)
    review_df = review_df.append(new_review_df, ignore_index=True)



    print("PROCESS IS DONE ---------------------")


    # finally:
    driver.quit()
    review_df.to_csv("output/hmhm_summary.csv")
