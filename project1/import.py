import csv, json

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


with open('database_url.json') as f:
    DATABASE_URL = json.load(f)


engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))


# set up variables for testing
TABLE = "books"
FILE = "books.csv"


with open(FILE, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            print(f"Attempting to add {row['title']}...")
            db.execute(f"INSERT INTO {TABLE} VALUES (:isbn, :title, :author, :year)", {"isbn": row['isbn'], "title": row['title'], "author": row['author'], "year": row['year']})
        except Exception as e:
            print(f"Error adding {row['title']} to database.\nError: {e}\n")
            raise Exception

    db.commit()
    print("Done!")
