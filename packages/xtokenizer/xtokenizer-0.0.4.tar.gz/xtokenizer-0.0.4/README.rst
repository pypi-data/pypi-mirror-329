Usage Sample
''''''''''''

.. code:: python

        from xtokenizer import Tokenizer

        tokenizer = Tokenizer.from_texts(texts, min_freq=5)
        sent = 'I love you'
        tokens = tokenizer.encode(sent, max_length=6)
        # [101, 66, 88, 99, 102, 0]
        sent = tokenizer.decode(tokens)
        # ['<BOS>', 'I', 'love', 'you', '<EOS>', '<PAD>']
