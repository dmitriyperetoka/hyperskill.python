import json
from typing import Dict, List, Union

from django.conf import settings


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
