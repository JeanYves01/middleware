import os
import json
import logging
import random
import string
import pika
import paramiko
from time import sleep

# Configuration
SFTP_HOST = 'sftp'
SFTP_PORT = 22
SFTP_USER = 'ftpuser'
SFTP_PASS = 'abcd1234'
SFTP_DIR = '/ftp'

RABBITMQ_HOST = 'rabbitmq'
RABBITMQ_USER = 'guest'
RABBITMQ_PASS = 'guest'
RABBITMQ_QUEUE = 'middleware_queue'

def generate_password(length=8):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def send_user_password(rabbitmq_channel, user_data):
    password = generate_password()
    user_data.password = password
    user = {
        "nom": user_data.get("nom", ""),
        "prenom": user_data.get("prenom", ""),
        "email": user_data.get("email", ""),
        "password": password
    }
    rabbitmq_channel.basic_publish(
        exchange='',
        routing_key=RABBITMQ_QUEUE,
        body=json.dumps(user)
    )
    logging.info(f"Sent user password message: {user}")

def connect_rabbitmq():
    """Create and return a RabbitMQ channel."""
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    return channel

def send_test_users(rabbitmq_channel):
    """Send test user data to RabbitMQ."""
    test_users = {"nom": "Koffi", "prenom": "Jean", "email": "jeanyvesk015@gmail.com"}
       
   
    
    for user_data in test_users:
        send_user_password(rabbitmq_channel, user_data)

def main():
    logging.basicConfig(level=logging.INFO)
    
    # Connexion à RabbitMQ
    channel = connect_rabbitmq()
    
    # Envoyer des utilisateurs de test
    send_test_users(channel)

    # Fermer la connexion
    channel.close()

if __name__ == '__main__':
    main()
