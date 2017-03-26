import sqlite3
import re
import unicodedata as ud
from collections import Counter

db = sqlite3.connect('words.db')

words = db.execute("select word from Words where length(word) = 5")

latin_letters= {}
def is_latin(uchr):
    try: return latin_letters[uchr]
    except KeyError:
         return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))

def only_roman_chars(unistr):
    return all(is_latin(uchr)
           for uchr in unistr
           if uchr.isalpha()) # isalpha suggested by John Machin


char_counter = Counter()
word_set = set()
for w in words:
    word = w[0].strip().lower()
    if re.search(r"[\d.,' ]", word): continue
    if len(word) == 5 and only_roman_chars(word):
        word_set.add(word)
        for c in word.lower():
            char_counter[c] += 1

# print(char_counter)
# print(len(char_counter.elements))

for w in word_set:
    print(w)

# for w in latin_letters:
#     print(w)
