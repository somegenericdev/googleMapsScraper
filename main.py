import time
from datetime import date

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

driver = webdriver.Chrome()


def getAllResults(query):
    url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}/?hl=en"
    driver.get(url)
    try:
        btnAccept=driver.find_element(By.CSS_SELECTOR,"button[aria-label='Accept all']")
        btnAccept.click()
    except NoSuchElementException:
        pass

    divSideBar=driver.find_element(By.CSS_SELECTOR,f"div[aria-label='Results for {query}']")

    keepScrolling=True
    while(keepScrolling):
        divSideBar.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        divSideBar.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        html =driver.find_element(By.TAG_NAME, "html").get_attribute('outerHTML')
        if(html.find("You've reached the end of the list.")!=-1):
            keepScrolling=False
    soup= BeautifulSoup(driver.find_element(By.TAG_NAME, "html").get_attribute('outerHTML'))
    articles=soup.select("div[role*=article]>a")
    # urls = driver.execute_script(script)
    return list(map(lambda x: x['href'],articles))

def getWebsite(url):
    driver.get(url)
    try:
        btnAccept=driver.find_element(By.CSS_SELECTOR,"button[aria-label='Accept all']")
        btnAccept.click()
    except NoSuchElementException:
        pass
    websiteElem=None
    try:
        websiteElem=driver.find_element(By.CSS_SELECTOR,f"a[aria-label^=\"Website:\"]")
    except NoSuchElementException:
        pass
    if(websiteElem):
        return websiteElem.text


links=getAllResults("mcdonalds in paris")
websites=list(map(lambda l: getWebsite(l),links))
print(websites)
