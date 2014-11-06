insert into freqkeywords

select *

from keyword

where keyword.freq > 6 and length(keyword.keyword) > 2