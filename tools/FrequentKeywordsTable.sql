insert into freqkeywords

select *

from keyword

where keyword.freq > 3 and length(keyword.keyword) > 2