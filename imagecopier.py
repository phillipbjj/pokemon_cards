import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from urllib.parse import urljoin

def main():
    # URL of the webpage to scrape
    url = 'https://www.pikawiz.com/cards/noblevictories'
    # Folder to save images
    save_folder = 'downloaded_images/Noble Victories'
    
    # Function to download images
    def download_image(url, folder):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_name = os.path.join(folder, url.split('/')[-1])
            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

    # Function to scrape and download .png images
    def scrape_images(url, folder):
        # Create folder if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Set up Selenium WebDriver for Firefox
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
        driver.get(url)

        # Scroll to the bottom of the page to load all images
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for new images to load
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Get the page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        # Find the specific containers
        containers = soup.find_all('div', class_='page-container')
        for container in containers:
            subset_containers = container.find_all('div', class_='leftCol cardSet')
            for subset in subset_containers:
                card_lists = subset.find_all('div', class_='card-list')
                for card_list in card_lists:
                    card_containers = card_list.find_all('div', class_='card-list-item-cards')
                    for card in card_containers:
                        img_tags = card.find_all('img')
                        for img in img_tags:
                            img_url = img.get('src')
                            if img_url and img_url.endswith('.png'):
                                # Construct the full URL
                                full_img_url = urljoin(url, img_url)
                                download_image(full_img_url, folder)

    # Scrape and download images
    scrape_images(url, save_folder)

if __name__ == "__main__":
    main()
