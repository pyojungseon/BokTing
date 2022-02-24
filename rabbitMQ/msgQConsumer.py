import pika
import telepot
import configparser
import sys


class msgQConsumer:

    def __init__(self):
        return

    def getMsgConfig(self):
        properties = configparser.ConfigParser()
        properties.read('../config/MQConfig.ini')
        return properties["RabbitMQ"]

    def getEnvConfig(self, env):
        properties = configparser.ConfigParser()
        properties.read('../config/config.ini')
        if(env=='T'):
            props = properties["TEST"]
        else:
            props = properties["PROD"]
        print("Mode : %s" % props["env"])
        return props


    def on_message(channel, method_frame, header_frame, body):
        print('Received %s' % body)
        body = body.decode("utf-8")
        msg = body.split("||")
        props = msgQConsumer().getEnvConfig(msg[0])
        token=props["token"]
        id=msg[1]
        bot = telepot.Bot(token)
        bot.sendMessage(id, msg[2])
        return

    def main(self):
        props = self.getMsgConfig()
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
            on_message_callback = msgQConsumer.on_message,
            auto_ack = True
        )
        print('Consumer is starting...')
        chan.start_consuming()
        return

consumer = msgQConsumer()
consumer.main();

