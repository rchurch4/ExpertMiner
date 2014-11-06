insert into freqbigrams

select *

from bigram

where bigram.freq > 6 and length(bigram.bigram) > 5