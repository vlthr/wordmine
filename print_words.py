import sqlite3
import re
import unicodedata as ud
from collections import Counter

db = sqlite3.connect('words.db')

words = db.execute("select word from Words where length(word) = 5 OR length(word) == 6")

latin_out = (open("words-latin.txt", "w+"), set(), Counter())
all_out = (open("words-all.txt", "w+"), set(), Counter())
ascii_out = (open("words-ascii.txt", "w+"), set(), Counter())

def add(out, word):
    f, s, counter = out
    s.add(word)

def write(out, word):
    f, s, counter = out
    f.write(word)
    f.write("\n")
    for c in word:
        counter[c] += 1

latin_letters= {}
def is_latin(uchr):
    try: return uchr.isalpha() and latin_letters[uchr]
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
    add(all_out, word)
    if only_ascii_chars(word):
        add(ascii_out, word)
    if only_roman_chars(word):
        add(latin_out, word)

for f, s, counter in (ascii_out, latin_out, all_out):
    for w in s:
        write((f, s, counter), w)
    f.close()

for f, s, counter in (ascii_out, latin_out, all_out):
    length = len(counter)
    print("Total count: {} characters".format(length))
    if length < 200:
        print(counter)
    print()
