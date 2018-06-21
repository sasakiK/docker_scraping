import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

def check_awasete(input_text):
    if ((re.search("【あわせて読みたい】", input_text) or (re.search("あわせて読みたい", input_text))) and re.search("※", input_text)):
        return 1
    else:
        return 0

if __name__ == '__main__':

    driver = webdriver.Remote(command_executor='http://selenium:4444/wd/hub',
                              desired_capabilities=DesiredCapabilities.CHROME.copy())
    # define empty DataFrame
    article_contents = pd.DataFrame(columns=["title", "category", "writer", "contents"], index=[])

    try:
        for article_num in range(1,2020):
            # 404 Not Foundでなければ
            try:
                # get page contents
                driver.get('https://filmaga.filmarks.com/articles/' + str(article_num))

                title = driver.find_element_by_xpath('//*[@id="js-container"]/div/div[4]/div[1]/article/header/h1')
                category = driver.find_element_by_xpath("//header/div[@class='category-data']/span")
                writer = driver.find_element_by_xpath("//header/div[@class='writer']/div[@class='writer-data']/*")
                contents = driver.find_element_by_xpath('//*[@id="js-container"]/div/div[4]/div[1]/article')
                print(title.text)

                new_contents = pd.Series([title.text, category.text, writer.text, contents.text],
                                         index=article_contents.columns,
                                         name = 'article/' + str(article_num) )
                article_contents = article_contents.append(new_contents)
                # for server capacity
                time.sleep(1)
            # 404 Not Foundであれば次のiterへ
            except NoSuchElementException:
                pass
        # remove \n in contents
        article_contents["contents"] = article_contents["contents"].replace("\n", "", regex=True)
        # add dummy
        data["awasete"] = data["contents"].apply(check_awasete)
        # save as csv file
        article_contents.to_csv("output/filmaga_contents_short.csv")

    finally:
        driver.quit()
