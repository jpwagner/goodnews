import urllib
import json
from dateutil import parser

from django.conf import settings
from django.utils import timezone

from textblob import TextBlob
from newspaper import Article

from goodnews import models as gn_models


def run_article_scores():
	sources_json = json.loads(urllib.urlopen(settings.SOURCES_ENDPOINT + '?apiKey=%s&language=en' % settings.NEWS_API_KEY).read())

	for source in sources_json['sources']:
		source_articles_endpoint = settings.ARTICLES_ENDPOINT + '?apiKey=%s&source=%s&sortBy=%s' % (settings.NEWS_API_KEY, source['id'], source['sortBysAvailable'][0])
		articles_json = json.loads(urllib.urlopen(source_articles_endpoint).read())

		for article in articles_json['articles']:
			try:
				content = Article(article['url'])
				content.download()
				content.parse()

				words = TextBlob(content.text)
				words.sentiment

				new_article = gn_models.Article.objects.get_or_create(url=article['url'])
				new_article.title = article['title']
				new_article.author = article['author']
				new_article.description = article['description']
				new_article.score = (words.polarity)*(1-words.subjectivity)
				new_article.published_at = parser.parse(article['publishedAt'])
				new_article.save()

			except:
				continue

