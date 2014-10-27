import xml.etree.ElementTree as ET
import MySQLdb as mdb
import sys
import re

try:

	print 'Starting Connection'
	con = mdb.connect('localhost', 'root', '', 'dblp');

	print 'Connected'
	cur = con.cursor()
	cur.execute('drop table if exists `author`;')
	cur.execute('create table `author` (`id` int(11) NOT NULL, `name` text, primary key (`id`));')
	cur.execute('drop table if exists `paper`;')
	cur.execute('create table `paper` (`id` int(11) NOT NULL, `title` text, primary key (`id`));')
	cur.execute('drop table if exists `authorship`;')
	cur.execute('create table `authorship` (`id` int(11) NOT NULL, `id1` int(11) NOT NULL, `id2` int(11) NOT NULL, primary key (`id`));')
	con.commit()
	
	print 'DBs recreated'

	tree = ET.parse('dblp.xml')      
									 
	root = tree.getroot() 

	max_paper_id = 1
	max_auth_id = 1
	max_ship_id = 1
	authors = {}           

	regex = re.compile('[^a-zA-Z\s]')

	print 'Starting Parse'
									   
	for ip in root.iter('inproceedings'):  
			if (max_paper_id % 1000 == 0):
				print max_paper_id                           
			p = ip.find('title')
			paper_id = max_paper_id
			#print 'Paper:' + p.text
			cleaned = regex.sub('', p.text)
			cur.execute('insert into paper values (' + str(paper_id) + ', "' + str(cleaned) + '");')
			max_paper_id += 1
			a = ip.findall('author')                                                
			for auth in a:
				if auth not in authors:
					auth_id = max_auth_id           
					#print auth.text 
					cleaned = regex.sub('', auth.text)                                 
					cur.execute('insert into author values (' + str(auth_id) + ', "' + str(auth.text) + '");')
					max_auth_id += 1
					authors[auth.text] = auth_id

				auth_id = authors[auth.text]
				#add authorship
				cur.execute('insert into authorship values (' + str(max_ship_id) + ', ' + str(auth_id) + ', ' + str(paper_id) + ');')
				max_ship_id+=1

except mdb.Error, e:
  
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
	
finally:    
	cur.close()
		
	if con:    
		con.commit()
		con.close()