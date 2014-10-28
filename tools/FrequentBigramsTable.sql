insert into freqbigrams

select *

from bigram

where bigram.freq > 3