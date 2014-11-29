# maxcoverage.py
#
# takes in: 
#	list of format (id, name, covered, totalscore, score1, score2, ... scoreN)
# 	value for covering a term (0-1)
#	multiplier for term score (0-2)
#	k for the number of people on the team
#
# returns:
#	team based on greedy coverage algorithm
#
# written by Rob Churchill
# rchurch4@bu.edu

# def find_low_score(l, team, boolean_list):
# 	if False not in boolean_list:
# 		return 0

# 	team_score = [0] * len(l[0])
# 	for t in team:
# 		index = 4
# 		while index < len(t):
# 			team_score[index] += t[index]
# 			index+=1

# 	low_score = 10000
# 	low_score_index = 0
# 	index = 4
# 	while index < len(team_score):
# 		if team_score[index] < low_score:
# 			low_score = team_score[index]
# 			low_score_index = index
# 		index += 1
# 	return low_score_index

# def reset_scores(l, c, x, team):
# 	for i in l:
# 		in_team = False
# 		for t in team:
# 			if t[0] == i[0]:
# 				in_team == True
# 		if in_team == False:
# 			index = 4
# 			while index < len(i):
# 				if i[index] != 0:
# 					i[3] += (i[index]*x + c)
# 				index += 1

def compute_score(team, c, x):
	team_score = [0] * (len(team[0])-3)
	for i in team:
		index = 4
		while index < len(i):
			team_score[0] += i[index]
			team_score[index-3] += i[index]
			index+=1

	return team_score

def remove_term (l, c, index, boolean_list):
	#removes score of term already covered:
	for i in l:
		if i[index] != 0:
			i[3] -= (c + i[index])

	#sets term to true
	boolean_list[index] = True

	return l

def max_coverage (l, c, x, k):
	boolean_list = [False] * (len(l[0]))
	boolean_list[0] = True
	boolean_list[1] = True
	boolean_list[2] = True
	boolean_list[3] = True

	#compute total
	for i in l:
		i[3] = x*i[3] + c*i[2]
	team = []

	#pick team

	while len(team) < k:
		next_guy = [0,0,0,0]
		for i in l:
			if i[3] > next_guy[3]:
				next_guy = i

		team.append(next_guy)

		if len(team) < k and False not in boolean_list:
			l.remove(next_guy)
			index = 4
			while index < len(next_guy):
				remove_term(l, c, index, boolean_list)
				index +=1
		else:
		 	l.remove(next_guy)

	return team, compute_score(team, c, x)
