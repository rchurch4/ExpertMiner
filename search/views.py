from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from forms import SearchForm
from models import Person

import sql

# Create your views here.

def index(request):
	form = SearchForm()
	return render(request, 'search/index.html', {'form': form})

def results(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			query_list = []
			query = form.cleaned_data['query']
			while query != 'end':
				nextComma = query.index(',')
				query_list.append(query[:nextComma])
				query = query[nextComma+1:]
			# Search the database of people on query_list
			# Assemble best 5 people from each group
	return render(request, 'search/results.html', {"query_list":query_list})

def authorlist(request):
	author_list = sql.get_first_100_authors()
	return render(request, 'search/authorlist.html', {'author_list':author_list})