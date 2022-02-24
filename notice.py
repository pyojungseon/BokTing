from mariaDB.bokTingDBCon import BokTingDB
from rabbitMQ.msgQPublisher import MsgQPublisher
from datetime import date
import sys
import io
import configparser

class Notice:

    conn = None
    env = None
    dbCon = None
    msgQ = None

    def __init__(self, _env):
        print("Notice Constructor : %s" % _env)
        self.env=_env
        self.dbCon = BokTingDB(_env)
        self.dbCon.dbConnection()
        self.msgQ = MsgQPublisher()

    def __del__(self):
        print("Notice Destructor")
    
    def getConfig(self, env):
        properties = configparser.ConfigParser()
        properties.read('./config/config.ini')
        if(env=='T'):
            props = properties["TEST"]
        else:
            props = properties["PROD"]
        print("Mode : %s" % props["env"])
        return props

    def sendNoticeData(self):
        noticeData =  self.dbCon.getNoticeData()
        userData = self.dbCon.getNoticeUserData()
        if len(noticeData)==0:
            return
        else:
            number = 1
            for notice in noticeData:
                print(notice)
                for user in userData:
                    msg = self.env+"||"+str(user[0])+"||[공지사항 "+str(date.today())+"]"+notice[1]
                    print(msg)
                    self.msgQ.send(msg)
                self.dbCon.updateNoticeData(notice)


sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding="utf-8")

dbCon = None
env = 'D'

if len(sys.argv) != 2:
    print("Arguments should be 1")
    sys.exit()
elif(sys.argv[1]!='P' and sys.argv[1]!='T'):
    print("Check Arguments : [P]/[T]")
    sys.exit()
else:
    env = sys.argv[1]

notice = Notice(env)
props = notice.getConfig(env)
dbCon = BokTingDB(env)
dbCon.dbConnection()

msgQ = MsgQPublisher()
notice.sendNoticeData()
