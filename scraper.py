import requests
from selenium import webdriver
from threading import Thread
import bs4
import stringhelper


class Scraper(Thread):

    def __init__(self, company_tuple):
        Thread.__init__(self)
        self.scrape_results = ()
        self.driver = None
        self.company_strings = company_tuple
        self.driver_done = False

    def get_bs(self):
        page_source = self.driver.page_source
        bs = bs4.BeautifulSoup(page_source, 'html.parser')
        return bs

    def initialize_driver(self):
        self.driver = webdriver.Chrome()

    def close_driver(self):
        self.driver.close()

    def get_closing_price(self):
        self.driver.get("https://www.google.ca/search?q=NASDAQ:" + self.company_strings[0])
        bs = self.get_bs()

        price = bs.find('span', attrs={'class': '_Rnb fmob_pr fac-l'}).getText().replace(',', '')

        return float(price)

    def get_price_change(self):
        bs = self.get_bs()

        delta = bs.find('span', attrs={'class': 'fac-cc'}).getText().split(' ')[0]
        percentage = bs.find('span', attrs={'class': 'fac-cc'}).getText().split(' ')[1]\
            .replace('%', '').replace('(', '').replace(')', '')

        return float(delta), float(percentage)

    def is_price_up(self):
        bs = self.get_bs()
        direction = bs.findAll('span', attrs={'class': '_Mnb vk-fin-dn finance_answer_card__apc fac-c'})

        if direction is None:
            return True
        else:
            return False

    def next_page(self, page_string):
        button = self.driver.find_element_by_link_text(page_string)
        button.click()

    def get_url_dict(self):
        self.driver.get("https://www.google.ca/search?q=" + stringhelper.prepare_for_news_search(self.company_strings[1]
                                                                                                 ) + "&tbm=nws")
        page_string = 2
        article_dict = {}
        for i in range(4):
            bs = self.get_bs()
            url_tag_list = bs.find_all('h3', attrs={'class': 'r _gJs'})
            summary_tag_list = bs.find_all('div', attrs={'class': 'st'})
            time_tag_list = bs.find_all('span', attrs={'class': 'f nsa _QHs'})
            title_temp_list = bs.find_all('h3', attrs={'class': 'r _gJs'})
            for k in range(len(url_tag_list)):
                url = url_tag_list.pop().find('a')['href']
                article_dict[url] = [summary_tag_list.pop().getText().replace("\xa0...", '').replace("\xa0... ", ''),
                                     time_tag_list.pop().getText(), title_temp_list.pop()
                                     .getText().replace(url, '').replace(" ...", "")]

            self.next_page(str(page_string))
            page_string += 1

        return article_dict

    def get_articles(self, article_dict):
        for url in article_dict:
            article = ''
            try:
                res = requests.get(url, timeout=5)
                res.raise_for_status()
            except Exception as e:
                continue
            bs = bs4.BeautifulSoup(res.text, 'html.parser')
            time_placeholder = article_dict[url][1]
            title_placeholder = article_dict[url][2]
            paragraphs = bs.find_all('p')
            for paragraph in paragraphs:
                article += paragraph.getText()

            article_dict[url] = [article, time_placeholder, title_placeholder]

        return article_dict

    def run(self):
        self.initialize_driver()
        price = self.get_closing_price()
        (delta, percentage) = self.get_price_change()
        if not self.is_price_up():
            delta = -delta
            percentage = -percentage

        pre_lookup_article_dict = self.get_url_dict()
        self.driver.close()
        self.driver_done = True
        article_dict = self.get_articles(pre_lookup_article_dict)
        self.scrape_results = (article_dict, price, delta, percentage)

    def get_scrape_results(self):
        return self.scrape_results
