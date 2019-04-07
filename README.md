# Lórum ipse

## Running the text generator in browser

```
scripts/setup.sh
```

Prepares corpus chunks from the limited subset of Hungarian Webcorpus in build/text_template

```
scripts/run.sh
```

The browser should be pointed to http://localhost:9999

## Text generation with a template

```
gzcat resource/sg3_nom_acc_sentences_xaa.txt.gz | langmodel/gibberize.py | less 
```

replaces content words in input sentences with gibberish word forms. The input should be formatted as follows:

\# _sentence_number_

_word_ \<TAB> _lemma_ \<TAB> _analysis_

_word_ \<TAB> _lemma_ \<TAB> _analysis_

...

\# _sentence_number_

...

## Text generation with a fixed template

```
basic_sentence_demo.py
```

generates 1000 sentences with ```definite_article subject verb indefinite_article adjective object``` structure

## Generate random words based on training words 

```
phonmodel.py <list-of-existing-stems
```

This will create a trigram model based on the input character sequences and output 100 generated stems


## Filter sentences from webcorpus

```
gzcat webcorpus.tagged.gz | iconv -f latin2 -t utf8 | resource/webcorp-parse.py | resource/sentence-filter.py
```

![lórum](http://konyvmanufaktura.hu/wp-content/uploads/2012/04/magyarkartya.jpg)
