update authbigram
join (
select
	ab.bigram_id,
	ab.auth_id,
	CAST(ab.freq as decimal(10,6)) / CAST(bi.max_freq as decimal(10,6)) as norm
from authbigram as ab
inner join bigram as bi on bi.id = ab.bigram_id
) as norms on norms.bigram_id = authbigram.bigram_id and norms.auth_id = authbigram.auth_id
set authbigram.norm = norms.norm

