#All of the imports
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import web_scraping.constants as const
from web_scraping.link_data_scraper import LinkDataScraper

#Define class behavior
class Scraper(webdriver.Safari):
    def __init__(self, teardown=False, cols=[]):
        super(Scraper,self).__init__()
        self.wait = WebDriverWait(self,10)                      #Enforce Wait time of 10 Seconds
        self.implicitly_wait(10)                                #Implicitly wait if wifi or server is slow
        self.fullscreen_window()                                #Make window max
        self.teardown = teardown                                #Define how to exit
        self.links = []                                         #Save href links here
        self.cols = cols                                        #Save through the information to scrape - Column Names
        self.data = None                                        #Save method for data

    #Define how to navigate browser
    def launch_browser(self):
        self.get(const.SCRAPE_URL)                              #Navigate to Url
        #time.sleep(5)                                          #Pro Gamer Move - Turn on So You can Scroll Down to load all people
    
    #Use __exit__ to exit a while loop
    def __exit__(self, *args):
        if self.teardown:
            self.quit()

    #Method to get links we will need to navigate to
    def get_links(self):
        #Grab All of the links on the page by card-photo
        scraped_links = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "card-photo")
                )
                )
        #Iterate through the links and save them to self
        for scraped_link in scraped_links:
            self.links.append(
                scraped_link.get_attribute('href')              #Get the href element linking us to a sales person's profile
                )
    
    #Define a method on how to iterate through the links
    def link_iterator(self, data_scraper):
        for link in self.links:
            self.get(link)                                      #Navigate to URL from Href Using Scraper Class
            data_scraper.scrape()                               #Scrape data using LinkDataScraper Class

    #Define how to scrape data
    def scrape_data(self):
        data_scraper = LinkDataScraper(self.cols,driver=self)   #Initialize Object responsible for scraping and formatting data
        data_scraper.initialize_dict()                          #Call method to initialize helper variabes in Object
        self.link_iterator(data_scraper)                        #Start iterating through links and get data
        self.data = data_scraper.data                           #Transfer Data From data_scraper to main object

    #Define how to save the data we scraped
    def save_scrape(self):
        df = pd.DataFrame.from_dict(data=self.data)             #Create DataFrame From Scraped Results in self.data
        df.to_csv("Scraped_Results.csv")                        #Output Results to Scraped_Results.csv
