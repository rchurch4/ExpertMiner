import re

def read_top():
	f = open('venues.txt', 'r')
	lines = f.readlines()
	journals = []
	confs = []

	for i in range(0, 100):
		temp = lines[i].strip()
		tokens = temp.split(' - ')
		if len(tokens) > 1:
			acro = tokens[0]
			full = tokens[1]
			journals.append([acro, full])
		else:
			full = tokens[0]
			journals.append([None, full])

	for i in range(0, 100):
		temp = lines[i + 100].strip()
		tokens = temp.split(' - ')
		if len(tokens) > 1:
			acro = tokens[0]
			full = tokens[1]
			confs.append([acro, full])
		else:
			full = tokens[0]
			confs.append([None, full])

	return(journals, confs)


def match(text, journals, confs, journals_count, confs_count):
	text = text.strip()
	# first try if something matches either the acro or the full name
	for i in range(0, 100):
		[acro, full] = journals[i]
		if (acro is not None and text.lower() == acro.lower()) or text.lower() == full.lower():
			journals_count[i] = journals_count[i] + 1
			return journals[i]
	for i in range(0, 100):
		[acro, full] = confs[i]
		if (acro is not None and text.lower() == acro.lower()) or text.lower() == full.lower():
			confs_count[i] = confs_count[i] + 1
			return confs[i]
	return None

def is_well_known(text, journals, confs):
	text = text.strip()
	# first try if something matches either the acro or the full name
	for i in range(0, 100):
		[acro, full] = journals[i]
		if (acro is not None and acro.lower() in text.lower()) or full.lower() in text.lower():
			return True
	for i in range(0, 100):
		[acro, full] = confs[i]
		if (acro is not None and acro.lower() in text.lower()) or full.lower() in text.lower():
			return True
	return False

# def main():
# 	(journals, confs) = read_top()
# 	# setting up the experiment
# 	journals_count = [0] * 100
# 	confs_count = [0] * 100

# 	# reading the file searching for tokens to try
# 	line_count = 0
# 	f = open('../dblp.xml', 'r')
# 	not_matched = 0
# 	for line in f:
# 		line_count = line_count + 1
# 		if line_count % 100000 == 0:
# 			print line_count

# 		# checking if it contains a venue name
# 		m = re.search('<journal>.*?</journal>', line.strip().lower())
# 		if m is not None:
# 			token = m.group(0)
# 			text = token[9:(len(token) - 10)]
# 		else:
# 			m = re.search('key=\"conf/.*?/', line.strip().lower())
# 			if m is not None:
# 				token = m.group(0)
# 				text = token[10:(len(token) - 1)]
# 			else:
# 				m = re.search('<booktitle>.*?</booktitle>', line.strip().lower())
# 				if m is not None:
# 					token = m.group(0)
# 					text = token[11:(len(token) - 12)]
# 				else:
# 					m = re.search('<crossref>conf/.*?/', line.strip().lower())
# 					if m is not None:
# 						token = m.group(0)
# 						text = token[15:(len(token) - 1)]

# 		if m is not None:
# 			result = match(text, journals, confs, journals_count, confs_count)
# 			if result is not None:
# 				if result[0] is not None:
# 					print text + ' matched ' + result[0] + ' - ' + result[1]
# 				else:
# 					print text + ' matched ' + result[1]
# 			else:
# 				not_matched = not_matched + 1

# 	# printing final results
# 	print journals_count
# 	print confs_count

# if __name__ == "__main__":
# 	main()
