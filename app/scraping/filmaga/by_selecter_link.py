import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

def check_rel(input_text):
    m = re.search("articles/([0-9]{1,4})", input_text)
    return m.group(0)


if __name__ == '__main__':

    driver = webdriver.Remote(command_executor='http://selenium:4444/wd/hub',
                              desired_capabilities=DesiredCapabilities.CHROME.copy())
    # define empt994at995ame
    article_contents = pd.DataFrame(columns=["title", "awasete", "link1", "link2", "link3", "link4", "link5", "link6", "link7"], index=[])

    try:
        for article_num in range(1,2020):
        # for article_num in range(199,200):
            # 404 Not Foundでなければ
            try:
                # get page contents
                driver.get('https://filmaga.filmarks.com/articles/ ' + str(article_num))
                print(str(article_num) + "--------------------------")
                title = driver.find_element_by_xpath('//*[@id="js-container"]/div/div[4]/div[1]/article/header/h1')
                contents = driver.find_element_by_xpath('//*[@id="js-container"]/div/div[4]/div[1]/article')


                if ((re.search("【あわせて読みたい】", contents.text) or (re.search("あわせて読みたい", contents.text))) and re.search("※", contents.text)):
                    contain = 1
                    elems = driver.find_elements_by_xpath("//a[@href]")

                    # for elem in elems:
                    link_list = []
                    for elem in elems:
                        link = elem.get_attribute("href")
                        if re.search("articles/([0-9]{1,4})", link):
                            if "/%" not in link:
                                link_extracted = check_rel(link)
                                link_list.append(link_extracted)
                                print("'合わせて読みたい' and link is found : {}".format(link_extracted))
                        # add link
                        try:
                            link1 = link_list[0]
                        except IndexError:
                            link1 = ""
                        try:
                            link2 = link_list[1]
                        except IndexError:
                            link2 = ""
                        try:
                            link3 = link_list[2]
                        except IndexError:
                            link3 = ""
                        try:
                            link4 = link_list[3]
                        except IndexError:
                            link4 = ""
                        try:
                            link5 = link_list[4]
                        except IndexError:
                            link5 = ""
                        try:
                            link6 = link_list[5]
                        except IndexError:
                            link6 = ""
                        try:
                            link7 = link_list[6]
                        except IndexError:
                            link7 = ""
                else:
                    contain = 0
                    print("'合わせて読みたい' is not found.")
                    link1, link2, link3, link4, link5, link6, link7 = "","","","","","",""

                new_contents = pd.Series([title.text, contain, link1, link2, link3, link4, link5, link6, link7],
                                         index=article_contents.columns,
                                         name = 'article/' + str(article_num) )

                # for server capacity
                # time.sleep(0.1)
                article_contents = article_contents.append(new_contents)
            # 404 Not Foundであれば次のiterへ
            except NoSuchElementException:
                pass

        # save as csv file
        article_contents.to_csv("output/filmaga_contents_link.csv")

    finally:
        driver.quit()
