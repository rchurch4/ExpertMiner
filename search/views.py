from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from forms import SearchForm

from stemming.porter2 import stem
from nltk.corpus import stopwords

import sql
import maxcoverage as mc

stop = stopwords.words('english')

# Create your views here.

def index(request):
	form = SearchForm()
	return render(request, 'search/index.html', {'form': form})

def author_index(request):
	form = SearchForm()
	return render(request, 'search/authorindex.html', {'form': form})

def team_index(request):
	form = SearchForm()
	return render(request, 'search/teamindex.html', {'form': form})

def results(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			query_list = []
			query = form.cleaned_data['query']
			# print query
			# print
			query_list = query.split(';')

			# CHANGE TO STEMMED WORDS
			stemmed_query_list = []
			stemmed_bigram_list = []
			for x in query_list:
				if ' ' in x:
					bigram_break = x.split()
					for y in bigram_break:
						if y not in stop:
							stemmed_query_list.append(stem(y))
					i = 0
					while i < len(bigram_break)-1:
						if bigram_break[i] not in stop and bigram_break[i+1] not in stop:
							stemmed_bigram_list.append(stem(bigram_break[i])+'$'+stem(bigram_break[i+1]))
						i+=1
				else:
					if x == '':
						pass
					else:
						stemmed_query_list.append(stem(x))

			# COMBINE BIGRAMS AND STEMMED KEYWORDS
			final_query_list = stemmed_bigram_list + stemmed_query_list

			if len(stemmed_bigram_list) == 0:
				stemmed_bigram_list = ['']

			keyword_author_list = [{'score': 'a zillion', 'name': u'Evimaria Terzi', 'id': '1095061'}]
			bigram_author_list = [{'score': 'a zillion', 'name': u'Evimaria Terzi', 'id': '1095061'}]
			keyword_author_list += sql.search_for_keywords(stemmed_query_list)
			bigram_author_list += sql.search_for_bigrams(stemmed_bigram_list)
			#print author_list[0]
			# Search the database of people on query_list
			# Assemble best 5 people from each group
		return render(request, 'search/results.html', {"keyword_author_list":keyword_author_list, "bigram_author_list":bigram_author_list, "query_list":final_query_list})
	return HttpResponseRedirect('/')

def team_search(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			query_list = []
			query = form.cleaned_data['query']
			# print query
			# print
			query_list = query.split(';')

			# CHANGE TO STEMMED WORDS
			stemmed_query_list = []
			for x in query_list:
				if ' ' in x:
					bigram_break = x.split()
					i = 0
					while i < len(bigram_break)-1:
						if bigram_break[i] not in stop and bigram_break[i+1] not in stop:
							stemmed_query_list.append(stem(bigram_break[i])+'$'+stem(bigram_break[i+1]))
						i+=1
				else:
					if x == '':
						pass
					else:
						stemmed_query_list.append(stem(x))

			# COMBINE BIGRAMS AND STEMMED KEYWORDS
			final_query_list = stemmed_query_list

			candidates = sql.get_team_candidates(final_query_list)
			print len(candidates)

			#DO MAX COVERAGE
			team_list = []
			team_scores = []
			t1 = mc.max_coverage(candidates, 0.1, 1, 5)
			team_list.append(t1[0])
			team_scores.append(t1[1])
			t1 = mc.max_coverage(candidates, 0.2, 1, 5)
			team_list.append(t1[0])
			team_scores.append(t1[1])
			t1 = mc.max_coverage(candidates, 0.5, 1, 5)
			team_list.append(t1[0])
			team_scores.append(t1[1])
			t1 = mc.max_coverage(candidates, 1, 1, 5)
			team_list.append(t1[0])
			team_scores.append(t1[1])
			t1 = mc.max_coverage(candidates, 1, 2, 5)
			team_list.append(t1[0])
			team_scores.append(t1[1])
			t1 = mc.max_coverage(candidates, 1, 0.5, 5)
			team_list.append(t1[0])
			team_scores.append(t1[1])
			t1 = mc.max_coverage(candidates, 0.2, 2, 5)
			team_list.append(t1[0])
			team_scores.append(t1[1])
			t1 = mc.max_coverage(candidates, 0.2, 3, 5)
			team_list.append(t1[0])
			team_scores.append(t1[1])
			t1 = mc.max_coverage(candidates, 0.5, 2, 5)
			team_list.append(t1[0])
			team_scores.append(t1[1])

			print team_scores

		return render(request, 'search/team_results.html', {"team_list":team_list, "team_scores":team_scores, "query_list":final_query_list})
	return HttpResponseRedirect('/')

def author_search(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			query_list = []
			authname = form.cleaned_data['query']
			author_list = [{'name': u'Evimaria Terzi', 'id': '1095061'}]
			author_list += sql.search_for_author(authname)
			return render(request, 'search/author_results.html', {"returned_list":author_list, "query_list":[authname]})
	return HttpResponseRedirect('/')

def authorlist(request):
	author_list = sql.get_first_100_authors()
	return render(request, 'search/authorlist.html', {'author_list':author_list})

def author_profile(request):
	# GET THE AUTHOR ID FROM THE URL
	auth_id = request.path
	auth_id = auth_id[16:]
	auth_id = auth_id[:len(auth_id)-1]

	author_papers = sql.get_author_papers_by_id(auth_id)
	author_keywords = sql.get_author_keywords_by_id(auth_id)
	author_bigrams = sql.get_author_bigrams_by_id(auth_id)
	author_name = author_keywords[0]['name']

	return render(request, 'search/authorprofile.html', {'author_name':author_name, 'author_papers':author_papers, 'author_keywords':author_keywords, 'author_bigrams':author_bigrams})

