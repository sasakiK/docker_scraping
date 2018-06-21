import re
import sys
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException


################################################################################

df_from_to = pd.read_csv("data/bus_routes/from_to_all.csv")

# define empty dataframe
returned_dataset = pd.DataFrame(columns=['ObjectID', "バスルート1"], index=[])


for from_to_list in df_from_to.iterrows():
    index, data = from_to_list

    # 出発地点・目的地・時刻を指定
    START_POINT = data.乗車場所バス停.split()[0].replace("'", "").replace(",", "")
    END_POINT = data.降車場所バス停.split()[0].replace("'", "").replace(",", "")
    START_TIME = data.出発時間

    SEARCH = START_POINT + " から " + END_POINT + " まで "
    FILENAME = "output/bus_routes_ss/" + START_POINT + "_" + END_POINT + "_" + START_TIME + ".png"
    TIMEOUT = 5

    driver = None

    print("Checking now ... 【出発点:" + START_POINT, "】 【降車点:" + END_POINT, "】 【出発時間:" + START_TIME + "】---------------")

    try:
        ############################################################################
        driver = webdriver.Remote(command_executor='http://selenium:4444/wd/hub',
                                  desired_capabilities=DesiredCapabilities.CHROME.copy())
        # driver.set_window_size(1200, 800)

        ############################################################################
        # 1) search
        driver.get("https://www.google.co.jp/maps")
        driver.implicitly_wait(TIMEOUT)
        # 검색 엘리먼트를 찾아 검색어를 입력하고
        elem = driver.find_element_by_id("searchboxinput")
        elem.send_keys(SEARCH)
        # 検索ボタンを押す
        elem = driver.find_element_by_id("searchbox-searchbutton")
        elem.click()

        driver.implicitly_wait(TIMEOUT)

        try:

            # click 「公共交通機関」モードで経路を表示する
            driver.find_element_by_xpath('//*[@id="omnibox-directions"]/div/div[2]/div/div/div[1]/div[3]/button').click()
            driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/span/div/div/div/div[2]').click()

            # 出発時刻を指定
            dropdown = WebDriverWait(driver,10).until(
                    # 遷移先で指定した要素がでてくるか確認
                    EC.presence_of_element_located((By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]'))
                )

            # 「出発時刻」のドロップボックスを選択する
            select = driver.find_elements_by_class_name('goog-menu-vertical')

            for sel in select:
                if sel.text != "出発時刻":
                    sel.click()
                    print("出発時刻 is clicked.")
            # select by visible text

            # 出発時刻を選択する箇所を取得
            start_time_input = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/span[1]/input')
             # 入力されているものを削除する
            length = len(start_time_input.get_attribute('value'))
            start_time_input.send_keys(length * Keys.BACKSPACE)
            # 出発時刻を取得する
            start_time_input.send_keys("9:00")
            start_time_input.send_keys(Keys.ENTER)

            try:
                # リストが出てくるまで待機する
                element = WebDriverWait(driver,10).until(
                    # 遷移先で指定した要素がでてくるか確認
                    EC.presence_of_element_located((By.ID, 'section-directions-trip-0'))
                )
            except TimeoutException:
                pass


            # 詳細をクリックする
            driver.find_element_by_xpath('//*[@id="section-directions-trip-0"]/div[2]/div[2]/div[4]/button').click()

            # リストが出てくるまで待機する
            element = WebDriverWait(driver,10).until(
                    # 遷移先で指定した要素がでてくるか確認
                    EC.presence_of_element_located((By.CLASS_NAME, 'section-trip-details'))
                )
            # 検索ルートの一つ目
            list1 = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[5]')

            routes_1 = list1.get_attribute("text")

            # get screen shot
            driver.save_screenshot(FILENAME)

            print("Bus route is found. screenshot is saved.")

        except NoSuchElementException:
            print("There are no bus route.")
            # ルートがないので空白を代入
            routes_1 = ""

            pass

        new_contents = pd.Series([data.ObjectID, routes_1],
                                 index=returned_dataset.columns,
                                 name = None)

        returned_dataset = returned_dataset.append(new_contents, ignore_index=True)

    finally:
        returned_dataset.to_csv("output/bus_routes.csv")
        ############################################################################
        # quit
        if driver is not None:
            driver.quit()
