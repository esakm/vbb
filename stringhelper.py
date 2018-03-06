not_allowed_in_name = [
    'Corp.',
    'Corporate',
    'Corporation',
    'Ltd.',
    'Limited',
    'Systems',
    'Inc.',
    'Co.',
    'LLC.',
]


def prepare_for_news_search(company_name):
    for word in not_allowed_in_name:
        company_name = company_name.replace(word, '').replace(',', '')
    return company_name
