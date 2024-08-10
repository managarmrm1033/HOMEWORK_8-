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

def search_quotes():
    while True:
        query = input("Введіть ваш запит (name, tag, tags, exit): ")
        
        if ':' not in query:
            print("Неправильний формат запиту. Введіть у форматі 'команда:значення'.")
            continue
        
        command, value = query.split(':', 1)
        
        if command == "exit":
            break
        elif command == "name":
            author = Author.objects(fullname=value).first()
            if author:
                quotes = Quote.objects(author=author)
                for quote in quotes:
                    print(quote.quote)
            else:
                print("Автор не знайдений.")
        elif command == "tag":
            quotes = Quote.objects(tags=value)
            for quote in quotes:
                print(quote.quote)
        elif command == "tags":
            tags_list = value.split(',')
            quotes = Quote.objects(tags__in=tags_list)
            for quote in quotes:
                print(quote.quote)
        else:
            print("Невідома команда. Спробуйте ще раз.")

if __name__ == "__main__":
    search_quotes()
