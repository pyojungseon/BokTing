import pymysql
import sys
import configparser

class BokTingDB:

    conn = None
    env = None

    def __init__(self, _env):
        print("DB Construcor : %s" % _env)
        self.env = _env

    def __del__(self):
        print("DB Destructor")
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

    def getUserData(self, telegramID):
        cur = self.conn.cursor()
        sql = 'select * from UserTBL where telegramID ='+str(telegramID)
        print('getUserData : '+sql)
        cur.execute(sql)
        userData = []
        while(True):
            row = cur.fetchone()
            if row==None:
                break
            userData = row
        return userData
    
    def getMateData(self, telegramID):
        cur = self.conn.cursor()
        sql = 'select * from MateTBL where telegramID ='+str(telegramID)
        cur.execute(sql)
        mateData = []
        while(True):
            row = cur.fetchone()
            if row==None:
                break
            mateData.append(row)
        return mateData
    
    def getMateDataOne(self, telegramID, name):
        cur = self.conn.cursor()
        sql = "select * from MateTBL where telegramID ='"+str(telegramID)+"' and name = '"+name+"'"
        print(sql)
        cur.execute(sql)
        row = cur.fetchone()
        return row
    
    def checkMateData(self, telegramID, name):
        cur = self.conn.cursor()
        sql = "select * from MateTBL where telegramID = '"+str(telegramID)+"' and name='"+name+"'"
        cur.execute(sql)
        mateData = []
        while(True):
            row = cur.fetchone()
            if row==None:
                break
            mateData.append(row)
        return mateData

    def insertUserData(self, userData):
        cur = self.conn.cursor()
        try:
            sql = "insert into UserTBL values('"+userData[0]+"','"+userData[1]+"','"+userData[2]+"','"+userData[3]+"','Y','"+userData[4]+"',current_timestamp,current_timestamp)"
            print(sql)
            cur.execute(sql)
        except Exception as ex:
            print("user insert error")
            print(ex)
        self.conn.commit()

    def insertLogData(self, textMsg):
        cur = self.conn.cursor()
        print("%s %s %s" %(textMsg[0], textMsg[2], textMsg[1]))
        try:
            sql = "insert into LogTBL values('"+str(textMsg[0])+"','"+textMsg[1]+"','"+textMsg[2]+"',current_timestamp)"
            print(sql)
            cur.execute(sql)
        except Exception as ex:
            print("log insert error")
            print(ex)
        self.conn.commit()

    def insertMateData(self, mateData):
        cur = self.conn.cursor()
        try:
            sql = "insert into MateTBL(telegramID, name, sex, tall, age, company, area, phoneNumber, regDate, modDate) values('"+str(mateData[7])+"','"+mateData[1]+"','"+mateData[2]+"','"+str(mateData[3])+"','"+str(mateData[4])+"','"+mateData[5]+"','"+mateData[6]+"','010-0000-0000',current_timestamp,current_timestamp)"
            print(sql)
            cur.execute(sql)
        except Exception as ex:
            print("mate insert error")
            print(ex)
        self.conn.commit()

    def deleteMateData(self, mateData):
        cur = self.conn.cursor()
        try:
            sql="delete from MateTBL where telegramID='"+str(mateData[0])+"' and name='"+mateData[1]+"'"
            print(sql)
            cur.execute(sql)
        except Exception as ex:
            print("mate delete error")
            print(ex)
        self.conn.commit()
        self.deleteReqData(mateData)

    def insertReqData(self, reqData):
        cur = self.conn.cursor()
        try:
            sql="insert into ReqTBL values('"+str(reqData[7])+"','"+reqData[1]+"','"+str(reqData[2])+"','"+str(reqData[3])+"','"+str(reqData[4])+"','"+str(reqData[5])+"',NULL,'"+reqData[6]+"',current_timestamp,current_timestamp)"
            print(sql)
            cur.execute(sql)
        except Exception as ex:
            print("req insert error")
            print(ex)
        self.conn.commit()


    def deleteReqData(self, reqData):
        cur = self.conn.cursor()
        try:
            sql="delete from ReqTBL where telegramID='"+str(reqData[0])+"' and name='"+reqData[1]+"'"
            print(sql)
            cur.execute(sql)
        except Exception as ex:
            print("req delete error")
            print(ex)
        self.conn.commit()
        self.deleteMatchData(reqData)
    
    def getReqData(self, reqData):
        cur = self.conn.cursor()
        sql = "select * from ReqTBL where telegramID ='"+str(reqData[1])+"'"
        print(sql)
        cur.execute(sql)
        reqData = []
        while(True):
            row = cur.fetchone()
            if row==None:
                break
            reqData.append(row)
        return reqData
    
    def getReqDataOne(self, telegramID, name):
        cur = self.conn.cursor()
        sql = "select * from ReqTBL where telegramID ='"+str(telegramID)+"' and name = '"+name+"'"
        print(sql)
        cur.execute(sql)
        row = cur.fetchone()
        return row
    
    def getReqMatchData(self, reqData, matchSex):
        cur = self.conn.cursor()
        sql = "select * from MateTBL where tall between '"+str(reqData[2])+"' and '"+str(reqData[3])+"' and age between '"+str(reqData[4])+"' and '"+str(reqData[5])+"' and sex = '"+matchSex+"' and telegramID != '"+str(reqData[7])+"'"
        print(sql)
        cur.execute(sql)
        reqData = []
        while(True):
            row = cur.fetchone()
            if row==None:
                break
            reqData.append(row)
            print(row[0])
        return reqData

    def getMatchData(self, mateData):
        cur = self.conn.cursor()
        sql = "select * from MatchTBL where telegramID ='"+str(mateData[1])+"' and DATEDIFF(current_timestamp, regDate)<=7"
        print(sql)
        cur.execute(sql)
        reqData = []
        while(True):
            row = cur.fetchone()
            if row==None:
                break
            reqData.append(row)
        return reqData
    
    def insertMatchData(self, matchData):
        cur = self.conn.cursor()
        try:
            sql="insert into MatchTBL values('"+str(matchData[5])+"','"+str(matchData[0])+"','"+matchData[1]+"','"+str(matchData[2])+"','"+matchData[3]+"','"+matchData[4]+"','Y','N',current_timestamp,current_timestamp)"
            print(sql)
            cur.execute(sql)
        except Exception as ex:
            print("matchData insert error")
            print(ex)
        self.conn.commit()
   
    def getMaxMatchSeq(self, matchData):
        cur = self.conn.cursor()
        sql = "select MAX(SEQ)+1 from MatchTBL where telegramID='"+matchData[0]+"'"
        print(sql)
        cur.execute(sql)
        row = cur.fetchone()
        return row[0]

    def getCheckMatchDataFrom(self, matchData):
        cur = self.conn.cursor()
        sql = "select A.*, B.comment from (select A.*, B.sex, B.tall, B.age, B.company, B.area, C.name as pname, C.phoneNumber from MatchTBL A, MateTBL B, UserTBL C where A.telegramID='"+matchData[2]+"' and A.name='"+matchData[1]+"' and A.partnerID = B.telegramID and A.partnerName = B.name and C.telegramID = B.telegramID and DATEDIFF(current_timestamp, A.modDate)<=14) as A left outer join ReqTBL B on A.partnerID=B.telegramID and A.partnerName=B.name"
        print(sql)
        cur.execute(sql)
        retData = []
        while(True):
            row = cur.fetchone()
            if row==None:
                break
            retData.append(row)
        return retData
    
    def getCheckMatchDataTo(self, matchData):
        cur = self.conn.cursor()
        sql = "select A.*, B.comment from (select A.*, B.sex, B.tall, B.age, B.company, B.area, C.name as pname, C.phoneNumber from MatchTBL A, MateTBL B, UserTBL C where A.partnerID='"+matchData[2]+"' and A.partnerName='"+matchData[1]+"' and A.telegramID = B.telegramID and A.name = B.name and coupling='N' and C.telegramID = B.telegramID and DATEDIFF(current_timestamp, A.modDate)<=14) as A left outer join ReqTBL B on A.telegramID=B.telegramID and A.name=B.name"
        print(sql)
        cur.execute(sql)
        retData = []
        while(True):
            row = cur.fetchone()
            if row==None:
                break
            retData.append(row)
        return retData
    
    def insertSuggestion(self, msgData):
        cur = self.conn.cursor()
        try:
            sql="insert into SugTBL values('"+str(msgData[0])+"','"+msgData[1]+"',current_timestamp,current_timestamp)"
            print(sql)
            cur.execute(sql)
        except Exception as ex:
            print("suggestion insert error")
            print(ex)
        self.conn.commit()
    
    def deleteMatchData(self, matchData):
        cur = self.conn.cursor()
        try:
            sql="delete from MatchTBL where (telegramID='"+str(matchData[0])+"' and name='"+matchData[1]+"') or (partnerID='"+str(matchData[0])+"' and partnerName='"+matchData[1]+"')"
            print(sql)
            cur.execute(sql)
        except Exception as ex:
            print("match delete error")
            print(ex)
        self.conn.commit()
    
    def noMatchData(self, matchData):
        cur = self.conn.cursor()
        try:
            sql="update MatchTBL set del='Y' where (seq = '"+str(matchData[1])+"' and telegramID = '"+str(matchData[2])+"') or (partnerID='"+str(matchData[2])+"' and partnerName = (select name from MatchTBL where seq='"+str(matchData[1])+"' and telegramID = '"+str(matchData[2])+"') and name=(select partnerName from MatchTBL where seq='"+str(matchData[1])+"' and telegramID='"+str(matchData[2])+"'))"
            print(sql)
            cur.execute(sql)
        except Exception as ex:
            print("noMatchData update error")
            print(ex)
        self.conn.commit()
    

    def insertNoticeData(self, noticeData):
        cur = self.conn.cursor()
        try:
            sql="insert into NoticeTBL(msg, send, regDate, modDate) values('"+noticeData+"','N',current_timestamp,current_timestamp)"
            print(sql)
            cur.execute(sql)
        except Exception as ex:
            print("notice insert error")
            print(ex)
        self.conn.commit()
    
    def getNoticeData(self):
        cur = self.conn.cursor()
        sql = "select * from NoticeTBL where send='N' order by regDate"
        print(sql)
        cur.execute(sql)
        retData = []
        while(True):
            row = cur.fetchone()
            if row==None:
                break
            retData.append(row)
        return retData
    
    def updateNoticeData(self, notice):
        cur = self.conn.cursor()
        try:
            sql="update NoticeTBL set send='Y', modDate=current_timestamp where seq = '"+str(notice[0])+"'"
            print(sql)
            cur.execute(sql)
        except Exception as ex:
            print("NoticeTBL update error")
            print(ex)
        self.conn.commit()
    
    def getNoticeUserData(self):
        cur = self.conn.cursor()
        sql = "select * from UserTBL where enable='Y'"
        print(sql)
        cur.execute(sql)
        retData = []
        while(True):
            row = cur.fetchone()
            if row==None:
                break
            retData.append(row)
        return retData
    

