update keyword
join (
	select
		ak.key_id,
		max(ak.freq) as freq
	from authkeyword as ak
	group by ak.key_id
) as maxs on maxs.key_id = keyword.id
set keyword.max_freq = maxs.freq
where keyword.id = maxs.keyword_id