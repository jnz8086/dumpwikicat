

This script dumps a list of a Wikimedia website category entries into a text file separated by lines.


#Usage

```
python ./dwc.py url file [filter] [-r]
   where: filter is a regular expression that discards entries when matched. (leave it like "" to bypass filtering)
          -r flag means that it recursively goes through the subcategories as well
```


e.g.
```
python ./dwc.py "https://en.wiktionary.org/wiki/Category:English_nouns" ./en-nouns.txt "^(Appendix\\:|User\\:|[*/\\!&$%-@()_+.]|\d)"
```

