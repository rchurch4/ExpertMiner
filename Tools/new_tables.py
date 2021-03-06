from stemming.porter2 import stem
import MySQLdb as mdb
import sys
import re
from nltk.corpus import stopwords

import find_venues as fv

try:
	print 'Starting'
	con = mdb.connect('localhost', 'root', '', 'dblp');
	print 'Connected'

	cur = con.cursor()
	cur.execute('drop table if exists `keyword`;')
	cur.execute('create table `keyword` (`id` int(11) NOT NULL, `keyword` varchar(250), `freq` int(8) default 0, `max_freq` int(8) default 0,'
				'primary key (`id`), INDEX(keyword));')
	cur.execute('drop table if exists `authkeyword`;')
	cur.execute('create table `authkeyword` (`auth_id` int(11) NOT NULL,'
				'`key_id` int(11) NOT NULL, `freq` int(8) default 0, `norm` float(7,6) default 0,'
				'primary key(`auth_id`, `key_id`));')
	cur.execute('drop table if exists `authbigram`;')
	cur.execute('create table `authbigram` (`auth_id` int(11) NOT NULL,'
				'`bigram_id` int(11) NOT NULL, `freq` int(8) default 0, `norm` float(7,6) default 0,'
				'primary key(`auth_id`, `bigram_id`));')
	cur.execute('drop table if exists `bigram`;')
	cur.execute('create table `bigram` (`id` int(11) NOT NULL,'
				'`bigram` varchar(250), `freq` int(8) default 0, `max_freq` int(8) default 0, primary key(`id`), INDEX(bigram));')
	con.commit()
	print 'Tables Recreated'

	cur.execute('select id1, title, conf from authorship join author on '
			'authorship.id1 = author.id join paper on authorship.id2'
			' = paper.id;')

	# TO RUN EVERYTHING AS IT SHOULD RUN, TAKE OUT LIMIT 100 ABOVE
	# TO TEST, ADD LIMIT 100 ABOVE

	rows = cur.fetchall()
	print len(rows)
	cur.close()
	cur = con.cursor()
	keywords = {}
	bigrams = {}

	max_id = 0
	max_bigram_id = 0
	paper = 0

	regex = re.compile('[^a-zA-Z]')
	stop = stopwords.words('english')

	read_venues = fv.read_top()
	journals = read_venues[0]
	confs = read_venues[1]

	for row in rows:
		paper = paper + 1
		if (paper % 1000 == 0):
			print (paper)
		author_id = row[0]
		title = row[1]
		tokens = title.split(' ');
		conf = row[2]
		multiplier = 1
		if fv.is_well_known(conf, journals, confs):
			multiplier = 10
	   # --------- for unigrams -----------------
		for token in tokens:
			stem_token = stem(regex.sub('', token)).lower()
			if stem_token not in stop and stem_token != '':
				if stem_token in keywords:
					keyword_id = keywords[stem_token]
					cur.execute('insert into authkeyword values (' + 
						str(author_id) + ', ' + str(keyword_id) + ', '+str(multiplier)+', 0) '
						'on duplicate key update freq = freq + '+str(multiplier)+';')
					cur.execute('update keyword set freq = freq+'+str(multiplier)+' where id = ' + str(keyword_id) +';')
				else:
					keyword_id = max_id
					keywords[stem_token] = max_id
					cur.execute('insert into authkeyword values (' +
						str(author_id) + ', ' + str(keyword_id) + ', '+str(multiplier)+', 0)'
						'on duplicate key update freq = freq + '+str(multiplier)+';')
					cur.execute('insert into keyword values (' + str(max_id) + 
						', \'' + stem_token + '\', '+str(multiplier)+', 1);')
					max_id = max_id + 1
		# --------- for bigrams -----------------
		for i in range(0, len(tokens) - 1):
			token1 = stem(regex.sub('', tokens[i])).lower()
			token2 = stem(regex.sub('', tokens[i+1])).lower()
			if token1 not in stop and token2 not in stop and token1 != '' and token2 != '':
				stem_token = token1 + '$' + token2
				if stem_token in bigrams:
					bigram_id = bigrams[stem_token]
					cur.execute('insert into authbigram values (' + 
						str(author_id) + ', ' + str(bigram_id) + ', '+str(multiplier)+', 0)'
						'on duplicate key update freq = freq + '+str(multiplier)+';')
					cur.execute('update bigram set freq = freq+'+str(multiplier)+' where id = ' + str(bigram_id) +';')
				else:
					bigram_id = max_bigram_id
					bigrams[stem_token] = max_bigram_id
					cur.execute('insert into authbigram values (' +
						str(author_id) + ', ' + str(bigram_id) + ', '+str(multiplier)+', 0)'
						'on duplicate key update freq = freq + '+str(multiplier)+';')
					cur.execute('insert into bigram values (' + str(max_bigram_id) + 
						', \'' + stem_token + '\', '+str(multiplier)+', 1);')
					max_bigram_id = max_bigram_id + 1

except mdb.Error, e:
  
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
	
finally:    
	cur.close()
		
	if con:    
		con.commit()
		con.close()
