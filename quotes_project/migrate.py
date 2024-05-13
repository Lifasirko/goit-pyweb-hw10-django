import os

import django
from mongoengine import connect, Document, StringField, ListField, ReferenceField

# Налаштування середовища Django перед викликом django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes_project.settings')

# Ініціалізація Django
django.setup()

# Імпорт Django моделей після налаштування середовища
try:
    from quotes.models import Author as DjangoAuthor, Quote as DjangoQuote
except ImportError as e:
    print(f"Error importing models: {e}")
    exit(1)

# Конфігурація MongoDB через configparser
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')

# Підключення до MongoDB
connect(
    host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@clustertest.s6h4lrj.mongodb.net/?retryWrites=true&w=majority&appName=ClusterTest",
    ssl=True)


# Визначення MongoDB моделей
class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)


# Міграція авторів
def migrate_authors():
    print(f"Migrating author")
    for mongo_author in Author.objects:
        print(f"Migrating author: {mongo_author.fullname}")
        django_author, created = DjangoAuthor.objects.get_or_create(
            name=mongo_author.fullname,
            defaults={
                'birth_date': mongo_author.born_date,
                'bio': mongo_author.description
            }
        )


# Міграція цитат
def migrate_quotes():
    for mongo_quote in Quote.objects:
        print(f"Migrating quote: {mongo_quote.quote}")
        try:
            django_author = DjangoAuthor.objects.get(name=mongo_quote.author.fullname)
            tags = ','.join(mongo_quote.tags)
            DjangoQuote.objects.get_or_create(
                text=mongo_quote.quote,
                author=django_author,
                defaults={'tags': tags}
            )
        except DjangoAuthor.DoesNotExist:
            print(f"Author {mongo_quote.author.fullname} not found in Django DB.")


# Виконання міграції
if __name__ == '__main__':
    migrate_authors()
    migrate_quotes()
    print("Migration completed.")
