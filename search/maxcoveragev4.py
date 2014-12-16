# maxcoveragev4.py
#
# this version searches for those with the most total coverage, not the best score in a category
#
# takes in: 
#	list of format (id, name, covered, totalscore, score1, score2, ... scoreN)
# 	min value to be considered an expert
#	coverage value that team must attain to be considered covering a term
#
# returns:
#	team based on greedy coverage algorithm
#
# written by Rob Churchill
# rchurch4@bu.edu

import copy as cp

def compute_score(team, alpha):
	if len(team) > 0:
		team_score = [0] * (len(team[0])-3)
		for i in team:
			index = 4
			while index < len(i):
				if i[index] > alpha:
					team_score[0] += i[index]
					team_score[index-3] += i[index]
				index+=1
		return team_score
	else:
		return 0

def max_coverage (m, alpha, omega):
	l = cp.deepcopy(m)

	#compute total
	team = []

	if len(l) < 1:
		return team, 0

	team_coverage = [0] * len(l[0])
	team_coverage[0] = omega
	team_coverage[1] = omega
	team_coverage[2] = omega
	team_coverage[3] = 0

	while team_coverage[3] < omega:
		next_guy = [0,0,0,0]
		for i in l:
			i[3] = 0
			index = 4
			while index < len(i):
				if i[index] > alpha:
					i[3] += max(0, min(max(0, omega - team_coverage[index]), i[index]))
				index += 1
			
			if i[3] > next_guy[3]:
				next_guy = i

		if len(next_guy) > 4:
			team.append(next_guy)
		else:
			print 'fuck'
			break

		l.remove(next_guy)
		covered = True
		index = 4
		while index < len(next_guy):
			if next_guy[index] > alpha:
				team_coverage[index] += next_guy[index]
			if team_coverage[index] < omega:
				covered = False
			index +=1
		if covered:
			team_coverage[3] = omega

	return team, compute_score(team, alpha)
