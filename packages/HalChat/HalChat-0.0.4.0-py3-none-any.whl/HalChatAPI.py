import requests
import websockets
import asyncio
import time
import json
import os
from HalEncryption import HalEncryption
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256
import base64

class HalChatAPI:
    def __init__(self,code,sleepTime=0.00,save_file_passwords='HalChatPasswords.json',auto_join_chats=True,check_bots_messages=False,log_level:int=1):
        self.code=code
        self.url='https://halchat.halwarsing.net/api'
        self.ws_url="wss://halchat.halwarsing.net/ws/"
        self.events={'onNewMessage':[],'onNewChat':[],'onReceivePassword':[],'onStart':[],'onClickButton':[],'onBotMessage':[],'onDeleteMessage':[],'onEditMessage':[]}
        self.isRun=False
        self.sleepTime=sleepTime
        self.chats={}
        self.chatsPasswords={}
        self.bot=requests.post('https://halwarsing.net/api/api?req=getInfoUser',data={'code':self.code}).json()
        self.botId=self.bot['id']
        self.he=HalEncryption()
        self.requested_passwords={}
        self.save_file_passwords=save_file_passwords
        self.auto_join_chats=auto_join_chats
        self.check_bots_messages=check_bots_messages
        self.log_level=log_level
        self.loadPasswords()

    def apiReq(self,req:str,getData:str='',postData:dict={}):
        postData['code']=self.code
        out=requests.post(self.url+'?req='+req+getData,data=postData)
        if out.status_code:
            try:
                o=out.json()
                if(o['errorCode']>0 and self.log_level>0):
                    print('Error api: ',o)
                if(self.log_level>1):
                    print('Successfully api request: ',req,getData,postData,o)
                return o
            except json.decoder.JSONDecodeError:
                if(self.log_level>0):
                    print('Error server: ',req,getData,postData,out.text)
                return None
        return None

    def event_add(self,name:str,func):
        if name in self.events:
            self.events[name].append(func)
            return True
        return False

    def event(self,name:str):
        def event_inside(func):
            return self.event_add(name,func)
        return event_inside

    def run_event(self,name:str,args:list):
        if name in self.events:
            for ev in self.events[name]:
                #ev(*args)
                asyncio.create_task(ev(*args))
            return True
        return False

    def run(self):
        asyncio.run(self.async_run())

    async def async_run(self):
        #for v in self.apiReq('getListChats')['chats']:
        #    self.chats[str(v['uid'])]=[v['maxLastMessage'],v['maxAction']]
        self.isRun=True
        self.run_event('onStart',[])
        await self.connect()
        """while self.isRun:
            data=self.apiReq('getEvents',postData={'chats':json.dumps(self.chats)})
            if not data is None and data['errorCode']==0:
                for msg in data['newMessages']:
                    self.chats[str(msg['fromChat'])][0]=msg['uid']
                    if str(msg['fromChat']) in self.chatsPasswords:
                        msg['message']=self.he.decodeByHash(bytes.fromhex(msg['message']),self.chatsPasswords[str(msg['fromChat'])]+msg['encryptId'],10).decode("utf-8")
                        if(msg['answerMsg']!='-1'):
                            msg['answerMsgText']=self.he.decodeByHash(bytes.fromhex(msg['answerMsgText']),self.chatsPasswords[str(msg['fromChat'])]+msg['answerMsgEncryptId'],10).decode("utf-8")
                    self.run_event("onNewMessage",[msg,str(msg['fromChat']) in self.chatsPasswords])
                for chat in data['newChats']:
                    if self.auto_join_chats:
                        self.joinChatByInviteId(chat['inviteId'])
                    self.chats[str(chat['chatId'])]=[chat['maxLastMessage'],chat['maxLastAction']]
                    self.run_event("onNewChat",[chat['chatId'],chat['inviteId']])
                for v in data['events']:
                    self.chats[str(v['fromChat'])][1]=v['uid']
                    if v['type']==2:
                        if str(v['fromChat']) in self.requested_passwords:
                            passw=self.requested_passwords[str(v['fromChat'])].decrypt(base64.b64decode(v['data'])).decode('utf-8')
                            self.addChatPassword(v['fromChat'],passw)
                            self.savePasswords()
                            v['data']=passw
                            del self.requested_passwords[v['fromChat']]
                        self.run_event('onReceivePassword',[v['fromChat'],v['data']])
                    elif v['type']==6:
                        self.run_event('onClickButton',[v['fromChat'],v['fromId'],v['fromMsg'],v['data']])
            if self.check_bots_messages:
                data=self.getBotsMessages()
                if not data is None and data['errorCode']==0:
                    for msg in data['messages']:
                        self.run_event('onBotMessage',[msg['fromId'],msg['time'],msg['data']])
            time.sleep(self.sleepTime)"""
        

    def close(self):
        self.isRun=False
        try:
            self.ws.close()
        except Exception as e:
            self.printError(f"Error WebSocket: {e}")

    def addChatPassword(self,chatId:int,password:str):
        self.chatsPasswords[str(chatId)]=password

    def requestPassword(self,chatId:int):
        key=RSA.generate(2048)
        out=self.apiReq("requestPassword",getData='&chatId='+str(chatId),postData={'publicKey':base64.b64encode(key.publickey().exportKey()).decode('utf-8')})
        if out['errorCode']==0:
            self.requested_passwords[str(chatId)]=PKCS1_OAEP.new(key,hashAlgo=SHA256)
            return True
        return False

    def savePasswords(self):
        f=open(self.save_file_passwords,'w')
        f.write(json.dumps(self.chatsPasswords))
        f.close()

    def loadPasswords(self):
        if os.path.isfile(self.save_file_passwords):
            f=open(self.save_file_passwords,'r')
            self.chatsPasswords=json.loads(f.read())
            f.close()

    def sendMessage(self,chatId:int,message:str,encryptId:str=None,
                    attachments:list=[],answerMsg:int=-1,commentMsg:int=-1,
                    soundMsg:str=-1,buttons:list=None,plugins=None):
        if str(chatId) in self.chatsPasswords:
            if encryptId is None:
                encryptId=self.he.hh.Str2Hash(str(time.time_ns())+":"+str(chatId)+":"+str(self.chats[str(chatId)] if str(chatId) in self.chats else chatId),16,16)
            message=self.he.encodeByHash(message.encode('utf-8'),self.chatsPasswords[str(chatId)]+encryptId,10).hex()
        elif encryptId is None:
            encryptId=""
        postData={
            'message':message,
            'attachments':json.dumps(attachments),
            'encryptId':encryptId
        }
        if not (buttons is None):
            postData['buttons']=json.dumps(buttons)
        if not (plugins is None):
            postData['plugins']=json.dumps(plugins)
        return self.apiReq(
            "sendMessage",
            getData="&soundMsg="+str(soundMsg)+"&chatId="+str(chatId)+("" if answerMsg==-1 else "&answerMsg="+str(answerMsg))+("" if commentMsg==-1 else "&commentMsg="+str(commentMsg)),
            postData=postData
        )
    
    """def sendMessages(self,chatIds:list,message:str,encryptId:str=None,
                    attachments:list=[],answerMsg:int=-1,commentMsg:int=-1,
                    soundMsg:str=-1,buttons:list=None,plugins=None):
        if str(chatId) in self.chatsPasswords:
            if encryptId is None:
                encryptId=self.he.hh.Str2Hash(str(time.time_ns())+":"+str(chatId)+":"+str(self.chats[str(chatId)] if str(chatId) in self.chats else chatId),16,16)
            message=self.he.encodeByHash(message.encode('utf-8'),self.chatsPasswords[str(chatId)]+encryptId,10).hex()
        elif encryptId is None:
            encryptId=""
        postData={
            'message':message,
            'attachments':json.dumps(attachments),
            'encryptId':encryptId
        }
        if not (buttons is None):
            postData['buttons']=json.dumps(buttons)
        if not (plugins is None):
            postData['plugins']=json.dumps(plugins)
        return self.apiReq(
            "sendMessage",
            getData="&soundMsg="+str(soundMsg)+"&chatId="+str(chatId)+("" if answerMsg==-1 else "&answerMsg="+str(answerMsg))+("" if commentMsg==-1 else "&commentMsg="+str(commentMsg)),
            postData=postData
        )"""

    def joinChatByInviteId(self,inviteId:int):
        return self.apiReq('joinChatByInviteId',getData='&inviteId='+str(inviteId))

    def deleteMessage(self,chatId:int,msgId:int):
        return self.apiReq('deleteMessage',getData='&chatId='+str(chatId)+'&msgId='+str(msgId))

    def editMessage(self,chatId:int,msgId:int,message:str,encryptId:str=None,attachments:list=[]):
        if str(chatId) in self.chatsPasswords:
            if encryptId is None:
                encryptId=self.he.hh.Str2Hash(str(time.time_ns())+":"+str(chatId)+":"+str(self.chats[str(chatId)]),16,16)
            message=self.he.encodeByHash(message.encode('utf-8'),self.chatsPasswords[str(chatId)]+encryptId,10).hex()
        elif encryptId is None:
            encryptId=""
        return self.apiReq('editMessage',getData="&chatId="+str(chatId)+"&msgId="+str(msgId),
                           postData={'message':message,'attachments':json.dumps(attachments),'encryptId':encryptId})
    
    def getMessage(self,chatId:int,msgId:int):
        out=self.apiReq('getMessage',getData='&chatId='+str(chatId)+"&msgId="+str(msgId))
        if(out['errorCode']==0):
            msg=out['msg']
            if str(msg['fromChat']) in self.chatsPasswords:
                msg['message']=self.he.decodeByHash(bytes.fromhex(msg['message']),self.chatsPasswords[str(msg['fromChat'])]+msg['encryptId'],10).decode("utf-8")
                if(msg['answerMsg']!='-1'):
                    msg['answerMsgText']=self.he.decodeByHash(bytes.fromhex(msg['answerMsgText']),self.chatsPasswords[str(msg['fromChat'])]+msg['answerMsgEncryptId'],10).decode("utf-8")
            return msg
        return None

    def setMenu(self,chatId:int,menu:list):
        return self.apiReq('setMenu',getData="&chatId="+str(chatId),postData={'menu':json.dumps(menu)})
    
    def execHDB(self,chatId:int,query:str):
        return self.apiReq('execHDB','&chatId='+chatId,{'query':json.dumps({'exec':exec})})
    
    def getBotsMessages(self,fromId:int=-1):
        return self.apiReq('getBotsMessages','&fromId='+('' if fromId<=0 else str(fromId)))
    
    #protocol messages between app and bot
    def sendBotMessage(self,toId:int,data:str):
        return self.apiReq('sendBotMessage','&toId='+str(toId),{'data':data})

    def printDebug(self,s:str):
        if(self.log_level>1):
            print("D:",s)
    
    def printError(self,s:str):
        if(self.log_level>0):
            print("E:",s)

    #WebSockets

    #Connect to HalChat WS
    #ping for alive connection
    async def keep_alive(self):
        while self.isRun:
            try:
                if self.ws:
                    await self.ws.send("ping")
            except Exception as e:
                self.printError(f"Error ping: {e}")
            await asyncio.sleep(1800)

    async def connect(self):
        while self.isRun:
            try:
                self.ws=await websockets.connect(self.ws_url)
                await self.auth()
                self.printDebug("Connected to HalChat WS")
                asyncio.create_task(self.keep_alive())
                await self.listen()
            except websockets.ConnectionClosed:
                self.printError("Connection closed, reconnecting...")
                await asyncio.sleep(5)
            except Exception as e:
                self.printError(f"Error WebSocket: {e}")
                await asyncio.sleep(5)

    #Auth WS HalNet
    async def auth(self):
        auth_payload={"action":"authBot","token":self.code}
        await self.ws.send(json.dumps(auth_payload))
        response=await self.ws.recv()
        self.printDebug("Auth response - "+response)


    #list new messages WS
    async def listen(self):
        async for message in self.ws:
            if(message=="pong"):
                continue
            data=json.loads(message)
            await self.handle_event(data)

    #Process message
    async def handle_event(self,data):
        event_type=data.get("rtype")

        if event_type=="msg":
            msg=data
            #self.chats[str(msg['fromChat'])][0]=msg['uid']
            if str(msg['fromChat']) in self.chatsPasswords:
                msg['message']=self.he.decodeByHash(bytes.fromhex(msg['message']),self.chatsPasswords[str(msg['fromChat'])]+msg['encryptId'],10).decode("utf-8")
                if(msg['answerMsg']!='-1'):
                    msg['answerMsgText']=self.he.decodeByHash(bytes.fromhex(msg['answerMsgText']),self.chatsPasswords[str(msg['fromChat'])]+msg['answerMsgEncryptId'],10).decode("utf-8")
            self.run_event("onNewMessage",[msg,str(msg['fromChat']) in self.chatsPasswords])
        elif event_type=="act":
            v=data
            #self.chats[str(v['fromChat'])][1]=v['uid']
            if v['type']==0:
                self.run_event('onDeleteMessage',[v['fromChat'],v['fromId'],v['fromMsg']])
            elif v['type']==1:
                self.run_event('onEditMessage',[v['fromChat'],v['fromId'],v['fromMsg']])
            elif v['type']==2:
                if str(v['fromChat']) in self.requested_passwords:
                    passw=self.requested_passwords[str(v['fromChat'])].decrypt(base64.b64decode(v['data'])).decode('utf-8')
                    self.addChatPassword(v['fromChat'],passw)
                    self.savePasswords()
                    v['data']=passw
                    del self.requested_passwords[v['fromChat']]
                self.run_event('onReceivePassword',[v['fromChat'],v['fromId'],v['data']])
            elif v['type']==3:
                if v['toId']==self.botId:
                    if self.auto_join_chats:
                        self.joinChatByInviteId(v['uid'])
                    self.run_event('onNewChat',[v['fromChat'],v['fromId'],v['uid']])
            elif v['type']==6:
                self.run_event('onClickButton',[v['fromChat'],v['fromId'],v['fromMsg'],v['data']])
        elif event_type=="botmsg":
            if self.check_bots_messages:
                msg=data
                self.run_event('onBotMessage',[msg['fromId'],msg['time'],msg['data']])