from django.db import connection

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

# END dictfetchall

def get_first_100_authors ():
	cursor = connection.cursor()

	cursor.execute('select author.name from author limit 100')
	return dictfetchall(cursor)

# END get_first_100_authors

def search_for_author (name):
	cursor = connection.cursor()
	name = name.replace(' ', '%')
	print name
	query = "select author.name, author.id from author where author.name like '%" + name + "%' limit 100"

	cursor.execute(query)
	return dictfetchall(cursor)

# END SEARCH_FOR_AUTHOR

def search_for_keywords (keys):
	cursor = connection.cursor()

	x = ""
	for k in keys:
		x += '\'' + k + '\', '
	x = x[:len(x)-2]

	query = """
		select 
		auth.name,
		auth.id,
		ak.freq as score
		from author as auth
		inner join freqauthkeywords as ak on ak.auth_id = auth.id
		inner join freqkeywords as kw on kw.id = ak.key_id
		where kw.keyword in ("""+x+""")
		group by auth.name, auth.id, kw.id
		order by -ak.freq
		limit 100
	"""

	cursor.execute(query)
	return dictfetchall(cursor)

def search_for_bigrams (bigrams):
	cursor = connection.cursor()

	y = ""
	for k in bigrams:
		y += '\'' + k + '\', '
	y = y[:len(y)-2]

	query = """
		select 
		auth.name,
		auth.id,
		ab.freq as score

		from author as auth
		inner join freqauthbigrams as ab on ab.auth_id = auth.id
		inner join freqbigrams as bi on bi.id = ab.bigram_id

		where bi.bigram in ("""+y+""")

		group by auth.name, auth.id, bi.id

		order by -ab.freq
		limit 100
	"""
	cursor.execute(query)
	return dictfetchall(cursor)

def search_for_both (keys, bigrams):
	cursor = connection.cursor()

	x = ""
	for k in keys:
		x += '\'' + k + '\', '
	x = x[:len(x)-2]
	# print x
	# print

	y = ""
	for k in bigrams:
		y += '\'' + k + '\', '
	y = y[:len(y)-2]

	query = """select
				distinct auth.name,
				auth.id,
				ifnull(bscore.score, 0) + kscore.score as score

			from author as auth
				inner join (
					select 
					auth.name,
					auth.id,
					ak.freq as score

					from author as auth
					inner join freqauthkeywords as ak on ak.auth_id = auth.id
					inner join freqkeywords as kw on kw.id = ak.key_id

					where kw.keyword in ("""+x+""")

					group by auth.name, auth.id, kw.id

					order by -ak.freq
					limit 1000
				) as kscore on kscore.id = auth.id
				left outer join (
					select 
					auth.name,
					auth.id,
					ab.freq * 10 as score

					from author as auth
					inner join freqauthbigrams as ab on ab.auth_id = auth.id
					inner join freqbigrams as bi on bi.id = ab.bigram_id

					where bi.bigram in ("""+y+""")

					group by auth.name, auth.id, bi.id

					order by -ab.freq
					limit 1000
				) as bscore on bscore.id = auth.id

			group by auth.name, auth.id

			order by -(ifnull(bscore.score, 0) + kscore.score)

			limit 100"""
	# print query
	cursor.execute(query)
	return dictfetchall(cursor)

# END SEARCH_FOR_KEYWORDS

# BEGIN AUTHOR INFO BY ID QUERIES

def get_author_papers_by_id(id):
	cursor = connection.cursor()

	query = '''
			select 
				paper.title, 
				paper.id as paper_id,
				paper.year,
				auth.id as auth_id 
			from paper as paper
				inner join authorship as ak on ak.id2 = paper.id
				inner join author as auth on ak.id1 = auth.id
			where auth.id = '''+ id +'''

			order by -year

			limit 10
			'''
	# print query
	cursor.execute(query)
	return dictfetchall(cursor)

def get_author_keywords_by_id(id):
	cursor = connection.cursor()

	query = '''
			select 
				keyword,
				keyword.id as key_id,
				ak.freq as freq,
				auth.name, 
				auth_id 
			from freqkeywords as keyword
				inner join freqauthkeywords as ak on ak.key_id = keyword.id
				inner join author as auth on ak.auth_id = auth.id
			where auth.id = '''+ id +'''
			and length(keyword) > 2

			#group by keyword

			order by -ak.freq

			limit 10
			'''
	# print query
	cursor.execute(query)
	return dictfetchall(cursor)

def get_author_bigrams_by_id(id):
	cursor = connection.cursor()

	query = '''
			select 
				bigram,
				bigram.id as bigram_id,
				ab.freq as freq,
				auth.name, 
				auth_id 
			from freqbigrams as bigram
				inner join freqauthbigrams as ab on ab.bigram_id = bigram.id
				inner join author as auth on ab.auth_id = auth.id
			where auth.id = '''+ id +'''
			and length(bigram) > 5

			#group by bigram, auth_id

			order by -ab.freq

			limit 10
			'''
	# print query
	cursor.execute(query)
	return dictfetchall(cursor)
# END AUTHOR INFO BY ID QUERIES