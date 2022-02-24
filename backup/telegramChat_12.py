from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from mariaDB.bokTingDBCon import BokTingDB
from rabbitMQ.msgQPublisher import MsgQPublisher
from matching import Matching
import configparser
import sys
import io

def getConfig(env):
    properties = configparser.ConfigParser()
    properties.read('./config/config.ini')
    if(env=='T'):
        props = properties["TEST"]
    else:
        props = properties["PROD"]
    print("Mode : %s" % props["env"])
    return props

def _start(update, context):
    logInsert(update, context)
    env_name=''
    if(env=='T'):
        env_name = '[TEST]'

    text="[welcome to Bok-ting]"+env_name+". /join 을 이용하여 사용자를 등록하여 주세요. 사용법을 알고싶으시면 /help를 입력하여주세요"
    msg = env+"||"+str(update.effective_chat.id)+"||"+text
    msgQ.send(msg)
    #context.bot.send_message(chat_id=update.effective_chat.id, text="welcome to Bok-ting"+env_name+". Please try /join to register user. If you want to know how to use it, try /help")

def _user(update, context):
    logInsert(update, context)
    userData = dbCon.getUserData(update.effective_chat.id)
    if len(userData)==0:
        text="사용자 등록이 되어있지 않습니다. /join 을 통해 사용자를 등록하여주세요"
        msg = env+"||"+str(update.effective_chat.id)+"||"+text
        msgQ.send(msg)
        #context.bot.send_message(chat_id=update.effective_chat.id, text="You are not Joined. Please try /join to register your Account")
    else:
        text = "User ["+userData[0]+"]"+" data "+userData[1]
        msg = env+"||"+str(update.effective_chat.id)+"||"+text
        msgQ.send(msg)
        #context.bot.send_message(chat_id=update.effective_chat.id, text=ansMsg)

def _join(update, context):
    logInsert(update, context)
    testData = update.message.text.split(" ")
    if len(testData)!=4:
        text="아래의 형식으로 입력하여주세요. \n\n/join [name] [phoneNumber] [BOK ID]\n\nex)/join 길동 010-1234-5678 2010062"
        msg = env+"||"+str(update.effective_chat.id)+"||"+text
        msgQ.send(msg)
        #context.bot.send_message(chat_id=update.effective_chat.id, text="Input like this. /join [name] [phoneNumber] [BOK ID]\n\nex)/join 길동 010-1234-5678 2010062")
    else:
        userData = []
        userData.append(str(update.effective_chat.id))
        userData.append(testData[1])
        userData.append(testData[2])
        userData.append(testData[3])
        dbCon.insertUserData(userData)
        text="사용자가 등록되었습니다! /user를 통해 확인해주세요"
        msg = env+"||"+str(update.effective_chat.id)+"||"+text
        msgQ.send(msg)
        #context.bot.send_message(chat_id=update.effective_chat.id, text="Your account is registered! check /user")

def echo(update, context):
    logInsert(update, context)
    ansMsg = "Input Data : "+update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=ansMsg)

def logInsert(update, context):
    #global dbCon
    logData=[]
    logData.append(update.effective_chat.id)
    print(str(update.message.text))
    logData.append(update.message.text)
    logData.append(update.message.text.split(" ")[0])
    dbCon.insertLogData(logData)
    
def _add(update, context):
    logInsert(update, context)
    
    mateData = update.message.text.split(" ")
    print(len(mateData))
    if len(mateData)!=7:
        text="아래의 형식으로 입력하여주세요. \n\n/add [name] [gender] [tall] [age] [company] [area] \n\nex)/add 현빈 남 180 30 한국은행 잠실\n\n 행내 매칭을 피하고싶으신 분은 직장명을 [한은]으로 입력하여주세요!!"
        msg = env+"||"+str(update.effective_chat.id)+"||"+text
        msgQ.send(msg)
        #context.bot.send_message(chat_id=update.effective_chat.id, text="Input like this. /add [name] [sex] [tall] [age] [company] [area] [phoneNumber] \n\nex)/add 현빈 남 180 30 한국은행 잠실 010-5667-6106")
    else:
        mateData.append(update.effective_chat.id)
        dbCon.insertMateData(mateData)
        text = "Added Mate user : "+mateData[1]
        msg = env+"||"+str(update.effective_chat.id)+"||"+text
        msgQ.send(msg)
        #context.bot.send_message(chat_id=update.effective_chat.id, text=ansMsg)
    
def _del(update, context):
    logInsert(update, context)

    mateData = update.message.text.split(" ")
    
    if len(mateData)!=2:
        text="아래의 형식으로 입력하여주세요. \n\n/del [name] \n\nex)/del 현빈"
        msg = env+"||"+str(update.effective_chat.id)+"||"+text
        msgQ.send(msg)
        #context.bot.send_message(chat_id=update.effective_chat.id, text="Input like this. /del [name] \n\nex)/del 현빈")
    else:
        mateData[0] = update.effective_chat.id
        dbCon.deleteMateData(mateData)
        text = "Deleted Mate user : "+mateData[1]
        msg = env+"||"+str(update.effective_chat.id)+"||"+text
        msgQ.send(msg)
        #context.bot.send_message(chat_id=update.effective_chat.id, text=ansMsg)
    

def _show(update, context):
    logInsert(update, context)
    mateData = dbCon.getMateData(update.effective_chat.id)
    if len(mateData)==0:
        text="소개팅 대상자 등록건이 없습니다. /add 를 통해 소개팅 대상자를 입력하여주세요."
        msg = env+"||"+str(update.effective_chat.id)+"||"+text
        msgQ.send(msg)
        #context.bot.send_message(chat_id=update.effective_chat.id, text="No mate user Data. Please try /add to register your mate user")
    else:
        number = 1
        for userData in mateData:
            text = str(number)+" : "+userData[1]+" "+userData[2]+" "+str(userData[3])+" "+str(userData[4])+" "+userData[5]+" "+userData[6]
            msg = env+"||"+str(update.effective_chat.id)+"||"+text
            msgQ.send(msg)
            #context.bot.send_message(chat_id=update.effective_chat.id, text=ansMsg)
            number=number+1
    
def _addr(update, context):
    logInsert(update, context)
    
    reqData = update.message.text.split(" ")
    print(len(reqData))
    if len(reqData)!=6:
        text="아래의 형식으로 입력하여주세요. \n\n/addr [name] [tall_min] [tall_max] [age_min] [age_max]\n\nex)/addr 현빈 155 163 28 31"
        msg = env+"||"+str(update.effective_chat.id)+"||"+text
        msgQ.send(msg)
        #context.bot.send_message(chat_id=update.effective_chat.id, text="Input like this. /addr [name] [tall_min] [tall_max] [age_min] [age_max]\n\nex)/addr 현빈 155 163 28 31")
    else:
        if (dbCon.checkMateData(str(update.effective_chat.id), reqData[1])):
            if(reqData[2]>reqData[3]):
                text="키 조건이 잘못되었습니다. tall_max>=tall_min이어야 합니다."
                msg = env+"||"+str(update.effective_chat.id)+"||"+text
                msgQ.send(msg)
                #context.bot.send_message(chat_id=update.effective_chat.id, text="Tall range is wrong. please check tall_max>=tall_min")
            elif(reqData[4]>reqData[5]):
                text="나이조건이 잘못되었습니다. age_max>=age_min이여야 합니다."
                msg = env+"||"+str(update.effective_chat.id)+"||"+text
                msgQ.send(msg)
                #context.bot.send_message(chat_id=update.effective_chat.id, text="Age range is wrong. please check age_max>=age_min")
            else:
                reqData.append(update.effective_chat.id)
                dbCon.insertReqData(reqData)
                text = "Added Request data : "+reqData[1]
                msg = env+"||"+str(update.effective_chat.id)+"||"+text
                msgQ.send(msg)

                mateData = dbCon.getMateDataOne(update.effective_chat.id, reqData[1])
                print("mateData : %s" % mateData[1])
                matchingBatch = Matching(env)
                matchingBatch.findMatchData(mateData, reqData)
                #context.bot.send_message(chat_id=update.effective_chat.id, text=ansMsg)
        else:
            text="소개팅 대상자를 확인해주세요. "+reqData[1]+"는(은) 등록되어있지 않습니다."
            msg = env+"||"+str(update.effective_chat.id)+"||"+text
            msgQ.send(msg)
            #context.bot.send_message(chat_id=update.effective_chat.id, text="Please Check your Mate Data. "+reqData[1]+" is not registered")
    
def _showr(update, context):
    logInsert(update, context)
    req = update.message.text.split(" ")
    req.append(str(update.effective_chat.id))
    reqData = dbCon.getReqData(req)
    if len(reqData)==0:
        text="요구사항 등록내용이 없습니다. /addr 를 입력하여 요구사항을 등록해주세요"
        msg = env+"||"+str(update.effective_chat.id)+"||"+text
        msgQ.send(msg)
        #context.bot.send_message(chat_id=update.effective_chat.id, text="No request Data. Please try /addr to register your mate request")
    else:
        number = 1
        for userData in reqData:
            text = str(number)+" : "+userData[1]+" tall : "+str(userData[2])+" - "+str(userData[3])+" age : "+str(userData[4])+" - "+str(userData[5])+" "
            msg = env+"||"+str(update.effective_chat.id)+"||"+text
            msgQ.send(msg)
            #context.bot.send_message(chat_id=update.effective_chat.id, text=ansMsg)
            number=number+1

def _delr(update, context):
    logInsert(update, context)

    reqData = update.message.text.split(" ")
    
    if len(reqData)!=2:
        text="아래의 형식으로 입력해주세요. \n\n/delr [name] \n\nex)/delr 현빈"
        msg = env+"||"+str(update.effective_chat.id)+"||"+text
        msgQ.send(msg)
        #context.bot.send_message(chat_id=update.effective_chat.id, text="Input like this. /delr [name] \n\nex)/delr 현빈")
    else:
        reqData[0] = update.effective_chat.id
        dbCon.deleteReqData(reqData)
        text = "Deleted Req data : "+reqData[1]
        msg = env+"||"+str(update.effective_chat.id)+"||"+text
        msgQ.send(msg)
        #context.bot.send_message(chat_id=update.effective_chat.id, text=ansMsg)

def _check(update, context):
    logInsert(update, context)
    match = update.message.text.split(" ")
    if len(match)!=2:
        text="아래의 형식으로 입력해주세요. \n\n/check [name] \n\n ex)/check 현빈"
        msg = env+"||"+str(update.effective_chat.id)+"||"+text
        msgQ.send(msg)
    else:
        match.append(str(update.effective_chat.id))
        matchDataFrom = dbCon.getCheckMatchDataFrom(match)
        matchDataTo = dbCon.getCheckMatchDataTo(match)
        print(len(matchDataFrom))
        print(len(matchDataTo))
        if len(matchDataFrom)==0 and len(matchDataTo)==0:
            text="매칭 내역이 없습니다."
            msg = env+"||"+str(update.effective_chat.id)+"||"+text
            print(msg)
            msgQ.send(msg)
        else:
            if len(matchDataFrom)>0:
                number = 1
                notiMent = "[요구사항 :  <-> 양쪽 매칭 / -> 한쪽 매칭]\n"
                headMsg = env+"||"+str(update.effective_chat.id)+"||"+notiMent
                print(headMsg)
                msgQ.send(headMsg)
                for userData in matchDataFrom:
                    arrow = " -> "
                    if userData[4]=="Y" :
                        arrow = " <-> "
                    text = userData[1]+arrow+userData[3]+", tall : "+str(userData[9])+" age : "+str(userData[10])+" company : "+userData[11]+" area : "+userData[12]+"\n\n"+userData[13]+" number : "+userData[14]+"에게 연락하여 "+userData[3]+"에 대해 문의하세요!"
                    msg = env+"||"+str(update.effective_chat.id)+"||"+text
                    print(msg)
                    msgQ.send(msg)
                    number=number+1
            if len(matchDataTo)>0:
                number = 1
                for userData in matchDataTo:
                    if userData[4]=="N" :
                        text = userData[3]+" -> "+userData[1]+", tall : "+str(userData[9])+" age : "+str(userData[10])+" company : "+userData[11]+" area : "+userData[12]+"\n\n"+userData[13]+" number : "+userData[14]+"에게 연락하여 "+userData[3]+"에 대해 문의하세요!"
                        msg = env+"||"+str(update.effective_chat.id)+"||"+text
                        print(msg)
                        msgQ.send(msg)
                        number=number+1

def _write(update, context):
    logInsert(update, context)
    suggData = update.message.text.split(" ")
    msg = update.message.text[len(suggData[0])+1:len(update.message.text)]
    msgData=[]
    msgData.append(update.effective_chat.id)
    msgData.append(msg)
    if len(suggData)<2:
        text="아래의 형식으로 입력해주세요. \n\n/write [suggestion] \n\nex)/write XX기능이 더 추가되었으면 좋겠습니다!"
        msg = env+"||"+str(update.effective_chat.id)+"||"+text
        msgQ.send(msg)
    else :
        dbCon.insertSuggestion(msgData)
        text="제안사항에 감사드립니다!"
        msg = env+"||"+str(update.effective_chat.id)+"||"+text
        msgQ.send(msg)

def _notice(update, context):
    logInsert(update, context)
    text="[2021-11-17] v0.1 Service Open.\n\n[2021-11-26] v.0.11 행내직원 매칭 방지여부 추가. /add로 확인가능\n\n[2021-12-10] 매칭내역 조회기간 2주로 수정 / 소개팅대상 핸드폰번호 입력 삭제"
    msg = env+"||"+str(update.effective_chat.id)+"||"+text
    msgQ.send(msg)

def _admin(update, context):
    if str(update.effective_chat.id)==props["admin"]:
        noticeData = update.message.text.split(" ")
        if len(noticeData)>=2:
            text = ""
            for i in range(1, len(noticeData)):
                text = text + " " + noticeData[i]
            dbCon.insertNoticeData(text)
            msg = env+"||"+str(update.effective_chat.id)+"||"+text
            print(msg)
            msgQ.send(msg)
    else:
        text="관리자만 가능한 기능입니다"
        msg = env+"||"+str(update.effective_chat.id)+"||"+text
        msgQ.send(msg)


def _help(update, context):
    text = '''/join : 사용자 등록
            \n/user : 사용자 정보 조회
            \n/add : 미팅 대상자 등록
            \n/del : 미팅 대상자 삭제
            \n/show : 미팅 대상자 조회
            \n/addr : 미팅 대상자 요구사항 등록
            \n/showr : 미팅 대상자 요구사항 조회
            \n/delr : 미팅 대상자 요구사항 삭제
            \n/check : 매칭 내역 조회
            \n/write : 개선&요청사항 등록
            \n/notice : 공지사항'''
    msg = env+"||"+str(update.effective_chat.id)+"||"+text
    msgQ.send(msg)
    #context.bot.send_message(chat_id=update.effective_chat.id, text=ansMsg)

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

props = getConfig(env)
dbCon = BokTingDB(env)
dbCon.dbConnection()

msgQ = MsgQPublisher()

updater = Updater(token=props["token"], use_context=True)
dispatcher = updater.dispatcher

add_handler = CommandHandler('add', _add)
dispatcher.add_handler(add_handler)

del_handler = CommandHandler('del', _del)
dispatcher.add_handler(del_handler)

start_handler = CommandHandler('start', _start)
dispatcher.add_handler(start_handler)

user_handler = CommandHandler('user', _user)
dispatcher.add_handler(user_handler)

join_handler = CommandHandler('join', _join)
dispatcher.add_handler(join_handler)

show_handler = CommandHandler('show', _show)
dispatcher.add_handler(show_handler)

addr_handler = CommandHandler('addr', _addr)
dispatcher.add_handler(addr_handler)

delr_handler = CommandHandler('delr', _delr)
dispatcher.add_handler(delr_handler)

showr_handler = CommandHandler('showr', _showr)
dispatcher.add_handler(showr_handler)

check_handler = CommandHandler('check', _check)
dispatcher.add_handler(check_handler)

write_handler = CommandHandler('write', _write)
dispatcher.add_handler(write_handler)

notice_handler = CommandHandler('notice', _notice)
dispatcher.add_handler(notice_handler)

admin_handler = CommandHandler('admin', _admin)
dispatcher.add_handler(admin_handler)

help_handler = CommandHandler('help', _help)
dispatcher.add_handler(help_handler)


echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
updater.idle()
