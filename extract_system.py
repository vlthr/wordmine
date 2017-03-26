import sqlite3
import sys

db = sqlite3.connect('words.db')

for file_path in sys.argv[1:]:
    dict_name = file_path.split("/")[-1]
    with open(file_path) as f:
        for word in f.readlines():
            word = word.strip().lower()
            db.execute('INSERT OR IGNORE INTO Words(word, language_tag) VALUES (?, ?)', (word, dict_name))

db.commit()
db.close()
