import datetime
import json
import random

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .services import binary_search, insertion_sort


def index(request):  # noqa
    return redirect('main_page')


def get_articles():
    try:
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            articles = json.load(json_file)
    except FileNotFoundError:
        return []
    else:
        return articles


def main_page(request):
    articles = get_articles()
    query = request.GET.get('q')

    if query:
        articles = [
            q for q in articles if query in q['title'] or query in q['text']
        ]

    for article in articles:
        article['created'] = datetime.datetime.strptime(
            article['created'], '%Y-%m-%d %H:%M:%S'
        )

    return render(request, 'main_page.html', {'articles': articles})


def article_page(request, link):
    articles = get_articles()
    article_index = binary_search(articles, link)

    if article_index is not False:
        return render(
            request, 'article_page.html', {'article': articles[article_index]}
        )

    return HttpResponse(status=404)


def create_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')

        if title and text:
            articles = get_articles()
            existing_links = {q['link'] for q in articles}
            link = random.choice(
                [q for q in range(1000000, 9999999) if q not in existing_links]
            )
            created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            article = {
                'created': created,
                'text': text,
                'title': title,
                'link': link
            }
            articles.append(article)
            insertion_sort(articles)

            with open(settings.NEWS_JSON_PATH, 'w') as json_file:
                json.dump(articles, json_file)

            return redirect('main_page')

    return render(request, 'create_article.html')
