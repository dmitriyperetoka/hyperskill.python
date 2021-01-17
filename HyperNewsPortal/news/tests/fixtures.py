import random

dates = ["2020-02-09 15:15:10", "2020-02-10 10:15:10", "2020-02-09 16:15:10"]
links = [3823981, 2619329, 1923563]

assert len(dates) == len(links), 'different quantity of dates and links'

random.shuffle(dates)
random.shuffle(links)

articles = []

for index, date in enumerate(dates):
    link = links[index]
    article = {
        'created': date,
        'text': f'Text of the news {link}',
        'title': f'News {link}',
        'link': link,
    }
    articles.append(article)

query_pattern_1 = 'Just'
query_pattern_2 = 'another'

new_article_kwargs = {
    'title': f'{query_pattern_1} some title',
    'text': f'Simply {query_pattern_2} text.',
}
