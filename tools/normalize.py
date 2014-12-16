import MySQLdb as mdb
import sys

try:
	con = mdb.connect('localhost', 'root', '', 'dblp');
	cur = con.cursor()
	print 'Connected'

	# #add norm rows
	# cur.execute('alter table authbigram add norm float(7,6);')
	# cur.execute('alter table authkeyword add norm float(7,6);')
	# cur.execute('alter table freqauthbigrams add norm float(7,6);')
	# cur.execute('alter table freqauthkeywords add norm float(7,6);')
	# #add max frequency rows
	# cur.execute('alter table bigram add max_freq int(8);')
	# cur.execute('alter table keyword add max_freq int(8);')
	# cur.execute('alter table freqbigrams add max_freq int(8);')
	# cur.execute('alter table freqkeywords add max_freq int(8);')
	#compute max_frequencies
	print 'Starting'
	cur.execute('''update keyword
		join (
		select 
		ak.key_id,
		max(ak.freq) as freq
		from authkeyword as ak 
		group by ak.key_id
		) as maxs on maxs.key_id = keyword.id 
		set keyword.max_freq = maxs.freq 
		where keyword.id = maxs.key_id;
		''')
	print 'Max Frequency Keywords Found'
	cur.execute('''
		update bigram 
		join (
		select 
		ab.bigram_id,
		max(ab.freq) as freq
		from authbigram as ab 
		group by ab.bigram_id 
		) as maxs on maxs.bigram_id = bigram.id 
		set bigram.max_freq = maxs.freq 
		where bigram.id = maxs.bigram_id;
		''')
	print 'Max Frequency Bigrams Found'

	# con.commit()
	# con.close()
	# con = mdb.connect('localhost', 'root', '', 'dblp');
	# cur = con.cursor()

	print 'Starting Normalization'
	cur.execute(
		'''update authbigram 
		join ( 
		select 
		ab.bigram_id, 
		ab.auth_id, 
		CAST(ab.freq as decimal(10,6)) / CAST(bi.max_freq as decimal(10,6)) as norm 
		from authbigram as ab 
		inner join bigram as bi on bi.id = ab.bigram_id 
		) as norms on norms.bigram_id = authbigram.bigram_id and norms.auth_id = authbigram.auth_id 
		set authbigram.norm = norms.norm;'''
		)
	print 'Bigrams Normalized'
	cur.execute(
		'''update authkeyword 
		join ( 
		select 
		ak.key_id, 
		ak.auth_id, 
		CAST(ak.freq as decimal(10,6)) / CAST(kw.max_freq as decimal(10,6)) as norm 
		from authkeyword as ak 
		inner join keyword as kw on kw.id = ak.key_id 
		) as norms on norms.key_id = authkeyword.key_id and norms.auth_id = authkeyword.auth_id 
		set authkeyword.norm = norms.norm;'''
		)
	print 'Keywords Normalized'

	print 'Starting Score Cropping'
	cur.execute(
		'''update authbigram 
		set norm = 0 
		where norm < .1;'''
		)
	print 'Bigrams Cropped'
	cur.execute(
		'''update authkeyword 
		set norm = 0 
		where norm < .1;'''
		)
	print 'Keywords Cropped'

except mdb.Error, e:
  
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
	
finally:    
	cur.close()
		
	if con:    
		con.commit()
		con.close()
