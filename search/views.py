from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from search import models

# Create your views here.

def index(request):
	return render(request, 'search/index.html', {})