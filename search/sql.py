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