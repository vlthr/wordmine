import sqlite3
import sys
import re
pattern = r"<w[^>]*>(\w+)</w>"

db = sqlite3.connect('words.db')

for file_path in sys.argv[1:]:
    with open(file_path) as f:
        for match in re.findall(pattern, f.read()):
            word = match
            db.execute('INSERT OR IGNORE INTO Words(word, language_tag) VALUES (?, ?)', (word, "icelandic"))

db.commit()
db.close()
