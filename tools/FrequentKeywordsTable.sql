insert into freqkeywords

select *

from keyword

where keyword.freq > 3