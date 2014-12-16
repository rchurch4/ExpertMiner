	##################################################
	#												 #
	#				  GENERAL NOTES					 #
	#												 #
	##################################################

'''
	This is the updated xmlparser that should parse dblp.xml using the .dtd file
	and give papers with their title, year, conference, and authors
	as well as authors with connections to their papers

'''


import MySQLdb as mdb
import sys
import re
import xml.etree.ElementTree as ET

	##################################################
	#												 #
	#		  FOR CLEANING Conference Names			 #
	#												 #
	##################################################

def clean_conference(conf):
	if conf == '' or len(conf) < 1:
		return ''
	# if '/' in conf:
	# 	conf = conf[conf.index('/')+1:]
	#print conf
	return conf.lower()
	#ask if any part of the conf is a well-known conference name


	##################################################
	#												 #
	#			   BEGIN ACTUAL CODE				 #
	#												 #
	##################################################

try:

	##################################################
	#												 #
	#			   CONNECT AND RESET DB				 #
	#												 #
	##################################################

	print 'Starting Connection'
	con = mdb.connect('localhost', 'root', '', 'dblp');

	print 'Connected'
	cur = con.cursor()
	cur.execute('drop table if exists `author`;')
	cur.execute('create table `author` (`id` int(11) NOT NULL, `name` text, primary key (`id`));')
	cur.execute('drop table if exists `paper`;')
	cur.execute('create table `paper` (`id` int(11) NOT NULL, `title` text, `year` int(4), `conf` text, primary key (`id`));')
	cur.execute('drop table if exists `authorship`;')
	cur.execute('create table `authorship` (`id` int(11) NOT NULL, `id1` int(11) NOT NULL, `id2` int(11) NOT NULL, primary key (`id`));')
	con.commit()
	con.close()

	# print 'DBs recreated'

	##################################################
	#												 #
	#				TESTING VARIABLES				 #
	#												 #
	##################################################
	
	testing = False # set to True to test on max_lines of xml
	max_lines = 10000 # when testing is true, this is how many lines of xml you will test on 
	paper_count = 0 # keeps track of number of papers processed. ! DO NOT ALTER !
	total_lines = 0 # keeps track of number of lines run. ! DO NOT ALTER !

	##################################################
	#												 #
	#			  VARIABLES FOR CREATION			 #
	#												 #
	##################################################

	max_paper_id = 1000001
	max_auth_id = 1000001
	max_ship_id = 1000001
	authors = {}
	regex = re.compile('[^a-zA-Z\s]')
	final_auth = ''

	##################################################
	#												 #
	#			   PARSING AND POPULATING			 #
	#												 #
	##################################################

	con = mdb.connect('localhost', 'root', '', 'dblp');	
	cur = con.cursor()
	print 'Starting Parse'

	tree = ET.parse('dblp.xml')

	root = tree.getroot() 

	entry_types = ('inproceedings', 'incollections', 'article', 'journal')

	for entry_type in entry_types:
		for ip in root.iter(entry_type):
			if (paper_count % 10000 == 0):
				print paper_count

			paper = ip.find('title')
			if paper != None:
				paper = regex.sub(' ', paper.text)
			else:
				paper = 'no title'
			#print paper
			year = ip.find('year')
			if year != None:
				year = year.text
			else:
				year = 1900
			#print year
			conf = ip.find('crossref')
			if conf == None:
				conf = ip.find('series')
				if conf == None:
					conf = ip.find('journal')
					if conf == None:
						conf = ip.find('booktitle')
			if conf != None:
				conf = clean_conference(conf.text)
			else:
				conf = 'none'
			paper_count += 1

			author_list = ip.findall('author')
			for auth in author_list:
				auth = regex.sub('', auth.text)
				#print auth
				if auth not in authors:
					authors[auth] = max_auth_id
					# ADD AUTHOR TO DB
					cur.execute('insert into author values (' + str(max_auth_id) + ', "' + str(auth) + '");')
					if auth == 'Behzad Golshan':
						print str(max_auth_id) + ' ' + auth
					max_auth_id += 1
				auth_id = authors[auth]
				# ADD AUTHORSHIP TO DB
				cur.execute('insert into authorship values (' + str(max_ship_id) + ', ' + str(auth_id) + ', ' + str(max_paper_id) + ');')
				if auth == 'Behzad Golshan':
					print str(max_ship_id) + ' ' + str(auth_id) + ' ' + str(max_paper_id)
				max_ship_id +=1

			# ADD PAPER TO DB
			if paper != '':
				#pass
				cur.execute('insert into paper values (' + str(max_paper_id) + ', "' + str(paper) + '", '+ str(year) +', "' + str(conf) + '");')
			max_paper_id += 1

except mdb.Error, e:
  
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
	
finally:    
	cur.close()

	print 'Papers: ' + str (paper_count)
	print 'Authors: ' + str (max_auth_id-1000001)
	print
	print 'Done ' + final_auth

	if con:    
		con.commit()
		con.close()