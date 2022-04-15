from web_scraping.scraper import Scraper

#Define main function to execute
def main():
    cols = ['Name','Email Address',
                'Telephone Number','Office Address',
                'Company Name','Email Address',
                'Caire Number','Specialty']
    
    #Use our Scraper as bot, exit window when complete
    with Scraper(teardown=True, cols=cols) as bot:
        print("launching")
        bot.launch_browser()                            #Launch bot
        bot.get_links()                                 #Get links
        bot.scrape_data()                               #Iterate through links - this will scrape the necessary information
        bot.save_scrape()                               #Save Scraped Data
        print("Exiting")                                #Let user know we are exiting from the scraper

# #For later
if __name__ == '__main__':
    main()