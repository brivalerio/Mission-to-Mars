# Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 

executable_path = {'executable': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=True)  # headless for opening or not opening browser when run
