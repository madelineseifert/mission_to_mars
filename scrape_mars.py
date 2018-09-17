# Dependencies
import os
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import time
from splinter import Browser
import pandas as pd


## Mars News 

def init_browser():
    return Browser('chrome', headless = False)

def scrape():
    browser = init_browser()
    mars_data = {}


    # URL of page to be scraped
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)
    time.sleep(2)

    html = browser.html
    news_soup = bs(html, 'html.parser')


    # Latest News Title from NASA Mars News Site
    print("Test 1")
    titles = news_soup.find_all('div', class_='content_title')
    news_title = titles[0].text
    print(news_title)
    print("Test 2")

    # Latest News Paragraph Text from NASA Mars News Site
    paragraphs = news_soup.find_all('div', class_="rollover_description_inner")
    news_p = paragraphs[0].text
    print(news_p)
    print("Test 3")

    #Adding news title and news paragraph to dictionary
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p


    ## Mars Featured Image

    # URL of JPL Mars Space Image to be scraped for featured image
    url_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_images)
    print("Test 5")


    # Browse through the pages 
    time.sleep(5)

    # Find and click the full image button
    full_image_attr = browser.find_by_id('full_image')
    full_image_attr.click()
    time.sleep(2)
    print("Test 6")

    # Find the more info button and click that# Find  
    more_info_attr = browser.find_link_by_partial_text('more info')
    more_info_attr.click()
    time.sleep(2)
    print("Test 7")


    # Using BeautifulSoup create an object and parse with 'html.parser'# Using 
    html = browser.html
    img_soup = bs(html, 'html.parser')
    print("Test 8")


    # find the relative image url  
    rel_img_url = img_soup.find('figure', class_='lede').find('img')['src']
    rel_img_url


    # Use the base url to create an absolute url
    base_link = 'https://www.jpl.nasa.gov'
    featured_image_url = base_link + rel_img_url
    featured_image_url
    print("Test 9")

    #Adding featured image url to dictionary
    mars_data['featured_image_url'] = featured_image_url
    print("Test 10")


    ## Mars Weather

    url_twitter = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url_twitter)
    soup = bs(response.text, 'html.parser')

    result = soup.find('div', class_="js-tweet-text-container")
    print("Test 11")
    

    weather = result.p.text
    print(weather)
    print("Test 12")

    mars_data['mars_weather'] = weather
    print("Test 13")


    ## Mars Facts

    url_facts = "http://space-facts.com/mars/"

    facts = pd.read_html(url_facts)[0]

    facts.columns=['description', 'value']
    facts.index.name = None

    # Convert the dataframe to HTML table string
    mars_facts_html = facts.to_html()
    mars_facts_html = mars_facts_html.replace('\n', '')

    mars_data['mars_facts'] = mars_facts_html
    print("Test 14")


    ## Mars Hemispheres

    # Scraping of USGS  
    url_USGS = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Setting up splinter

    browser.visit(url_USGS)

    html = browser.html
    soup = bs(html, 'html.parser')


    url_base = "https://astrogeology.usgs.gov"
    result = soup.find_all('div', class_="item")

    url_list = []

    for y in result:
        link = y.find('a')['href']
        url_list.append(link)
    
    print(url_list)
    print("Test 15")


    # Create an empty list to hold dictionaries of hemisphere title with the image url string# Create 
    hemisphere_image_urls = []

    for x in url_list:
        url = url_base + x
        
        browser.visit(url)
    
        # Sleep script to ensure the page fully loads
        time.sleep(5)
    
        soup = bs(browser.html, 'html.parser')
    
        # Grab image url
        result_image = soup.find('img', class_="wide-image")
        image = url_base + result_image["src"]
    
        # Grab page title and remove "Enhanced" from string
        result_title = soup.find('h2', class_='title')
        title = result_title.text
        title = title.rsplit(' ', 1)[0]
    
        diction = {"title": title, "image": image}
        hemisphere_image_urls.append(diction)
    
        time.sleep(5)
    
    print(hemisphere_image_urls)
    print("Test 15")

    mars_data["hemispheres"] = hemisphere_image_urls

    return mars_data

