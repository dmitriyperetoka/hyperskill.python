import datetime
import json
import random

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render


def index(request):  # noqa
    return redirect('main_page')


def get_articles():
    try:
        with open(settings.NEWS_JSON_PATH, 'r', encoding='utf-8') as file:
            articles = json.load(file)
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
    for article in articles:
        if article['link'] == link:
            return render(
                request, 'article_page.html', {'article': article}
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

            with open(settings.NEWS_JSON_PATH, 'w', encoding='utf-8') as file:
                json.dump(articles, file)

            return redirect('main_page')

    return render(request, 'create_article.html')
