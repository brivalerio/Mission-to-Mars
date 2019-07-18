# Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 

executable_path = {'executable': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=True)  # headless for opening or not opening browser when run

def scrape_all():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": feature_image(browser)
    }
    return data

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find('div', class_="content_title")
        news_title = slide_elem.find('div', class_="content_title").text
        news_p = slide_elem.find('div', class_="article_teaser_body").text
    except AttributeError:
        return None, None
        
    return news_title, news_p

def feature_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    more_info_elem = browser.find_link_by_partial_text("more info")
    more_info_elem.click()
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    try:
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    except AttributeError:
        return None
    
    return img_url

def mars_weather(browser):
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    weather_soup = BeautifulSoup(html, "html.parser")
    tweets = weather_soup.find_all('div', class_='js-tweet-text-container')
    for tweet in tweets:
        mars_weather = tweet.find('p').text
    
    return mars_weather

def facts(browser):
    url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(url)
    mars_df = mars_facts[1]
    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)
    mars_html = mars_df.to_html()

    return facts

def hemispheres(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemi_html = browser.html
    hemi_soup = BeautifulSoup(hemi_html, 'html.parser')
    items = hemi_soup.find_all('div', class_='item')
    images = []
    main_url = 'https://astrogeology.usgs.gov'
    for item in items:
        title = item.find('h3').text
        x_url = item.find('a', class_='itemLink product-item')['href']
        browser.visit(main_url+x_url)
        x_url = browser.html
        x_soup = BeautifulSoup(x_url, 'html.parser')
        img_url = main_url + x_soup.find('img', class_="wide-image")['src']      
        images.append({"title":title, "img_url":img_url})

    return images