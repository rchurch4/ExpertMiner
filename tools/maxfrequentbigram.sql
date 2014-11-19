update bigram
join (
	select
		ab.bigram_id,
		max(ab.freq) as freq
	from authbigram as ab
	group by ab.bigram_id
) as maxs on maxs.bigram_id = bigram.id
set bigram.max_freq = maxs.freq
where bigram.id = maxs.bigram_id