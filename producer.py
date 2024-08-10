import pika
import json
from faker import Faker
from mongoengine import connect
from models import Contact

connect('test')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

fake = Faker()
for _ in range(10):
    contact = Contact(
        fullname=fake.name(),
        email=fake.email()
    )
    contact.save()

    message = {'contact_id': str(contact.id)}
    channel.basic_publish(exchange='', routing_key='email_queue', body=json.dumps(message))

print("Контакти згенеровані та додані до черги.")
connection.close()
