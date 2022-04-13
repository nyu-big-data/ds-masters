#All of the imports
import re
from selenium.webdriver.remote.webelement import WebElement

class LinkDataScraper():
    def __init__(self,cols,driver:WebElement):
        self.cols = cols                                    #List of Str - Col Names To Specify What Data to pull
        self.data = dict()                                  #Empty Dict to Store Data Col Name : [vals,...]
        self.driver = driver                                #Selenium Object to Parse HTML

    def initialize_dict(self):
    #Iterate through the colunmns passed to 
        for key in self.cols:
            self.data[key] = []                             #Create an empty list for each key passed through cols

    #Method to load all of the links and iterate thorugh them
    def scrape(self):   
        #Scrape the Necessary Data
        self.data['Telephone Number'].append(           #Append Result of get_telephone_number Method
            self.get_telephone_number()
            )
        self.data['Name'].append(                       #Append Result of get_name
            self.get_name()
        )
        self.data['Email Address'].append(              #Append Result of get_email_address
            self.get_email_address()                    
        )
        self.data['Company Name'].append(               #Append Result of get_email_address
            self.get_company_name()                    
        )
        self.data['Office Address'].append(             #Append Result of get_office_address
            self.get_office_address()
        )
        self.data['Caire Number'].append(               #Append Result of get_caire_number
            self.get_caire_number()
        )
        self.data['Specialty'].append(
            self.get_specialty()                        #Append Results of get_specialty
        )
        #time.sleep(.5)                                 #See if this stops it from limiting our traffic
        

    #Method to Scrape Telephone Number
    def get_telephone_number(self):
        try:
            return str(self.driver.find_element_by_class_name("contact-info").find_element_by_css_selector('a').get_attribute('href'))[4:]
        except:
            return "No Telephone Number"

    #Method to Scrape Telephone Number
    def get_name(self):
        try:
            return self.clean(self.driver.find_element_by_css_selector("h3").text)
        except:
            return "No Name"
    #Method to Scrape Email Address
    def get_email_address(self):
        try:
            return str(self.driver.find_element_by_class_name("mailto").get_attribute('href'))[7:]
        except:
            return "No Email Address"

    #Method to Scrape Company Name
    def get_company_name(self):
        try:
            return self.clean(self.driver.find_element_by_class_name("office-name").text)
        except:
            return "No Company Name"

    #Method to Scrape Company Name
    def get_office_address(self):
        try:
            return self.clean(self.driver.find_element_by_class_name("office-address").text)
        except:
            return "No Company Address"
    
    #Method to Scrape Caire Number
    def get_caire_number(self):
        try:
           return self.driver.find_element_by_class_name("contact-info").find_element_by_css_selector("p").text[9:]
        except:
            return "No Caire Number"

    #Method to Scrape Caire Number
    def get_specialty(self):
        try:
           return self.clean(self.driver.find_element_by_class_name("subtitle").find_element_by_css_selector('p').text)
        except:
            return "No Specialty"

    #Define how to clean data of unecessary blank space
    def clean(self,string):
        return re.sub('\s+',' ',str(string)).strip()