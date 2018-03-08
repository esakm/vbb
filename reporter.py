import scraper
import article_parser
from threading import Thread

class Reporter(Thread):

    def __init__(self, company):
        Thread.__init__(self)
        self._scraper = scraper.Scraper((company[0], company[1]))
        self._parser = article_parser.Parser(self._scraper.company_name)
        self._company = company
        self._scraper_results = ()
        self.report = {}
        self.report['articles'] = {}
        self.report['good-count'] = 0
        self.report['bad-count'] = 0
        self.report['op-count'] = 0
        self.report['pe-count'] = 0
        self.driver_done = False

    def start_report(self):
        self._scraper.start()

    def poll_scraper(self):
        return self._scraper.driver_done

    def get_scrape_report(self):
        self._scraper_results = self._scraper.get_scrape_results()

    def parse_article(self):
        good_count = self._parser.count_good_keywords()
        bad_count = self._parser.count_bad_keywords()
        op_count = self._parser.count_op_keywords()
        pe_count = self._parser.count_pe_keywords()

        return good_count, bad_count, op_count, pe_count

    def parse_articles(self):
        collective_score = 0
        for article_url in self._scraper_results[0]:
            self._parser.switch_articles(self._scraper_results[0][article_url])
            counts = self.parse_article()

            article_score = counts[0] - counts[1] + ((counts[2] * 10) - (counts[3] * 10))
            self.report['good-count'] += counts[0]
            self.report['bad-count'] += counts[1]
            self.report['op-count'] += counts[2]
            self.report['pe-count'] += counts[3]
            article_weight = self._parser.parse_date()
            collective_score += article_score/article_weight
            self.report['articles'][article_url] = (article_score, article_weight)
        self.report['total-score'] = collective_score

    def calculate_score(self):
        if 'B' in self._company[3]:
            company_weight = 10
        elif 'M' in self._company[3] and float(self._company[3].replace('$', '').replace('M', '')) > 750:
            company_weight = 7.5
        elif 'M' in self._company[3] and float(self._company[3].replace('$', '').replace('M', '')) > 500:
            company_weight = 5
        elif 'M' in self._company[3] and float(self._company[3].replace('$', '').replace('M', '')) > 250:
            company_weight = 2.5
        else:
            company_weight = 1
        if 'n/a' not in self._company[4]:
            company_weight += 2018 - int(self._company[4])

        price = self._scraper_results[1]
        delta = self._scraper_results[2]
        percentage = self._scraper_results[3]
        article_total_score = self.report['total-score']
        op = self.report['op-count']
        pe = self.report['pe-count']
        op_pe = op + pe
        prelim_score = 0
        prelim_score += op/op_pe * 1000
        prelim_score -= pe/op_pe * 1000
        final_score = ((prelim_score + article_total_score) + ((percentage * 100)/(price + delta))) * company_weight

        self.report['final-score'] = final_score
        self.report['price'] = price
        self.report['percentage'] = percentage
        self.report['delta'] = delta

    def dump_report(self):
        print('Dumping report for %s' % self._company[1])
        file_name = '{}{}-{}'.format('reports//', self.report['final-score'], self._company[1])
        file = open(file_name, 'w')
        content = ''
        for key in self.report:
            if key is 'articles':
                content += 'Articles:\n'
                for article_url in self.report['articles']:
                    content += article_url + ":\n"
                    content += 'Score: ' + str(self.report['articles'][article_url][0]) + \
                               "\nWeight: " + str(self.report['articles'][article_url][1])
                    content += '\n'
                continue
            content += key + ': '
            content += str(self.report[key])
            content += '\n'
        file.write(content)
        file.close()

    def run(self):
        print('Generating report for %s' % self._company[1])
        self._scraper.start()
        while not self.poll_scraper():
            pass
        self.driver_done = True
        while self._scraper.is_alive():
            pass
        self.get_scrape_report()
        del self._scraper
        self.parse_articles()
        self.calculate_score()
        self.dump_report()
