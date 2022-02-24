import pika
import configparser
import sys

class MsgQPublisher:
    def __init__(self):
        return

    def getConfig(self):
        properties = configparser.ConfigParser()
        properties.read('./config/MQConfig.ini')
        return properties["RabbitMQ"]

    def send(self, msg):
        props = self.getConfig()
        self.__url = props["url"]
        self.__port = props["port"]
        self.__vhost = props["vhost"]
        self.__cred = pika.PlainCredentials(props['cred_id'], props['cred_password'])
        self.__queue = props['queue']

        conn = pika.BlockingConnection(pika.ConnectionParameters(self.__url, self.__port, self.__vhost, self.__cred))
        chan = conn.channel()
        chan.basic_publish(
            exchange='',
            routing_key = self.__queue,
            body = msg
        )
        conn.close()
        return

