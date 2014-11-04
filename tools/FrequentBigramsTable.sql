insert into freqbigrams

select *

from bigram

where bigram.freq > 3 and length(bigram.bigram) > 5