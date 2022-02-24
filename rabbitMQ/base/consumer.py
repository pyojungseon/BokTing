import pika
import telepot
import configparser
import sys

class Consumer:

    def __init__(self):
        return

    def getConfig(self):
        properties = configparser.ConfigParser()
        properties.read('../config/MQConfig.ini')
        return properties["RabbitMQ"]

    def on_message(channel, method_frame, header_frame, body):
        print('Received %s' % body)

        token='2004595800:AAF9PfIiutxs9rEIzWOOSFuY1JtTl72FOkk'
        id='2026330004'
        bot = telepot.Bot(token)
        bot.sendMessage(id, body)
        return

    def main(self):
        props = self.getConfig()
        print("%s" % props["url"])
        self.__url = props["url"]
        self.__port = props["port"]
        self.__vhost = props["vhost"]
        self.__cred = pika.PlainCredentials(props['cred_id'], props['cred_password'])
        self.__queue = props['queue']
        
        conn = pika.BlockingConnection(pika.ConnectionParameters(self.__url, self.__port, self.__vhost, self.__cred))
        chan = conn.channel()
        chan.basic_consume(
            queue = self.__queue,
            on_message_callback = Consumer.on_message,
            auto_ack = True
        )
        print('Consumer is starting...')
        chan.start_consuming()
        return

consumer = Consumer()
consumer.main()

