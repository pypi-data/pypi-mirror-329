import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from HalChatAPI import *

hca=HalChatAPI("hBfWguy2XqgTbS852z71alaQSWaCyxcOgD7jCLMK1icfWiHpfMEWqidNtgSqppsCV0DoVSuEIb3a0FB3bmB0sUqfa2OjVJpFZcSz")

@hca.event('onNewMessage')
async def on_new_message(msg,isExistPassword):
    if not isExistPassword:
        hca.requestPassword(msg['fromChat'])
        return
    chatId=str(msg['fromChat'])
    print(msg['message'])

@hca.event('onNewChat')
async def on_new_chat(chatId,fromId,inviteId):
    hca.requestPassword(chatId)

@hca.event('onReceivePassword')
async def on_receive_password(chatId,fromId,password):
    hca.sendMessage(chatId,'Бот успешно инициализирован.')

if __name__ == "__main__":
    hca.run()