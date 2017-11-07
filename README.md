# Stock-scraping
This project will scrape data from marketwatch.com for getting all listed indian stocks, also scrapes mutual funds from coinbase in zerodha.

Change the working directory to spiders folder in marketwatch/spiders and open command line from there.

You need to have PhantomJs driver to be downloaded if you dont have it from this [link](https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip)

Run the follwing assuming you have installed scrapy in python 3.5

```
$ scrapy crawl marketwatchspider -o stocks.json
```
To create a json file to have a list of all stocks


```
$ scrapy crawl coinbasespider -o mutualfunds.json
```
To create a json file listing all the important mutual funds
