import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

def main():
    # URL of the webpage to scrape
    url = 'https://www.pikawiz.com/cards'
    # Folder to save the sets
    save_folder = 'downloaded_images'
    
    # Function to create folders based on the set names
    def create_folders(folder, set_name):
        set_folder = os.path.join(folder, set_name)
        if not os.path.exists(set_folder):
            os.makedirs(set_folder)
            print(f"Created folder: {set_folder}")
        else:
            print(f"Folder already exists: {set_folder}")

    # Function to scrape the set names and create folders
    def scrape_and_create_folders(url, folder):
        # Create the base folder if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Set up Selenium WebDriver for Firefox
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
        driver.get(url)

        # Scroll to the bottom of the page to load all the content
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for new content to load
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Get the page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        # Find the specific containers to get the set names
        containers = soup.find_all('div', class_='page-container')
        for container in containers:
            subset_containers = container.find_all('div', class_='leftColCardSet')
            for subset in subset_containers:
                card_set_lists = subset.find_all('div', class_='card-set-list')
                for card_set_list in card_set_lists:
                    card_set_containers = card_set_list.find_all('div', class_='card-set-container')
                    for card_set in card_set_containers:
                        set_divs = card_set.find_all('a', class_='card-set')
                        for set_div in set_divs:
                            set_name_div = set_div.find('div', class_='set-name')
                            if set_name_div:
                                set_name = set_name_div.get_text(strip=True)
                                # Create a folder for this set name
                                create_folders(folder, set_name)

    # Scrape and create folders
    scrape_and_create_folders(url, save_folder)

if __name__ == "__main__":
    main()
