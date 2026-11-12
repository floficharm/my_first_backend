import pika
import json

def publish_book_event(event_type: str, book_data: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue="books", durable=True)

    massage = {
        "event": event_type,
        "data": book_data,
    }

    channel.basic_publish(
        exchange='',
        routing_key='books',
        body=json.dumps(massage),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()