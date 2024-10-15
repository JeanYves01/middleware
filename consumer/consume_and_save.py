# import json
# import logging

# import pika
# import smtplib
# from email.mime.text import MIMEText
# import pika
# import mysql.connector
# from time import sleep


# # Configurer le logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# RABBITMQ_HOST = 'rabbitmq'
# RABBITMQ_USER = 'guest'
# RABBITMQ_PASS = 'guest'
# RABBITMQ_QUEUE = 'middleware_queue'

# DB_HOST = 'mysql'
# DB_NAME = 'suivi_conso'
# DB_USER = 'jeanyves'
# DB_PASS = '01@3338689'
# DB_PORT = '3306'

# def send_email(user_email, password):
#     smtp_server = 'smtp.gmail.com'
#     smtp_port = 587
#     sender_email = 'jeanvianney0103@gmail.com'
#     sender_password = 'jfsmwptrdjuxnywf'

#     message = MIMEText(f"Bonjour, votre mot de passe est: {password}")
#     message['Subject'] = 'Votre mot de passe'
#     message['From'] = sender_email
#     message['To'] = user_email

#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(sender_email, sender_password)
#             server.send_message(message)
#             logging.info(f"Email sent to {user_email}")
#     except Exception as e:
#         logging.error(f"Failed to send email: {e}")

# def save_message_to_db(db_conn, message):
#     try:
#         cursor = db_conn.cursor()
#         query = 'INSERT INTO messages (message) VALUES (%s)'
#         cursor.execute(query, (message,))
#         db_conn.commit()

#         # Extract user data to send email
#         user_data = json.loads(message)
#         send_email(user_data.get("email"), user_data.get("password"))

#         logging.info(f"Message saved to database: {message}")
#     except mysql.connector.Error as err:
#         logging.error(f"Error: {err}")
#         db_conn.rollback()

# def consume_messages():
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
#     channel = connection.channel()
#     channel.queue_declare(queue=RABBITMQ_QUEUE)

#     db_conn = mysql.connector.connect(
#         host=DB_HOST,
#         user=DB_USER,
#         password=DB_PASS,
#         database=DB_NAME
#     )

#     def callback(ch, method, properties, body):
#         logging.info(f"Received message: {body}")
#         save_message_to_db(db_conn, body)

#     channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)
#     logging.info("Waiting for messages...")
#     channel.start_consuming()

# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     consume_messages()


import os
import json
import pika
import mysql.connector
from time import sleep
import logging

import smtplib
from email.mime.text import MIMEText

# Configurer le logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

RABBITMQ_HOST = 'rabbitmq'
RABBITMQ_USER = 'guest'
RABBITMQ_PASS = 'guest'
RABBITMQ_QUEUE = 'middleware_queue'

DB_HOST = 'mysql'
DB_NAME = 'suivi_conso'
DB_USER = 'jeanyves'
DB_PASS = '01@3338689'
DB_PORT = '3306'

def wait_for_service(service_func, retries=50, delay=10):
    for i in range(retries):
        try:
            return service_func()
        except Exception as e:
            logging.info(f"Waiting for service: {e}")
            sleep(delay)
    raise Exception(f"Service not available after {retries * delay} seconds")

def connect_rabbitmq():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    return channel

def send_email(email, password):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'jeanvianney0103@gmail.com'
    sender_password = 'jfsmwptrdjuxnywf'

    message = MIMEText(f"Bonjour, votre mot de passe est: {password}")
    message['Subject'] = 'Votre mot de passe'
    message['From'] = sender_email
    message['To'] = email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
            logging.info(f"Email sent to {email}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def connect_db():
    conn = mysql.connector.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INT AUTO_INCREMENT PRIMARY KEY,
                       nom CHARACTER(25) NOT NULL, prenom CHARACTER(25) NOT NULL, email CHARACTER(25) NOT NULL, password CHARACTER(25) NOT NULL)''')
    conn.commit()
    if cursor:
        logging.info("Table 'messages' created ")
    else:
        logging.info("Table 'messages' already exists")
    return conn

def save_message_to_db(db_conn, message):
    try:
        cursor = db_conn.cursor()

        # Vérifier dans quelle base de données on travaille
        cursor.execute('SELECT DATABASE();')
        current_database = cursor.fetchone()
        if current_database:
            logging.info(f"Using database: {current_database[0]}")
        else:
            logging.error("Unable to determine the current database")

        # Insérer le message
        query = 'INSERT INTO users (content) VALUES (%s)'
        cursor.execute(query, (message,))
        db_conn.commit()
        if query:
            logging.info("Message saved to database")
        else:
            logging.info("Message don't saved to database")
        # Validation: récupérer les données après insertion pour vérifier
        cursor.execute('SELECT * FROM users ORDER BY id DESC LIMIT 1;')
        result = cursor.fetchone()
        if result:
            logging.info(f"Message retrieved from database: {result}")
        else:
            logging.error("Message not found in database after insertion")
    except mysql.connector.Error as err:
        logging.error(f"Error: {err}")
        db_conn.rollback()

def consume_messages(rabbitmq_channel, db_conn):
    def callback(ch, method, properties, body):
        message = body.decode()
        logging.info(f"Received message: {message}")
        save_message_to_db(db_conn, message)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    rabbitmq_channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)
    logging.info("Waiting for messages. To exit press CTRL+C")
    rabbitmq_channel.start_consuming()

if __name__ == '__main__':
    rabbitmq_channel = wait_for_service(connect_rabbitmq)
    db_conn = wait_for_service(connect_db)
    try:
        consume_messages(rabbitmq_channel, db_conn)
    except KeyboardInterrupt:
        db_conn.close()
        rabbitmq_channel.close()