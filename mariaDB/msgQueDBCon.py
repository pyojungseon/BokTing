import pymysql
import sys
import configparser

class MsgQueDB:

    conn = None
    env = None

    def __init__(self, _env):
        print("Queue DB Construcor : %s" % _env)
        self.env = _env

    def __del__(self):
        print("Queue DB Destructor")
        self.conn.close()

    def getDBConfig(self):
        properties = configparser.ConfigParser()
        properties.read('./config/DBconfig.ini')
        if(self.env=='T'):
            props = properties["TEST"]
        else:
            props = properties["PROD"]
        print("DB Mode : %s" % props["env"])
        return props

    def dbConnection(self):
        props = self.getDBConfig()
        _host = props["host"]
        _user = props["user"]
        _password = props["password"]
        _db = props["db"]
        _charset=props["charset"]
        print(props)
        self.conn = pymysql.connect(host=_host, user=_user, password=_password, db=_db, charset=_charset)


    def insertQueueData(self, queueData):
        cur = self.conn.cursor()
        try:
            sql = "insert into MsgQTBL values('"+queueData[0]+"', '"+queueData[1]+"','"+queueData[2]+"','N',current_timestamp,current_timestamp)"
            print(sql)
            cur.execute(sql)
        except Exception as ex:
            print("msgQueue DB insert error")
            print(ex)
        self.conn.commit()


    def updateSucessQueueData(self, queueData):
        cur = self.conn.cursor()
        try:
            sql="update MateTBL set success='Y' where telegramID='"+str(mateData[1])+"' and seq='"+str(mateData[0])+"'"
            print(sql)
            cur.execute(sql)
        except Exception as ex:
            print("msgQueue DB update error")
            print(ex)
        self.conn.commit()


