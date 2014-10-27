from stemming.porter2 import stem


query = 'On Honesty in Sovereign Information Sharing'

query_list = query.split()

# CHANGE TO STEMMED WORDS
stemmed_query_list = []
for x in query_list:
	stemmed_query_list.append(stem(x))

# CREATE BIGRAMS OUT OF INDIVIDUAL TERMS
stemmed_bigram_list = []
i = 0
while i < len(stemmed_query_list)-1:
	stemmed_bigram_list.append(stemmed_query_list[i]+stemmed_query_list[i+1])
	i+=1

print 'Query List: '+str(stemmed_query_list)
print 'Bigram List: '+str(stemmed_bigram_list)