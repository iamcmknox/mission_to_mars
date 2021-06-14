import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    
    ## Mars Exploration Program Scrape
    # Import url and parse the html
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    # latest news title and paragraph text
    newsTitle = soup.find('div', class_='content_title').text
    pText = soup.find('div', class_='image_and_description_container').text


    ## JPL Scrape
    # splinter: find the image url for the current Featured Mars Image - `featured_image_url`.
    executable_path = {'executable_path': "~/usr/local/bin/chromedriver.exec"}
    browser = Browser('chrome', executable_path, headless=False)

    # open the url and parse
    url2 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space'
    browser.visit(url2 + '/index.html')
    html = browser.html
    soup = bs(html, 'html.parser')

    # Scrape the featured image location
    header = soup.find_all('div', class_='header')
    for item in header: 
        featuredImg = item.find('img',class_='headerimage fade-in')['src']
        
    # Get the full image url 
    featuredImgUrl = url + '/' + featuredImg

    # Quit browser 
    browser.quit()


    ## Mars Facts Scrape
    # Scrape the facts table
    url3 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url3)

    # Convert to dataframe 
    facts_df = pd.DataFrame(tables[0])

    # Convert to HTML table string
    facts_html = facts_df.to_html(header=None, index=False)


    ## Mars Hemispheres Scrape
    # Open url and parse
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url4)
    soup = bs(response.text, 'html.parser')

    # Navigate to item section 
    links = soup.find_all('a', class_='itemLink product-item')

    # Create empty list of links 
    linkList = []

    # Loop through link section and get image info links 
    for link in links:
        imgLink = link['href']
        
        # Add image info to list 
        linkList.append(imgLink)

    # Generate full links to image info pages 
    base_url = 'https://astrogeology.usgs.gov'

    # Empty list for full links 
    fullLinks = []

    # Loop through link list and generate full link
    for link in linkList:
        fullLink = base_url + link
        fullLinks.append(fullLink)

    # Empty lists for full-size image links and titles
    imgLinks = []
    titles = []

    # Loop through each link and scrape title and links to the full size image
    for link in fullLinks:
        response = requests.get(link)
        soup = bs(response.text, 'html.parser')
        
        # Navigate to title 
        title = soup.find('h2', class_='title').text
        titles.append(title)
        
        # Navigate to image link location
        imgLink = soup.find('img', class_='wide-image')
        imgLink = imgLink['src']
        imgLinks.append(imgLink)

        # Create list of dictionaries for each image
        keys = ['title', 'img_url']
        zipList= list(zip(titles, imgLinks))
        hemispheres = [{k:v for k,v in zip(keys, z)} for z in zipList]

    # Generate full url link
    fullImgLinks = []
    for link in imgLinks:
        fullLink = base_url + link
        fullImgLinks.append(fullLink)

    # Create list of dictionaries for each image
    keys = ['title', 'img_url']
    zipList= list(zip(titles, fullImgLinks))
    hemispheres = [{k:v for k,v in zip(keys, z)} for z in zipList]

    # Compile into a dictionary
    mars_dict = {
        'news_title': newsTitle,
        'news_text': pText,
        'featured_img': featuredImgUrl,
        'mars_facts': facts_html,
        'hemisphere_imgs': hemispheres
    }

    return mars_dict
