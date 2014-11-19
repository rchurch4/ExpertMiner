update authkeyword
join (
select
	ak.key_id,
	ak.auth_id,
	CAST(ak.freq as decimal(10,6)) / CAST(kw.max_freq as decimal(10,6)) as norm
from authkeyword as ak
inner join keyword as kw on kw.id = ak.key_id
) as norms on norms.key_id = authkeyword.key_id and norms.auth_id = authkeyword.auth_id
set authkeyword.norm = norms.norm

