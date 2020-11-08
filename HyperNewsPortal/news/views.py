import datetime
import json

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect, render


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
        articles = tuple(q for q in articles if query in q['title'])

    for article in articles:
        article['created'] = datetime.datetime.strptime(
            article['created'],
            '%Y-%m-%d %H:%M:%S'
        )

    return render(request, 'main_page.html', {'articles': articles})


def article_page(request, link):
    articles = get_articles()

    for article in articles:
        if article['link'] == link:
            return render(request, 'article_page.html', {'article': article})

    raise Http404


def create_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')

        if title and text:
            articles = get_articles()

            if articles:
                link = max(q['link'] for q in articles) + 1
            else:
                link = 1

            created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            article = {
                'created': created,
                'text': text,
                'title': title,
                'link': link
            }
            articles.append(article)

            with open(settings.NEWS_JSON_PATH, 'w') as json_file:
                json.dump(articles, json_file)

            return redirect('main_page')

    return render(request, 'create_article.html')
