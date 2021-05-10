https://radimrehurek.com/gensim/

```python
from gensim.models.word2vec import LineSentence
from gensim.models import word2vec
from multiprocessing import cpu_count
import numpy as np
import os
from processer import ChipProcessor
from itertools import chain

processer = ChipProcessor()

train_sentences = word2vec.LineSentence(processer.train_seg)
val_sentences = word2vec.LineSentence(processer.val_seg)


model = word2vec.Word2Vec(train_sentences,
                          workers=cpu_count(),
                          min_count=5,
                          sg=1,  # skip-gram
                          size=100,
                          iter=10,
                          seed=1)


vocab = model.wv.index2word

embedding = model.wv.vectors
print(len(vocab), embedding.shape)
```

