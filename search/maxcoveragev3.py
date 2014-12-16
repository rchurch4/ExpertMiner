# maxcoveragev3.py
#
# takes in: 
#	list of format (id, name, covered, totalscore, score1, score2, ... scoreN)
# 	value for covering a term (0-1)
#	tuning variable (0-1)
#	k for the number of people on the team
#	min coverage value
#
# returns:
#	team based on greedy coverage algorithm
#
# written by Rob Churchill
# rchurch4@bu.edu

import copy as cp

def reset_scores(l, c, x, z, boolean_list):
	for i in l:
		index = 4
		i[3] = 0
		while index < len(i):
			if i[index] > z:
				i[3] += (i[index]*x + (1-x)*c)
			index += 1

	index = 4
	while index < len(boolean_list):
		boolean_list[index] = False
		index += 1

def compute_score(team, c, x, z):
	if len(team) > 0:
		team_score = [0] * (len(team[0])-3)
		for i in team:
			index = 4
			while index < len(i):
				if i[index] > z:
					team_score[0] += i[index]
					team_score[index-3] += i[index]
				index+=1
		return team_score
	else:
		return 0

def remove_term (l, c, x, index, boolean_list):
	#sets term to true
	boolean_list[index] = True

	#removes score of term already covered:
	for i in l:
		i[3] = 0
		idx = 4
		while idx < len(i):
			if boolean_list[idx] == False:
				if i[idx] != 0:
					i[3] += (1-x)*c + x*i[idx]
			idx+=1

def max_coverage (m, c, x, k, z):
	l = cp.deepcopy(m)

	if len(l) < 1:
		return [], 0
		
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
	if k == 0:
		while False in boolean_list:
			next_guy = [0,0,0,0]
			for i in l:
				if i[3] > next_guy[3]:
					index = 4
					while index < len(i):
						if i[index] > z:
							next_guy = i
						index += 1

			if len(next_guy) > 4:
				team.append(next_guy)
			else:
				print 'fuck'
				break

			l.remove(next_guy)
			index = 4
			while index < len(next_guy):
				if next_guy[index] > z:
					remove_term(l, c, x, index, boolean_list)
					if False not in boolean_list:
						break
				index +=1

	else:
		while len(team) < k:
			next_guy = [0,0,0,0]
			for i in l:
				if i[3] > next_guy[3]:
					index = 4
					while index < len(i):
						if i[index] > z:
							next_guy = i
						index += 1


			if len(next_guy) > 4:
				team.append(next_guy)
			else:
				print 'fuck'
				break

			if len(team) < k:
				if False in boolean_list:
					l.remove(next_guy)
					index = 4
					while index < len(next_guy):
						if next_guy[index] > z:
							remove_term(l, c, x, index, boolean_list)
							if False not in boolean_list:
								reset_scores(l, c, x, z, boolean_list)
						index +=1
				else:
					reset_scores(l, c, x, z, boolean_list)
			else:
			 	l.remove(next_guy)

	return team, compute_score(team, c, x, z)
