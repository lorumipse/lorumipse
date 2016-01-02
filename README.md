# Lórum ipse

```
gzcat resource/sg3_nom_acc_sentences_xaa.txt.gz | langmodel/gibberize.py | less 
```

replaces content words in input sentences with gibberish word forms. The input should be formatted as follows:

\# _sentence_number_

_word_ <TAB> _lemma_ <TAB> _analysis_

_word_ <TAB> _lemma_ <TAB> _analysis_

...

\# _sentence_number_

...

```
basic_sentence_demo.py
```

generates 1000 sentence with ```definite_article subject verb indefinite_article adjective object``` structure

```
phonmodel.py <list-of-existing-stems
```

This will create a trigram model based on the input character sequences and output 100 generated stems

![lórum](http://konyvmanufaktura.hu/wp-content/uploads/2012/04/magyarkartya.jpg)
