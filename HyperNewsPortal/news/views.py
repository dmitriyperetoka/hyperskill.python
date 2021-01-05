import datetime
import json
import random
from typing import Dict, List, Union

from django.conf import settings
from django.http.response import HttpResponse, HttpResponseRedirect
from django.http.request import HttpRequest
from django.shortcuts import redirect, render

DATETIME_FORMATTING = '%Y-%m-%d %H:%M:%S'


def index(request: HttpRequest) -> HttpResponseRedirect:  # noqa
    """Redirect to the main page."""
    return redirect('main_page')


def get_articles() -> List[Dict[str, Union[str, int]]]:
    """Return the articles list from JSON file if exists or return
    empty list.
    """
    try:
        with open(settings.NEWS_JSON_PATH, 'r', encoding='utf-8') as file:
            articles = json.load(file)
    except FileNotFoundError:
        return []
    else:
        return articles


def main_page(request: HttpRequest) -> HttpResponse:
    """Display the main page with list of articles filtered by query
    if provided.
    """
    articles = get_articles()
    query = request.GET.get('q')

    if query:
        articles = [
            q for q in articles if query in q['title'] or query in q['text']
        ]

    return render(request, 'main_page.html', {'articles': articles})


def article_page(request: HttpRequest, link: int) -> HttpResponse:
    """Display the page with details a single article."""
    articles = get_articles()
    for article in articles:
        if article['link'] == link:
            return render(request, 'article_page.html', {'article': article})

    return HttpResponse(status=404)


def create_article(
        request: HttpRequest
) -> Union[HttpResponse, HttpResponseRedirect]:
    """Create an article and append it to the JSON file."""
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')

        if title and text:
            articles = get_articles()
            existing_links = {q['link'] for q in articles}

            link = random.choice(
                [q for q in range(1000000, 9999999) if q not in existing_links]
            )
            created = datetime.datetime.now().strftime(DATETIME_FORMATTING)

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
