insert into freqauthbigrams

select auth_id, bigram_id, ab.freq
from authbigram as ab
inner join bigram as bi on bi.id = ab.bigram_id and bi.freq > 6 and length(bi.bigram) > 5
group by auth_id, bigram_id