
import scrapy
from selenium import webdriver
import logging
import os
import sys
import time
from marketwatch.items import MarketwatchItem

#%%
class MarketwatchSeleniumSpider(scrapy.Spider):

    name = "marketwatchspider"
    allowed_domains = ["marketwatch.com"]
    start_urls = ["https://www.marketwatch.com/tools/markets/stocks/country/india"]
    base_url = "https://www.marketwatch.com/tools/markets/stocks/country/india/"
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
        self.driver = webdriver.PhantomJS(executable_path =r'Path for PhantomJS.exe file')
        logging.info("Webdriver from selenium is started")
    
        
    def parse_next_items(self):
        
        logging.info("Parse next items function is called")
        tempobject = self.driver.find_element_by_xpath("//*[@id='marketsindex']/table/tbody")
        company_divs = tempobject.find_elements_by_xpath(".//tr")
        logging.info("Found %d company divs " %company_divs.__len__())
        items = []
        for eachcompany in company_divs:
            item = MarketwatchItem()
            eachcompanydata = eachcompany.find_elements_by_xpath(".//td")
            item['company_exchange'] =  eachcompanydata[1].text
            item['company_code'] = eachcompanydata[0].find_element_by_xpath(".//a/small").text[1:-1]
            item['company_name'] = eachcompanydata[0].find_element_by_xpath(".//a").text[:-(len(item['company_code'])+2)]
            item['company_sector'] = eachcompanydata[2].text
            item['company_url'] = eachcompanydata[0].find_element_by_xpath(".//a").get_attribute('href')
            items.append(item)
        
        return items

        
    def parse(self,response):
        logging.info("#############  The Parse function is called  #################")
        self.driver.get(response.url)
        time.sleep(5)
        currentpageno = 1
        
        while currentpageno != 34:
            logging.info("########### Currently parsing page no %d " %currentpageno)
            currentpageitems = self.parse_next_items()
            nextpageno = currentpageno + 1
            self.driver.get(self.base_url+str(nextpageno))
            time.sleep(15)
            #currentpageno = int(self.driver.find_element_by_xpath(".//li[@class = 'active']/span").text)
            currentpageno = nextpageno
            for eachitem in currentpageitems:
                yield eachitem
        
        logging.info("##############  Driver is going to be closed  ################")
        self.driver.close()
        logging.info("##############  Selenium driver is closed now  ################")
        
        
