from datetime import date

month_list = {'Jan.': 1,
                          'Feb.': 2,
                          'Mar.': 3,
                          'Apr.': 4,
                          'May': 5,
                          'Jun.': 6,
                          'Jul.': 7,
                          'Aug.': 8,
                          'Sep.': 9,
                          'Oct.': 10,
                          'Nov.': 11,
                          'Dec.': 12}


class Parser:
    bad_keyword_file = open('keywords\\bad_keywords.txt')
    good_keyword_file = open('keywords\\good_keywords.txt')
    optimistic_keyword_file = open('keywords\\optimistic_keywords.txt')
    pessimistic_keyword_file = open('keywords\\pessimistic_keywords.txt')
    bad_keywords = bad_keyword_file.readlines()
    good_keywords = good_keyword_file.readlines()
    optimistic_keywords = optimistic_keyword_file.readlines()
    pessimistic_keywords = pessimistic_keyword_file.readlines()

    def __init__(self, name):
        self.string_to_parse = ''
        self.company_name = name

    def switch_articles(self, new_article):
        self.string_to_parse = new_article
        self.string_to_parse[0] = self.string_to_parse[0].lower()
        self.string_to_parse[2] = self.string_to_parse[2].lower()

    def count_good_keywords(self):
        count = 0
        for keyword in self.good_keywords:
            count += self.string_to_parse[0].count(
                keyword.replace('\n', '').replace(r'"company"', self.company_name).lower())
            count += self.string_to_parse[2].count(
                keyword.replace('\n', '').replace(r'"company"', self.company_name).lower())

        if count == 0:
            return 1
        else:
            return count

    def count_bad_keywords(self):
        count = 0
        for keyword in self.bad_keywords:
            count += self.string_to_parse[0].count(
                keyword.replace('\n', '').replace(r'"company"', self.company_name).lower())
            count += self.string_to_parse[2].count(
                keyword.replace('\n', '').replace(r'"company"', self.company_name).lower())

        if count == 0:
            return 1
        else:
            return count

    def count_op_keywords(self):
        count = 0
        for keyword in self.optimistic_keywords:
            count += self.string_to_parse[0].count(
                keyword.replace('\n', '').replace(r'"company"', self.company_name).lower())
            count += self.string_to_parse[2].count(
                keyword.replace('\n', '').replace(r'"company"', self.company_name).lower())
        if count == 0:
            return 1
        else:
            return count

    def count_pe_keywords(self):
        count = 0
        for keyword in self.pessimistic_keywords:
            count += self.string_to_parse[0].count(
                keyword.replace('\n', '').replace(r'"company"', self.company_name).lower())
            count += self.string_to_parse[2].count(
                keyword.replace('\n', '').replace(r'"company"', self.company_name).lower())
        if count == 0:
            return 1
        else:
            return count

    def parse_date(self):
        article_date = self.string_to_parse[1].split(' ')
        if 'hour' in article_date[1] or 'hours' in article_date[1]:
            return int(article_date[0])
        elif 'minute' in article_date[1] or 'minutes' in article_date[1]:
            return int(article_date[0])/10
        else:
            ar_date = date(int(article_date[2]), month_list[article_date[0]],
                           int(article_date[1].replace(',', '')))
            current_date = date.today()
            delta = current_date - ar_date
            return int(delta.days) * 24
