import scrapy
from selenium import webdriver
import logging
import os
import sys
import time
from marketwatch.items import CoinBaseItem

#%%
class CoinBaseSpider(scrapy.Spider):

    name = "coinbasespider"
    allowed_domains = ["coin.zerodha.com"]
    start_urls = ["https://coin.zerodha.com/funds"]
    base_url = "https://coin.zerodha.com/"
    logfile_name = "scrapy_%s_%s.log" %(name,"now")
    logfile_path = os.getcwd()
# we cant delete pre existing log file if it is loaded and running
# so this code will check if logging module is loaded ,then shutsdown the logging file that is being in process
# then os.remove will delete the file present at the path location    
    try:
        if "logging" in set(sys.modules)&set(globals()):
            logging.shutdown()
        else:
            pass
        if os.path.isfile(logfile_path +logfile_name ):
            os.remove(logfile_path+"\\"+logfile_name)
            print("Previous logger existed,deleting the logger!!!")
        else:
            pass
    except Exception:
        print(Exception)
        pass
    
    logging.basicConfig(filename = logfile_name,level = logging.DEBUG)
    
#%%
    def __init__(self, arbitargument = None, *args, **kwargs):
        logging.info("The TestSpider is initialized")
        # path should be given for phantomjs exe, also have to keeep 'r' before the path
        # https://stackoverflow.com/questions/29869757/selenium-phantomjs-raises-error
        self.driver = webdriver.PhantomJS(executable_path =r'Path for phantomjs.exe file')
        logging.info("Webdriver from selenium is started")
    
    def parse(self,response):
        logging.info("#############  The Parse function is called  #################")
        self.driver.get(response.url)
        time.sleep(5)
        fundamcdivs = self.driver.find_elements_by_xpath("//div[@class='units-row border-bottom']")
        
        for eachamc in fundamcdivs:
            item = CoinBaseItem()
            fundbroker = eachamc.find_element_by_xpath(".//div[@class='unit-20']/img").get_attribute('src')[44:-4]
            item['fundbroker'] = fundbroker
            fundcategories = eachamc.find_elements_by_xpath(".//div[@class='fund-list-categorywise']")
            
            for eachcategory in fundcategories:
                item['fundcategory'] = eachcategory.find_element_by_xpath(".//h3").text
                fundnames = eachcategory.find_elements_by_xpath(".//div[@ng-repeat='fund in value2']")
                
                for eachfund in fundnames:
                    item['fundlink'] = eachfund.find_element_by_xpath(".//a").get_attribute('href')
                    item['fundname'] = eachfund.find_element_by_xpath(".//a").text
                    yield item

        logging.info("##############  Driver is going to be closed  ################")
        self.driver.close()
        logging.info("##############  Selenium driver is closed now  ################")
        
        
