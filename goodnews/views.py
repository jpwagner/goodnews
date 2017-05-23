from datetime import datetime, timedelta

from django.conf import settings
from django.shortcuts import render, redirect
from django.utils import timezone

from . import models


def home(request):
	articles = models.Article.objects.filter(
		published_at__gt=timezone.now() - timedelta(days=2),
		score__gt=settings.SCORE_THRESHOLD
		)
	return render(request, 'home.html', {'articles': articles})
