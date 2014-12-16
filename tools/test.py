def clean_conference(conf):
	if '/' in conf:
		conf = conf[conf.index('/')+1:]
	return conf.lower()

print clean_conference('sigmod/kdd')
