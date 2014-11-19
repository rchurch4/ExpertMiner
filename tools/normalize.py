import MySQLdb as mdb
import sys

try:
	con = mdb.connect('localhost', 'root', '', 'dblp');
	cur = con.cursor()

except mdb.Error, e:
  
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
	
finally:    
	cur.close()
		
	if con:    
		con.commit()
		con.close()
