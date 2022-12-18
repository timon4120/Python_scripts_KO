import pika
import threading
import os
import argparse
from termcolor import colored
from sys import exit
os.system("")

"""
Kamil Orzechowski
Simple RabbitMQ Client: https://www.rabbitmq.com
There is a necessity to create second file and change:
1. queue basic_publish to 'USER2TO' and basic_consume to 'USER1TO';
2. line42: change color for the second user from 'green' to another you like :).
Picture 'results.png' presents results with 2 clients Pychat_KO.py and Pychat_KO2.py.
"""

def main():
    # Server connection
    # credentials = pika.PlainCredentials("login","password")
    # connection_parameteres = pika.ConnectionParameters("xx.xx.xxx.xxx", virtual_host="login", credentials=credentials)
    # connection = pika.BlockingConnection(connection_parameteres)

    #Localhost connection
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))

    channel = connection.channel()
    channel.queue_declare("USER1TO")
    channel.queue_declare("USER2TO")
    channel.queue_purge("USER1TO")
    channel.queue_purge("USER2TO")

    argp = argparse.ArgumentParser()
    argp.add_argument("--user", default = "USER")
    args = argp.parse_args()
    usr = args.user
    print(f"==========|Welcome {usr}! You have just joined to the chat!|==========")
    
    class MyThread_Producer(threading.Thread):
        global usr
        def run(self):
            username = colored(usr,"green")
            while True:
                message = input()
                print('\x1b[1A'+'\x1b[2K'+f"{username}: {message}")
                channel.basic_publish("","USER1TO",f"{username}: {message}")

    class MyThread_Consumer(threading.Thread):
        def run(self):
            def on_message_callback(channel,method,properties,body): 
                print('\x1b[2K' + body.decode())
            channel.basic_consume("USER2TO",on_message_callback,False)
            channel.start_consuming()
            channel.close()

    prod = MyThread_Producer()
    cons = MyThread_Consumer()

    prod.start()
    cons.start()

if __name__ == '__main__':
    main()