import re

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

regex = re.compile('[^a-zA-Z\s]')

print remove_tags('<author>Giorgio Giacinto</author>')
print regex.sub('', remove_tags('<title>Intrusion Detection in Computer Networks by Multiple Classifier Systems.</title>'))
