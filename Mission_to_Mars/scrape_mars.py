from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import requests
from webdriver_manager.chrome import ChromeDriverManager


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Mars News
    url = "https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find_all('div', class_='list_text')
    news_title = results[0].find('div', class_='content_title').text
    news_p = results[0].find('div', class_='article_teaser_body').text

    # Featured Image
    url = "https://spaceimages-mars.com"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find('img', class_='headerimage fade-in').get("src")
    featured_image_url = url + "/" + results

    # Mars Facts
    url = "https://galaxyfacts-mars.com"
    tables = pd.read_html(url)
    mars_table = tables[0]
    mars_table = mars_table.rename(columns={0: "Description", 1: "Mars", 2: "Earth"})
    mars_table.set_index("Description", inplace = True)
    mars_table_html = mars_table.to_html("mars_table_html.html")

    #Mars Hemispheres
    url = "https://marshemispheres.com/"
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    results = soup.find_all('div', class_='item')

    hemisphere_image_urls = []
    for result in results:
        img_title = result.find("div", class_="description").find("a").find("h3").text
        img_loc = result.find("a", class_ = "itemLink product-item")["href"]
        img_loc_url = url + img_loc
        browser.visit(img_loc_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        img = soup.find("div", class_ = "downloads").find("ul").find("li").find("a")["href"]
        img_url = url + img
        hemisphere_image_urls.append({"title": img_title, "link": img_url})

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_table_html": mars_table_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }




    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data