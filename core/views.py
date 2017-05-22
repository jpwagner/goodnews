from django.conf import settings
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages


def my_404_view(request):
    messages.error(request, 'PAGE NOT FOUND', extra_tags='safe')
    return redirect(reverse('home'))

def my_500_view(request):
    messages.error(request, 'AN ERROR OCCURRED', extra_tags='safe')
    return redirect(reverse('home'))
