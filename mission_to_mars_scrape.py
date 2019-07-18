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
    except: AttributeError:
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