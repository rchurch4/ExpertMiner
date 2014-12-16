# maxcoveragev2.py
#
# takes in: 
#	list of format (id, name, covered, totalscore, score1, score2, ... scoreN)
# 	value for covering a term (0-1)
#	tuning variable (0-1)
#	k for the number of people on the team
#
# returns:
#	team based on greedy coverage algorithm
#
# written by Rob Churchill
# rchurch4@bu.edu

import copy as cp

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
			i[3] -= ((1-x)*c + x*i[index])

	#sets term to true
	boolean_list[index] = True

	return l

def max_coverage (m, c, x, k):
	l = cp.deepcopy(m)

	boolean_list = [False] * (len(l[0]))
	boolean_list[0] = True
	boolean_list[1] = True
	boolean_list[2] = True
	boolean_list[3] = True

	#compute total
	for i in l:
		i[3] = x*i[3] + (1-x)*c*i[2]
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
				if next_guy[index] > 0:
					remove_term(l, c, index, boolean_list)
				index +=1
		else:
		 	l.remove(next_guy)

	return team, compute_score(team, c, x)
