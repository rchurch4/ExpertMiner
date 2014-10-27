# ampreplace
# replaces ampersands with &amp; for xml parsing purposes
# takes in a file, outputs an updated file

sourcename = 'dblp.xml'
outputname = 'good.xml'

input_file = open (sourcename, 'r')
output_file = open (outputname, 'w')

x = input_file.readline()

while x != '':
	x = x.replace('&amp;', '&')
	x = x.replace('&', '&amp;')
	output_file.write(x)
	x = input_file.readline()