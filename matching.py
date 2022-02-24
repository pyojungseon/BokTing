from mariaDB.bokTingDBCon import BokTingDB
from rabbitMQ.msgQPublisher import MsgQPublisher

class Matching:

    conn = None
    env = None
    dbCon = None
    msgQ = None

    def __init__(self, _env):
        print("Matching Constructor : %s" % _env)
        self.env=_env
        self.dbCon = BokTingDB(_env)
        self.dbCon.dbConnection()
        self.msgQ = MsgQPublisher()

    def __del__(self):
        print("Matching Destructor")

    def findMatchData(self, mateData, reqData):
        matchSex="여"
        if mateData[2]=="여":
            matchSex="남"
        print(reqData)
        matchData =  self.dbCon.getReqMatchData(reqData, matchSex)
        fromUser = self.dbCon.getUserData(str(reqData[len(reqData)-1]))
        print(fromUser)
        isBok=False
        isGroup=False
        groupAge=str(fromUser[3])[0:2]
        if mateData[5]=="한은":
            isBok=True
        if fromUser[5]=="Y":
            isGroup=True
            print("group여부 : "+str(isGroup)+" || "+groupAge)
        if len(matchData)==0:
            return
        else:
            number = 1
            for match in matchData:
                #check counterpart
                toUser = self.dbCon.getUserData(match[0])
                if toUser[5]=="Y":
                    isGroup=True
                isOKAY = ((isGroup) and (groupAge!=str(toUser[3])[0:2]))
                print("group여부 : "+ str(isOKAY) + " "+str(isGroup)+" "+groupAge+" "+str(toUser[3])[0:2])
                if ((not isBok) or (match[5]!="한은")) and (not ((isGroup) and (groupAge!=str(toUser[3])[0:2]))):
                    coupling="N"
                    msgFrom = self.env+"||"+str(mateData[0])
                    msgTo = self.env+"||"+str(match[0])
                
                    print("match data : %s, %s, %s" %(match[0], match[1], match[2]))

                    partnerReq = self.dbCon.getReqDataOne(match[0], match[1])

                    if partnerReq is None:
                        msgFrom = msgFrom+"||소개팅대상자 ["+mateData[1]+"] 이(가) 매칭되었습니다! \n\n/check를 통해 매칭데이터를 확인하세요"
                        msgTo = msgTo+"||소개팅대상자 ["+match[1]+"] 을(를) 원하는 사람이 있습니다! \n\n/check를 통해 매칭데이터를 확인하세요"
                    elif mateData[3]>=partnerReq[2] and mateData[3]<=partnerReq[3] and mateData[4]>=partnerReq[4] and mateData[4]<=partnerReq[5]:
                        msgFrom = msgFrom+"||소개팅대상자 ["+mateData[1]+"] 이(가) 매칭되었습니다! \n\n/check를 통해 매칭데이터를 확인하세요"
                        msgTo = msgTo+"||소개팅대상자 ["+match[1]+"] 이(가) 매칭되었습니다! \n\n/check를 통해 매칭데이터를 확인하세요"
                        partner=[]
                        partner.append(match[0])
                        partner.append(match[1])
                        partner.append(mateData[0])
                        partner.append(mateData[1])
                        coupling="Y"
                        partner.append(coupling)
                        print("%s %s %s %s" %(partner[0], partner[1], partner[2], partner[3]))
                        seq = self.dbCon.getMaxMatchSeq(partner)
                        if seq==None:
                            seq=1
                        partner.append(seq)
                        self.dbCon.insertMatchData(partner)
                    else :
                        msgFrom = msgFrom+"||소개팅 대상자 ["+mateData[1]+"] 이(가) 매칭되었습니다! \n\n/check 를 통해 매칭데이터를 확인하세요"
                        msgTo = msgTo+"||소개팅 대상자 ["+match[1]+"] 을(를) 원하는 사람이 있습니다! use \n\n/check to check matching"

                    matchData=[]
                    matchData.append(mateData[0])
                    matchData.append(mateData[1])
                    matchData.append(match[0])
                    matchData.append(match[1])
                    matchData.append(coupling)
                    seq = self.dbCon.getMaxMatchSeq(matchData)
                    if seq==None:
                        seq=1
                    matchData.append(seq)

                    self.dbCon.insertMatchData(matchData)
                    print(msgTo)
                    print(msgFrom)
                    self.msgQ.send(msgTo)
                    self.msgQ.send(msgFrom)
