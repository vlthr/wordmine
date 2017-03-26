import sqlite3
import sys

db = sqlite3.connect('words.db')

for file_path in sys.argv[1:]:
    with open(file_path) as f:
        for line in f.readlines():
            if line.startswith("#"):  continue
            line_parts = line.split()
            word = " ".join(line_parts[2:])
            tag, _ = line_parts[1].split(":")
            db.execute('INSERT OR IGNORE INTO Words(word, language_tag) VALUES (?, ?)', (word, tag))

db.commit()
db.close()
