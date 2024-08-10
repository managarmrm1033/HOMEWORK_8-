import pika
import json
from mongoengine import connect
from models import Contact

connect('test')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

def send_email_stub(contact):
    print(f"Відправлення email до {contact.email}")
    return True

def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    
    contact = Contact.objects(id=contact_id).first()
    if contact:
        if send_email_stub(contact):
            contact.is_sent = True
            contact.save()
            print(f"Email до {contact.email} відправлено.")

channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Очікування повідомлень. Натисніть CTRL+C для виходу.')
channel.start_consuming()
