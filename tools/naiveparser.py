	##################################################
	#												 #
	#				  GENERAL NOTES					 #
	#												 #
	##################################################

'''
	This code is meant to run without use of python xml-parsing methods because
	the methods were used and took over 11 hours to run and it still came out missing
	over 99 percent of the entries expected.

	If it is possible that an inproceedings or incollections has no <title> tag, 
	then it is possible that there will be authorships that connect to no paper.
	This can be easily deduced in SQL after running the code by selecting all where
	paper_id does not correspond to a paper entry.

	TO RUN THIS IN TESTING MODE, REFER TO THE VARIABLE 'testing' IN THE 'TESTING VARIABLES'
	SECTION BELOW (approx. line 80).  Set 'testing' to false to run the code for the full file.

'''


import MySQLdb as mdb
import sys
import re

	##################################################
	#												 #
	#			  FOR CLEANING XML TAGS				 #
	#												 #
	##################################################

# thanks tgamblin on stackoverflow
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def remove_tags(x):
	if '<' in x and '>' in x:
		return x[x.index('>')+1:find_nth(x, '<', 2)]
	return x

	##################################################
	#												 #
	#			   BEGIN ACTUAL CODE				 #
	#												 #
	##################################################

try:
	xml = open('dblp.xml', 'r')

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
	cur.execute('create table `paper` (`id` int(11) NOT NULL, `title` text, primary key (`id`));')
	cur.execute('drop table if exists `authorship`;')
	cur.execute('create table `authorship` (`id` int(11) NOT NULL, `id1` int(11) NOT NULL, `id2` int(11) NOT NULL, primary key (`id`));')
	con.commit()
	con.close()

	print 'DBs recreated'

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

	max_paper_id = 1
	max_auth_id = 1
	max_ship_id = 1
	authors = {}
	regex = re.compile('[^a-zA-Z\s]')

	##################################################
	#												 #
	#			   PARSING AND POPULATING			 #
	#												 #
	##################################################

	con = mdb.connect('localhost', 'root', '', 'dblp');	
	cur = con.cursor()
	print 'Starting Parse'

	nextLine = xml.readline()
	# READ UNTIL END OF FILE
	while nextLine != '':
		# TESTING
		if total_lines > max_lines and testing:
			break
		# END TESTING

		# FIND ALL INPROCEEDINGS AND INCOLLECTIONS
		if nextLine.startswith('<in') or nextLine.startswith('<article'):
			paper_count += 1
			if (paper_count % 10000 == 0):
				print paper_count
			# TESTING
			if total_lines > max_lines and testing:
				break
			# END TESTING

			nextLine = xml.readline()

			# READ PAPER INFO UNTIL END OF CURRENT INPROCEEDINGS TAG
			while '</in' not in nextLine and '</art' not in nextLine:
				# TESTING
				if total_lines > max_lines and testing:
					break
				# END TESTING

				# IF REACHES EOF, BREAK
				if nextLine == '':
					break

				# IF AUTHOR, PROCESS AUTHOR
				if nextLine.startswith('<author>'):
					auth = remove_tags(nextLine)
					auth = regex.sub('', auth)
					if auth not in authors:
						authors[auth] = max_auth_id
						# ADD AUTHOR TO DB
						cur.execute('insert into author values (' + str(max_auth_id) + ', "' + str(auth) + '");')
						#print str(max_auth_id) + ' ' + auth
						max_auth_id += 1
					auth_id = authors[auth]
					# ADD AUTHORSHIP TO DB
					cur.execute('insert into authorship values (' + str(max_ship_id) + ', ' + str(auth_id) + ', ' + str(max_paper_id) + ');')
					#print str(max_ship_id) + ' ' + str(auth_id) + ' ' + str(max_paper_id)
					max_ship_id +=1

				# IF TITLE, PROCESS PAPER
				if nextLine.startswith('<title>'):
					paper = remove_tags(nextLine)
					paper = regex.sub('', paper)
					#print str(max_paper_id) + ' ' + paper
					# ADD PAPER TO DB
					cur.execute('insert into paper values (' + str(max_paper_id) + ', "' + str(paper) + '");')

				nextLine = xml.readline()
				total_lines +=1
			max_paper_id += 1
			nextLine = xml.readline()
			total_lines +=1
		nextLine = xml.readline()
		total_lines +=1

except mdb.Error, e:
  
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
	
finally:    
	cur.close()

	print paper_count
	print 'Done'

	if con:    
		con.commit()
		con.close()