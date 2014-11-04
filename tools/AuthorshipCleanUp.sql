insert into tempauthorship
select ap.id, ap.id1, ap.id2
from authorship as ap
inner join paper as p on ap.id2 = p.id