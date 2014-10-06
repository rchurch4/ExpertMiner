from django.db import connection

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def get_first_100_authors ():
	cursor = connection.cursor()

	cursor.execute('select author.name from author limit 100')
	return dictfetchall(cursor)

def search_for_author (name):
	cursor = connection.cursor()

	query = "select author.name from author where author.name like '%" + name + "%' limit 100"

	cursor.execute(query)
	return dictfetchall(cursor)

def search_for_keywords (keys):
	cursor = connection.cursor()

	x = ""
	for k in keys:
		x += '\'' + k + '\', '
	x = x[:len(x)-2]
	print x
	print

	query = "select distinct auth.name from author as auth inner join authkeyword as ak on ak.auth_id = auth.id inner join keyword on keyword.id = ak.key_id where keyword.keyword in ("+ x +") limit 100"
	print query
	cursor.execute(query)
	return dictfetchall(cursor)