from django.conf import settings
from django.shortcuts import render, redirect

from . import models

def home(request):
	# articles = models.Article.objects.filter(score__gte=0.6)
	articles = models.Article.objects.all()
	return render(request, 'home.html', {'articles': articles})
