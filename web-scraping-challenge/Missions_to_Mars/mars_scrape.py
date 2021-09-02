import pandas as pd
from bs4 import BeautifulSoup as bs
import time
from splinter import Browser
import html5lib
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    time.sleep(5)

    html = browser.html
    soup = bs(html, 'html.parser')
    browser.is_element_present_by_css("ul.item_list li.slide")

    items_list = soup.find_all('div', class_='list_text')
    item = soup.find('div', class_='list_text')
    news_title = item.find('div', class_='content_title').text

    date = item.find('div', class_='list_date').text
    news_p = item.find('div', class_='article_teaser_body').text

    # JPL Mars Images - Scrapping Featured Image
    image_url = 'https://spaceimages-mars.com'
    browser.visit(image_url)

    time.sleep(5)



    # print(image_soup.prettify)

    browser.links.find_by_partial_text('FULL IMAGE').click()

    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')

    image_list = image_soup.find('div', class_='fancybox-overlay')
    print(image_list)
    image_list = image_list.find('div', class_='fancybox-inner')
    image_url = image_list.find('img', class_='fancybox-image').get('src')
    print(image_url)

    featured_image_url = f'https://spaceimages-mars.com/{image_url}'

    # Mars Facts

    marsfacts_url = 'https://galaxyfacts-mars.com'

    marsfacts = pd.read_html(marsfacts_url)[0]
    marsfacts.columns = ['Measurement', 'Mars', 'Earth']
    marsfacts.set_index('Measurement', inplace=True)
    marsfacts = marsfacts.to_html()

    # Mars Hemisphere

    hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(hemisphere_url)

    time.sleep(5)

    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'html.parser')

    hemisphere_image_urls = []
    hemisphere_list = hemisphere_soup.find_all('div', class_='item')
    for item in hemisphere_list:
        url = 'https://marshemispheres.com/'

        title = item.find('h3').text
        title = title.replace('Enhanced', '')
        link = item.find('a')['href']
        full_link = url + link

        executable_path = {'executable_path': 'chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(full_link)
        html = browser.html
        soup = bs(html, 'html.parser')

        time.sleep(5)

        downloads = soup.find('div', class_='downloads')
        image = downloads.find('a')['href']
        image = url + image
        entry = {'title': title, 'image': image}
        hemisphere_image_urls.append(entry)

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "marsfacts": marsfacts,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()

    return mars_data


if __name__ == "__main__":
    print(scrape())
