
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
    review_df = pd.DataFrame(columns=["title", "reviewer", "date", "rating", "spoiler", "text"], index=[])

    # for num in range(836):
    for num in range(0,837):
        print("NUM "+str(num)+" IS STARTING ------------------------------------")
        if num == 0:
            driver.get('https://filmarks.com/movies/65933')
        else:
            driver.get('https://filmarks.com/movies/65933?page='+str(num))

        # titleを取得
        title = driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/div[2]/h2/span').text

        # get one by one -----------------------------------------------------------
        # reviewers
        reviewers = driver.find_elements_by_css_selector('h4.c-media__text')
        # dates
        dates = driver.find_elements_by_css_selector('time.c-media__date')
        # ratings
        ratings = driver.find_elements_by_css_selector('div.c-rating__score')

        # spoilers
        cards = driver.find_elements_by_css_selector('div.js-mark-card')
        review_txts = driver.find_elements_by_css_selector('div.p-mark__review')

        spoiler_dummy_list = []
        review_list = []
        count = 0
        for card, review_txt  in zip(cards, review_txts):
            # 'このレビューはネタバレを含みます'があれば
            if check_spoiler(card.text) == 1:
                spoiler_dummy_list.append(1)

                # spoiler = alert_ps[count]
                spoiler = driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[1]/div['+str(1+len(spoiler_dummy_list))+']/p').click()
                time.sleep(1)
                Alert(driver).accept()
                review = driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[1]/div[' + str(1+len(spoiler_dummy_list)) + ']/div[2]')

                review_list.append(review.text)
                count += 1
            else:
                spoiler_dummy_list.append(0)
                review_list.append(review_txt.text)

        # print for
        for date,reviewer,rating,spoiler_dummy,review in zip(dates, reviewers, ratings, spoiler_dummy_list, review_list):
            print("タイトル : {:}, 日付 : {:}, 投稿者 : {:}, レート : {:}, ネタバレ : {:}, レビュー : {:5}".format(title, date.text, remove_string(reviewer.text), rating.text, spoiler_dummy, review[0:10]))
            new_review_df = pd.Series([title, remove_string(reviewer.text), date.text, rating.text, spoiler_dummy, review],index=review_df.columns)
            review_df = review_df.append(new_review_df, ignore_index=True)



        print("DONE ---------------------")


    # finally:
    driver.quit()
    review_df.to_csv("output/filmarks_reviews.csv")
