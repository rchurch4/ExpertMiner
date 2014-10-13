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

def author_index(request):
	form = SearchForm()
	return render(request, 'search/authorindex.html', {'form': form})

def results(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			query_list = []
			query = form.cleaned_data['query']
			# print query
			# print
			query_list = query.split()
			author_list = sql.search_for_keywords(query_list)
			# Search the database of people on query_list
			# Assemble best 5 people from each group
		return render(request, 'search/results.html', {"returned_list":author_list, "query_list":query_list})
	return HttpResponseRedirect('/')

def author_search(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			query_list = []
			authname = form.cleaned_data['query']
			author_list = sql.search_for_author(authname)
			return render(request, 'search/results.html', {"returned_list":author_list, "query_list":[authname]})
	return HttpResponseRedirect('/')

def authorlist(request):
	author_list = sql.get_first_100_authors()
	return render(request, 'search/authorlist.html', {'author_list':author_list})

def author_profile(request):
	return render(request, 'search/authorprofile.html', {})