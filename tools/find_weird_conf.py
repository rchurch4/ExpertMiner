def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def find_bad_line(x):
	if find_nth(x, '/', 3) != -1:
		return True
	return False

testing = False # set to True to test on max_lines of xml
max_lines = 10000 # when testing is true, this is how many lines of xml you will test on 
paper_count = 0 # keeps track of number of papers processed. ! DO NOT ALTER !
total_lines = 0 # keeps track of number of lines run. ! DO NOT ALTER !

xml = open('dblp.xml', 'r')

nextLine = xml.readline()

while nextLine != '':
	if 'booktitle' in nextLine:
		if find_bad_line(nextLine):
			print nextLine
	nextLine = xml.readline()