import json
from mongoengine import connect
from models import Author, Quote
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

connection_string = f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority"
connect(host=connection_string, ssl=True)

def load_authors():
    with open('authors.json', 'r', encoding='utf-8') as file:
        authors = json.load(file)
        for author_data in authors:
            author = Author(**author_data)
            author.save()

def load_quotes():
    with open('quotes.json', 'r', encoding='utf-8') as file:
        quotes = json.load(file)
        for quote_data in quotes:
            author_name = quote_data.pop('author')
            author = Author.objects(fullname=author_name).first()  # Виправлено на .objects замість .object
            if author:
                quote = Quote(author=author, **quote_data)
                quote.save()

if __name__ == "__main__":
    load_authors()
    load_quotes()