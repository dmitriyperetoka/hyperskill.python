import datetime
import json
import random
from typing import Union

from django.conf import settings
from django.http.response import HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest
from django.shortcuts import redirect, render

from .services import get_articles


def index(request: HttpRequest) -> HttpResponseRedirect:  # noqa
    """Redirect to the main page."""
    return redirect('main_page')


def main_page(request: HttpRequest) -> HttpResponse:
    """Display the main page with list of articles filtered by query
    if provided.
    """
    articles = get_articles()
    query = request.GET.get('q')

    if query:
        articles = [
            article for article in articles
            if query.lower() in article['title'].lower()
            or query.lower() in article['text'].lower()
        ]

    return render(request, 'main_page.html', {'articles': articles})


def article_page(request: HttpRequest, link: int) -> HttpResponse:
    """Display the page with details a single article."""
    articles = get_articles()
    for article in articles:
        if article['link'] == link:
            return render(request, 'article_page.html', {'article': article})

    return HttpResponse(status=404)


def create_article(request: HttpRequest) -> Union[
    HttpResponse, HttpResponseRedirect
]:
    """Create an article and append it to the JSON file."""
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')

        if title and text:
            articles = get_articles()
            existing_links = {q['link'] for q in articles}

            while True:
                link = random.randint(1000000, 9999999)
                if link not in existing_links:
                    break

            created = datetime.datetime.now().strftime(settings.DATETIME_FORMATTING)

            article = {
                'created': created,
                'text': text,
                'title': title,
                'link': link,
            }

            articles.append(article)

            with open(settings.NEWS_JSON_PATH, 'w', encoding='utf-8') as file:
                json.dump(articles, file)

            return redirect('main_page')

    return render(request, 'create_article.html')
