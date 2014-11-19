# frequency_tables.py

# takes giant tables and cuts them off at a frequency lower than 7

import MySQLdb as mdb
import sys

try:
	print 'Starting Connection'
	con = mdb.connect('localhost', 'root', '', 'dblp');

	cur = con.cursor()
	cur.execute('drop table if exists `freqkeywords`;')
	cur.execute('create table `freqkeywords` (`id` int(11) NOT NULL, `keyword` varchar(250), `freq` int(8) default 0, `max_freq` int(8) default 0,'
				'primary key (`id`), INDEX(keyword));')
	cur.execute('drop table if exists `freqauthkeywords`;')
	cur.execute('create table `freqauthkeywords` (`auth_id` int(11) NOT NULL,'
				'`key_id` int(11) NOT NULL, `freq` int(8) default 0, `norm` float(7,6) default 0,'
				'primary key(`auth_id`, `key_id`));')
	cur.execute('drop table if exists `freqauthbigrams`;')
	cur.execute('create table `freqauthbigrams` (`auth_id` int(11) NOT NULL,'
				'`bigram_id` int(11) NOT NULL, `freq` int(8) default 0, `norm` float(7,6) default 0,'
				'primary key(`auth_id`, `bigram_id`));')
	cur.execute('drop table if exists `freqbigrams`;')
	cur.execute('create table `freqbigrams` (`id` int(11) NOT NULL,'
				'`bigram` varchar(250), `freq` int(8) default 0, `max_freq` int(8) default 0, primary key(`id`), INDEX(bigram));')
	con.commit()

	print 'Creating freqauthbigrams'
	cur.execute('''
		insert into freqauthbigrams
		select auth_id, bigram_id, ab.freq, ab.norm
		from authbigram as ab
		inner join bigram as bi on bi.id = ab.bigram_id and bi.freq > 6 and length(bi.bigram) > 5
		group by auth_id, bigram_id;
		''')

	print 'Creating freqauthkeywords'
	cur.execute('''
		insert into freqauthkeywords
		select auth_id, key_id, ak.freq, ak.norm
		from authkeyword as ak
		inner join keyword as kw on kw.id = ak.key_id
		where kw.freq > 6 and length(kw.keyword) > 2;
		''')

	print 'Creating freqbigrams'
	cur.execute('''
		insert into freqbigrams
		select *
		from bigram
		where bigram.freq > 6 and length(bigram.bigram) > 5;
		''')

	print 'Creating freqkeywords'
	cur.execute('''
		insert into freqkeywords
		select *
		from keyword
		where keyword.freq > 6 and length(keyword.keyword) > 2;
		''')



except mdb.Error, e:
  
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)

finally:
	cur.close()
		
	if con:    
		con.commit()
		con.close()