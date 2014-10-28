insert into freqauthbigrams

select auth_id, bigram_id, ab.freq
from authbigram as ab
inner join bigram as bi on bi.id = ab.bigram_id
where bi.freq > 3