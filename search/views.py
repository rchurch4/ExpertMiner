from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from forms import SearchForm

from stemming.porter2 import stem
from nltk.corpus import stopwords

import sql

stop = stopwords.words('english')

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

			# CHANGE TO STEMMED WORDS
			stemmed_query_list = []
			for x in query_list:
				if x not in stop:
					stemmed_query_list.append(stem(x))
			
			# CREATE BIGRAMS OUT OF INDIVIDUAL TERMS
			stemmed_bigram_list = []
			i = 0
			while i < len(query_list)-1:
				if query_list[i] not in stop and query_list[i+1] not in stop:
					stemmed_bigram_list.append(stem(query_list[i])+'$'+stem(query_list[i+1]))
				i+=1

			# COMBINE BIGRAMS AND STEMMED KEYWORDS
			final_query_list = stemmed_bigram_list + stemmed_query_list

			if len(stemmed_bigram_list) == 0:
				stemmed_bigram_list = ['']

			author_list = [{'score': 'a zillion', 'name': u'Evimaria Terzi', 'id': '778977'}]
			author_list += sql.search_for_keywords(stemmed_query_list, stemmed_bigram_list)
			#print author_list[0]
			# Search the database of people on query_list
			# Assemble best 5 people from each group
		return render(request, 'search/results.html', {"returned_list":author_list, "query_list":final_query_list})
	return HttpResponseRedirect('/')

def author_search(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			query_list = []
			authname = form.cleaned_data['query']
			author_list = [{'name': u'Evimaria Terzi', 'id': '778977'}]
			author_list += sql.search_for_author(authname)
			return render(request, 'search/results.html', {"returned_list":author_list, "query_list":[authname]})
	return HttpResponseRedirect('/')

def authorlist(request):
	author_list = sql.get_first_100_authors()
	return render(request, 'search/authorlist.html', {'author_list':author_list})

def author_profile(request):
	# GET THE AUTHOR ID FROM THE URL
	auth_id = request.path
	auth_id = auth_id[16:]
	auth_id = auth_id[:len(auth_id)-1]

	author_papers = sql.get_author_papers_by_id(auth_id)[0]
	author_keywords = sql.get_author_keywords_by_id(auth_id)[0]
	author_bigrams = sql.get_author_bigrams_by_id(auth_id)[0]

	print author_info
	return render(request, 'search/authorprofile.html', {'author_papers':author_papers, 'author_keywords':author_keywords, 'author_bigrams':author_bigrams})

	