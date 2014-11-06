insert into freqauthkeywords

select auth_id, key_id, ak.freq
from authkeyword as ak
inner join keyword as kw on kw.id = ak.key_id
where kw.freq > 4 and length(kw.keyword) > 2