# Web Scraper Personal Project
## Table of Contents:
- [Part 1. Description](#Description)
- [Part 2. scraper.py Description](#Scraper.py)
- [Part 3. link_data_scraper Description](#link_data_scraper.py)
# Description
The code stored in this folder is a personal project of mine. The task was to scrape contact infromation from the web of Commerical Real Estate Salesmen, utilizing primarily the `Selenium` Python library, via `webdriver.Safari()`. 

Wanting to work with an abstract framework for maximum reproducability, I used an Object Oriented Framework. The code that defines the classes used is stored in the `web_scraping` folder. The script in `main.py` imports and executes the code outlined in `/web_scraping/scraper.py` and `/web_scraping/link_data_scraper.py`. 

Additionally, there is a third file, `/web_scraping/constants.py`, which is used to store constants necessary to define our webscraping task, such as `SCRAPE_URL`. 

The project was largerly inspired by an online tutorial, **{Insert Link}**, made available by freecodecamp on YouTube. Ideally, for future use, the class structure should be changed with minimal effort, allowing for further generalized scraping tasks.

# Scraper.py
`/web_scraping/scraper.py` is the file which defines our main class: `Scraper()`. `Scraper`'s `__init__()` is defined in the following way:
```python
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
```
Our `Scraper` class has a few main methods that defines its behavior: 
 - `.launch_browser(self)`:
>     - Method to navigate to `constants.SCRAPE_URL`
 - `.get_links(self)`:> 
>    - Method to scrape `href` links on a webpage
 - `.link_iterator(self, data_scraper)`
>     - Method to iterate through the scraped `href` links obtained through `.get_links() `, called in the `.scrape_data()` class method
 - `.scrape_data(self)`
  >  - This method defines how we scrape data. I've elected to create another class, `LinkDataScraper` which is imported from the `/web_scraper/link_data_scraper.py` file. The `LinkDataScraper` Class creates a dictionary used to store data, and contains methods that scrape data by CSS element, or by Class element through the `Selenium` library. Additionally, there is some text String cleaning, primarily implmented through indexing, the `.strip()` method, and some regex courtesy of the `re` library.
- `.save_scrape(self)`
  >  - Saves scraped data into a Pandas DataFrame, exports it to a .csv file located at: `/Scraped_Results.csv`

# link_data_scraper.py
`/web_scraper/link_data_scraper.py` is the file which defines our secondary class: `LinkDataScraper()`, defined in the following way:
```python
class LinkDataScraper():
    def __init__(self,cols,driver:WebElement):
        self.cols = cols                                    #List of Str - Col Names To Specify What Data to pull
        self.data = dict()                                  #Empty Dict to Store Data Col Name : [vals,...]
        self.driver = driver                                #Selenium Object to Parse HTML
```
`LinkDataScraper()` has two main purposes: firstly to store and hold our data which will be obtained during the scraping process and then passed back to the main `Scraper()` class. Secondly, it defines the behavior of various scraping methods, specifically, what CSS or Class tag to scrape. The idea is that for future use, the methods of the `LinkDataScraper` class can be changed in an arbitrary way to scrape whatever information is at interest.

There are three main methods for the `LinkDataScraper` class:
- `.scrape(self)`
>   - .`scrape` defines what `.get_X_CSS_attribute` methods call in what sequence, and appends the output to a list stored in the `self.data` Python `dict()` structure.
- `.initialize_dict(self)`
> - This method sets up a dictionary with keys equal to the texts strings passed in the `self.cols` list, and values equal to an empty Python `list()`.
- clean(self,string)`
> - This method returns a string that has been stripped of all whitespace, newline characteres, or tab characters using `re.sub('\s+\,' ')` and the Python `.strip()` method.

An example of a `.get_X_CSS_attribute` method called in the `.scrape(self)` method is as follows:
```python
#Method to Scrape Email Address
def get_email_address(self):
    try:
        return str(self.driver.find_element_by_class_name("mailto").get_attribute('href'))[7:]
    except:
        return "No Email Address"
```
Without a doubt, I need to work on handling specific Errors thrown during this process, as my `try /except` block as it stands is far too generic. This can be imrpoved in future iterations of this process.