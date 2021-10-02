import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import undetected_chromedriver as uc
import time

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
driver = uc.Chrome(options=options)

def loginReuters(url):
    driver.get(url)
    email = driver.find_element_by_xpath("//input[@name='email']")
    password = driver.find_element_by_xpath("//input[@name='password']")
    loginButton = driver.find_element_by_xpath("//button[@class='Button__button___3FFWBE Button__primary___1PWXOG Button__round___1BK77J']")
    acceptCookies = driver.find_element_by_xpath("//button[@id='accept-recommended-btn-handler']")

    email.send_keys("bernardo_brg@hotmail.com")
    password.send_keys("Al1715@l")
    acceptCookies.click()
    loginButton.click()


def parseArticles(urls):
    text = ""
    for n in urls:
        driver.get(n)
        soup = bs(driver.page_source, 'html.parser')
        article = soup.find("div",{"class":"Article__container___7jklW_"})

        image = article.find("div",{"data-testid":"primary-image"}).find("img")["srcset"]
        title = article.find("div",{"class":"ArticleHeader__container___3rO4Ad"}).find("h1",{"class":"Text__text___3eVx1j Text__dark-grey___AS2I_p Text__medium___1ocDap Text__heading_2___sUlNJP Heading__base___1dDlXY Heading__heading_2___3f_bIW"})
        body = article.find("div",{"class":"ArticleBody__content___2gQno2 paywall-article"})
        print(body)
            

def getArticlesUrls():
    urls = []
    offset = 1700
    driver.get("https://www.reuters.com/site-search/?query=Afghanistan&offset=" + str(offset))
    soup = bs(driver.page_source, 'html.parser')
    while not soup.find_all("div", {"class":"SearchResults__empty___39dP61"}):
        print(soup.find_all("div", {"class":"SearchResults__empty___39dP61"}))

        articles = soup.find("ul", {"class": "SearchResults__list___1Dcpcj"}).find_all("li", {
            "class": "SearchResults__item___3jzYEE"})
        for article in articles:
            urls.append("https://www.reuters.com/" + article.find("a")["href"])
        offset += 10
        driver.get("https://www.reuters.com/site-search/?query=Afghanistan&offset=" + str(offset))
        time.sleep(1)
        soup = bs(driver.page_source, 'html.parser')
    return urls

def wpLogin():
    driver.get(
        "https://www.washingtonpost.com/search?query=afghanistan&btn-search=&facets=%7B%22time%22%3A%22all%22%2C%22sort%22%3A%22relevancy%22%2C%22section%22%3A%5B%22Politics%22%5D%2C%22author%22%3A%5B%5D%7D")
    signIn = driver.find_element_by_xpath("//a[@id='sign-in']")
    signIn.click()
    time.sleep(2)
    username = driver.find_element_by_xpath("//input[@id='username']")
    username.send_keys("bernardo_brg@hotmail.com")
    nextButton = driver.find_element_by_xpath("//button[@type='submit']")
    nextButton.click()
    time.sleep(2)
    password = driver.find_element_by_xpath("//input[@id='password']")
    password.send_keys("Al1715@l")
    signInButton = driver.find_element_by_xpath("//button[@type='submit']")
    signInButton.click()
    time.sleep(2)

def scrapWPArticles():
    urls = []
    driver.get("https://www.washingtonpost.com/search?query=afghanistan&btn-search=&facets=%7B%22time%22%3A%22all%22%2C%22sort%22%3A%22relevancy%22%2C%22section%22%3A%5B%22Politics%22%5D%2C%22author%22%3A%5B%5D%7D")
    soup = bs(driver.page_source)
    found = soup.find_all("button",{"class":"inline-flex items-center justify-center lh-md overflow-hidden border-box min-w-btn transition-colors duration-200 ease-in-out font-sans-serif font-bold antialiased bg-offblack hover-bg-gray-darker focus-bg-gray-darker white b-solid bw bc-transparent focus-bc-black mt-md mb-md brad-lg pl-md pr-md h-md pt-0 pb-0 w-100 pointer"})
    while found:
        print(found)
        loadMore = driver.find_element_by_xpath("//button[@class='inline-flex items-center justify-center lh-md overflow-hidden border-box min-w-btn transition-colors duration-200 ease-in-out font-sans-serif font-bold antialiased bg-offblack hover-bg-gray-darker focus-bg-gray-darker white b-solid bw bc-transparent focus-bc-black mt-md mb-md brad-lg pl-md pr-md h-md pt-0 pb-0 w-100 pointer']")
        driver.execute_script("arguments[0].scrollIntoView();", loadMore)
        loadMore.click()
        time.sleep(2)
        soup = bs(driver.page_source)
        found = soup.find_all("button", {
            "class": "inline-flex items-center justify-center lh-md overflow-hidden border-box min-w-btn transition-colors duration-200 ease-in-out font-sans-serif font-bold antialiased bg-offblack hover-bg-gray-darker focus-bg-gray-darker white b-solid bw bc-transparent focus-bc-black mt-md mb-md brad-lg pl-md pr-md h-md pt-0 pb-0 w-100 pointer"})

    soup = bs(driver.page_source)
    articles =soup.find("div", {"class":"search-app-container mr-auto ml-auto flex flex-column col-8-lg"}).find_all("article")
    for article in articles:
        urls.append(article.find("a")["href"])
    return urls

def parseWPArticles(articles):

    articleContent = ""

    for article in articles:
        driver.get(article)
        time.sleep(2)
        soup = bs(driver.page_source)
        title = soup.find("span",{"data-qa":"headline-text"})
        author = soup.find("a",{"data-qa":"autor-name"})
        body = soup.find("div",{"class":"article-body"}).find_all("p")
        for paragraph in body:
            articleContent = paragraph.content[0] + "\n"
        print(articleContent)


def scrapReuters():
    loginReuters("https://www.reuters.com/signin/?redirect=https%3A%2F%2Fwww.reuters.com%2F%23")
    articles = getArticlesUrls()
    parseArticles(articles)

def scrapWP():
    wpLogin()
    urls = scrapWPArticles()
    parseWPArticles(urls)

def main():

    scrapWP()







# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
