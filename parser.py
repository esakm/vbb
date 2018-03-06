

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
        self.string_to_parse = new_article.lower()

    def count_good_keywords(self):
        count = 0
        for keyword in self.good_keywords:
            count += self.string_to_parse.count(keyword.replace('\n', '').replace(r'"company"', self.company_name).lower())

        if count == 0:
            return 1
        else:
            return count

    def count_bad_keywords(self):
        count = 0
        for keyword in self.bad_keywords:
            count += self.string_to_parse.count(keyword.replace('\n', '').replace(r'"company"', self.company_name).lower())

        if count == 0:
            return 1
        else:
            return count

    def count_op_keywords(self):
        count = 0
        for keyword in self.optimistic_keywords:
            count += self.string_to_parse.count(keyword.replace('\n', '').replace(r'"company"', self.company_name).lower())
        if count == 0:
            return 1
        else:
            return count

    def count_pe_keywords(self):
        count = 0
        for keyword in self.pessimistic_keywords:
            count += self.string_to_parse.count(keyword.replace('\n', '').replace(r'"company"', self.company_name).lower())

        if count == 0:
            return 1
        else:
            return count
