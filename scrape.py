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
    news_title = soup.find('div', class_='content_title').text
    p_text = soup.find('div', class_='image_and_description_container').text


    ## JPL Scrape
    # splinter: find the image url for the current Featured Mars Image - `featured_image_url`.
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # open the url and parse
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space'
    browser.visit(url + '/index.html')
    html = browser.html
    soup = bs(html, 'html.parser')

    # Scrape the featured image location
    header = soup.find_all('div', class_='header')
    for item in header: 
        featured_img = item.find('img',class_='headerimage fade-in')['src']
        
    # Get the full image url 
    featured_img_url = url + '/' + featured_img

    # Quit browser 
    browser.quit()


    ## Mars Facts Scrape
    # Scrape the facts table
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    # Convert to dataframe 
    facts_df = pd.DataFrame(tables[0])

    # Convert to HTML table string
    facts_html = facts_df.to_html(header=None, index=False)


    ## Mars Hemispheres Scrape
    # Open url and parse
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    # Navigate to item section 
    links = soup.find_all('a', class_='itemLink product-item')

    # Create empty list of links 
    link_list = []

    # Loop through link section and get image info links 
    for link in links:
        img_link = link['href']
        
        # Add image info to list 
        link_list.append(img_link)

    # Generate full links to image info pages 
    base_url = 'https://astrogeology.usgs.gov'

    # Empty list for full links 
    full_links = []

    # Loop through link list and generate full link
    for link in link_list:
        full_link = base_url + link
        full_links.append(full_link)

    # Empty lists for full-size image links and titles
    img_links = []
    titles = []

    # Loop through each link and scrape title and links to the full size image
    for link in full_links:
        response = requests.get(link)
        soup = bs(response.text, 'html.parser')
        
        # Navigate to title 
        title = soup.find('h2', class_='title').text
        titles.append(title)
        
        # Navigate to image link location
        img_link = soup.find('img', class_='wide-image')
        img_link = img_link['src']
        img_links.append(img_link)

        # Create list of dictionaries for each image
        keys = ['title', 'img_url']
        zip_list= list(zip(titles, img_links))
        hemispheres = [{k:v for k,v in zip(keys, z)} for z in zip_list]

    # Generate full url link
    full_img_links = []
    for link in img_links:
        full_link = base_url + link
        full_img_links.append(full_link)

    # Create list of dictionaries for each image
    keys = ['title', 'img_url']
    zip_list= list(zip(titles, full_img_links))
    hemispheres = [{k:v for k,v in zip(keys, z)} for z in zip_list]

    # Compile into a dictionary
    mars_dict = {
        'news_title': news_title,
        'news_text': p_text,
        'featured_img': featured_img_url,
        'mars_facts': facts_html,
        'hemisphere_imgs': hemispheres
    }

    return mars_dict
