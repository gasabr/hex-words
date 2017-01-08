# hex words

a small python script which generates all the possible words from letters: a, b, c, d, e, f. It just creates all permutations and checks them with enchant dictionary.

By default dictionary will be loaded from `hex-dictionary.json`.

### Available features

#### Find a word from given decimal form

```bash
$./hex-words.py --number=2989
	BAD ( 2989 ) --
 of poor quality or a low standard.
```

#### Find a definition and number representation of the word

```bash
$./hex-words.py --word=bad
 	BAD ( 2989 ) --
of poor quality or a low standard.
```

#### Find all words given length

```bash
$./hex-words.py --length=4
# list of words
```

i have not found a word with length 8, so 7 is maximum and 2 is minimum.