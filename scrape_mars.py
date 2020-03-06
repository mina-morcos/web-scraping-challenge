# Scrape Mars data, return one library to collect scrape data
# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import time

# Define function
def scrape():
    # Library to hold Mars data
    mars_library = {}	
    # Chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
	
    # NASA MARS NEWS
	
    # scrape latest News Title/Paragragh text
    url1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url1)
    # Assign html content
    html = browser.html
    # BeautifulSoup object
    soup1 = bs(html, "html5lib")
    # Extract text from class="content_title" and cleanup
    news_title = soup1.find_all('div', class_='content_title')[0].find('a').text.strip()
    # Extract paragraph from class="rollover_description_inner" and cleanup
    news_p = soup1.find_all('div', class_='rollover_description_inner')[0].text.strip()
    # Put in library
    mars_library['news_title'] = news_title
    mars_library['news_p'] = news_p

    #  JPL MARS SPACE IMAGE FEATURED IMAGE
	
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    # Assign html content
    html = browser.html
    # Beautiful Soup
    soup2 = bs(html, "html5lib")
    #Scrape path for feature image url
    partial_address = soup2.find_all('a', class_='fancybox')[0].get('data-fancybox-href').strip()
    # Combine root url for full address
    featured_image_url = "https://www.jpl.nasa.gov"+partial_address
    # Put in library
    mars_library['featured_image_url'] = featured_image_url

    # MARS WEATHER
	
    # Splinter to scrape latest weather tweet from twitter account
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    # assign html content
    html = browser.html
    # beautifl soup
    soup3 = bs(html, "html5lib")
    # Scrape latest weather tweet
    mars_weather = soup3.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text
    # Put in library
    mars_library['mars_weather'] = mars_weather

    # MARS FACTS
	
    # Pandas to scrape table from facts webpage, convert data to a html table string
    url4 = 'https://space-facts.com/mars/'
    # use Pandas to get the url table
    tables = pd.read_html(url4)
    # Convert list of table into pandas DF
    df = tables[0]
    # update column name
    df.columns=['description','value']
    #Set index to description column
    df.set_index('description', inplace=True)
    # Pandas to generate html tables from DF, save as html
    mars_facts=df.to_html(justify='left')
    # Put in library
    mars_library['mars_facts'] = mars_facts

    # MARS HEMISPHERE
	
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    # assign html content
    html = browser.html
    # Beautiful soup
    soup5 = bs(html,"html5lib")
    # Assigne list to store
    hemisphere_image_urls = []
    # create empty dict
    dict = {}
    # Get all title
    results = soup5.find_all('h3')
    # Loop through results
    for result in results:
        # Get text from result
        itema = result.text
        time.sleep(1)    
        browser.click_link_by_partial_text(itema)
        time.sleep(1)
        # Assign html content
        htmla = browser.html
        # Beautiful Soup
        soupa = bs(htmla,"html5lib")
        time.sleep(1)
        # Image link
        linka = soupa.find_all('div', class_="downloads")[0].find_all('a')[0].get("href")
        # Pass title to dict
        time.sleep(1)
        dict["title"]=itema
        # Pass url to dict
        dict["img_url"]=linka
        # Append dict to list 
        hemisphere_image_urls.append(dict)
        # Cleanup
        dict = {}
        browser.click_link_by_partial_text('Back')
        time.sleep(1)
    # Put into library
    mars_library['hemisphere_image_urls']=hemisphere_image_urls
    # Return library
    return mars_library