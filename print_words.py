import sqlite3
import re
import unicodedata as ud
from collections import Counter

db = sqlite3.connect('words.db')

words = db.execute("select word from Words where length(word) = 5 OR length(word) == 6")

latin_out = (open("words-latin.txt", "w+"), Counter())
all_out = (open("words-all.txt", "w+"), Counter())
ascii_out = (open("words-ascii.txt", "w+"), Counter())

def write(out, word):
    f, counter = out
    f.write(word)
    f.write('\n')
    for c in word.lower():
        counter[c] += 1
latin_letters= {}
def is_latin(uchr):
    try: return latin_letters[uchr]
    except KeyError:
         return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))

def only_roman_chars(unistr):
    return all(is_latin(uchr)
           for uchr in unistr) # isalpha suggested by John Machin

ascii_chars = set("abcdefghijklmnopqrstuvwxyz")
def only_ascii_chars(unistr):
    return all((uchr in ascii_chars)
           for uchr in unistr)

for w in words:
    word = w[0].strip().lower()
    if re.search(r"[\d.,' ]", word): continue
    if len(word) != 5: continue
    write(all_out, word)
    if only_ascii_chars(word):
        write(ascii_out, word)
    if only_roman_chars(word):
        write(latin_out, word)

for f, counter in (ascii_out, latin_out, all_out):
    f.close()
    length = len(counter)
    print("Total count: {} characters".format(length))
    if length < 200:
        print(counter)
    print()
