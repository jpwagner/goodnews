from django.conf import settings
from django.db import models

from core.models import SuperModel


class Article(SuperModel):
	title = models.CharField(max_length=255, null=True, blank=True)
	author = models.CharField(max_length=255, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	url = models.URLField(max_length=1000, null=True, blank=True)
	score = models.FloatField(default=0)
	published_at = models.DateTimeField()

	def __unicode__(self):
		return self.title