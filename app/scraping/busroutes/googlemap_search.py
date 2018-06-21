# REF Python seleniumの基本 https://torina.top/detail/264/

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
df_from_to = df_from_to

# define empty dataframe
returned_dataset = pd.DataFrame(columns=['ObjectID', "Route1", "Route2", "Route3"], index=[])

count = 1
for from_to_list in df_from_to.iterrows():
    index, data = from_to_list

    # 出発地点・目的地・時刻を指定
    START_POINT = data.乗車場所バス停.split()[0].replace("'", "").replace(",", "")
    END_POINT = data.降車場所バス停.split()[0].replace("'", "").replace(",", "")
    START_TIME = data.出発時間

    SEARCH = START_POINT + " から " + END_POINT + " まで "
    FILENAME = "output/bus_routes_ss/" + START_POINT + "_" + END_POINT + "_" + START_TIME.replace("/","_") + ".png"
    TIMEOUT = 5

    driver = None

    print(count , ": Checking now ... 【出発点:" + START_POINT, "】 【降車点:" + END_POINT, "】 【出発時間:" + START_TIME + "】---------------")

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

            # 出発時刻を選択する箇所を取得
            start_time_input = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/span[1]/input')
             # 入力されているものを削除する
            length = len(start_time_input.get_attribute('value'))
            start_time_input.send_keys(length * Keys.BACKSPACE)
            # 出発時刻を取得する
            start_time_input.send_keys(START_TIME)
            start_time_input.send_keys(Keys.ENTER)

            try:
                # リストが出てくるまで待機する
                element = WebDriverWait(driver,10).until(
                    # 遷移先で指定した要素がでてくるか確認
                    EC.presence_of_element_located((By.ID, 'section-directions-trip-0'))
                )
            except TimeoutException:
                pass

            # 検索ルートを取得してリストに加える
            list_route = driver.find_elements_by_class_name('section-directions-trip-description')

            route_list = []
            for ls in list_route:
                route_list.append(ls.text.replace("\n", " "))
                print("Routes is found ... ")

            # get screen shot
            driver.save_screenshot(FILENAME)
            print("Bus route is found.\nscreenshot is saved.")

        except NoSuchElementException:
            driver.save_screenshot(FILENAME)
            print("Screenshot is saved.\n")
            print("There are no bus route.")

            # ルートのリスト空白を代入
            route_list.append("")
            route_list.append("")
            route_list.append("")

        print("adjusting list size")
        if len(route_list) <= 3:
            while len(route_list) != 3:
                route_list.append("")
        new_contents = pd.Series([data.ObjectID, route_list[0], route_list[1], route_list[2]],
                                 index=returned_dataset.columns,
                                 name = None)


        returned_dataset = returned_dataset.append(new_contents, ignore_index=True)
        print("data is appended.")
        count += 1

    finally:
        # returned_dataset.to_csv("output/bus_routes.csv")
        returned_dataset.to_excel("output/bus_routes.xlsx")

        # quit
        if driver is not None:
            driver.quit()
