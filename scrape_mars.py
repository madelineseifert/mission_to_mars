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


    # latest news title
   
    titles = news_soup.find_all('div', class_='content_title')
    news_title = titles[0].text
    print(news_title)
   

    # latest news paragraph
    paragraphs = news_soup.find_all('div', class_="rollover_description_inner")
    news_p = paragraphs[0].text
    print(news_p)
    

    
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p


    ## Mars Featured Image

    # URL of mars image
    url_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_images)
    

    time.sleep(5)

  
    full_image_attr = browser.find_by_id('full_image')
    full_image_attr.click()
    time.sleep(2)
    
 
    more_info_attr = browser.find_link_by_partial_text('more info')
    more_info_attr.click()
    time.sleep(2)
    

    html = browser.html
    img_soup = bs(html, 'html.parser')
    


    # find the relative image url  
    rel_img_url = img_soup.find('figure', class_='lede').find('img')['src']
    rel_img_url


    base_link = 'https://www.jpl.nasa.gov'
    featured_image_url = base_link + rel_img_url
    featured_image_url
    

    
    mars_data['featured_image_url'] = featured_image_url
   


    # Mars Weather

    url_twitter = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url_twitter)
    soup = bs(response.text, 'html.parser')

    result = soup.find('div', class_="js-tweet-text-container")
   
    

    weather = result.p.text
    print(weather)
    

    mars_data['mars_weather'] = weather
    


    # Mars Facts

    url_facts = "http://space-facts.com/mars/"

    facts = pd.read_html(url_facts)[0]

    facts.columns=['Description', 'Value']
    facts.reset_index(drop = True, inplace=True)
   


    mars_facts_html = facts.to_html()
    mars_facts_html = mars_facts_html.replace('\n', '')

    mars_data['mars_facts'] = mars_facts_html
   


    ## Mars Hemispheres

     
    url_USGS = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

   

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
   


    hemisphere_image_urls = []

    for x in url_list:
        url = url_base + x
        
        browser.visit(url)
    
        
        time.sleep(5)
    
        soup = bs(browser.html, 'html.parser')
    
        result_image = soup.find('img', class_="wide-image")
        image = url_base + result_image["src"]
    
       
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

