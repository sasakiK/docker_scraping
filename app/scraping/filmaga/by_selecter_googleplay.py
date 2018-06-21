from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

if __name__ == '__main__':
    driver = webdriver.Remote(command_executor='http://selenium:4444/wd/hub',
                              desired_capabilities=DesiredCapabilities.CHROME.copy())
    try:
        driver.get('https://play.google.com/store/apps/details?id=in.tsumiki.filmarks&showAllReviews=true')
        # reviews = driver.find_elements_by_class_name('UD7Dzf')
        # for rev in reviews.head(10):
        #     print(rev.text)
        title = driver.find_element_by_css_selector('body[jscontroller="LVJlx"]').text

        print(title)
    finally:
        driver.quit()
