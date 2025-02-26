# TgrEzLi

**TgrEzLi** is a Python library based [telegram-bot](https://pypi.org/project/python-telegram-bot/) that simplifies Telegram bot development by providing a synchronous interface, runs in background with non-blocking operations and offers intuitive handlers for messages, commands, callbacks, and API requests.

## Installation

```bash
pip install TgrEzLi

```
## Usage

```python

# Importing the library
from TgrEzLi import TEL, TgMsg, TgCmd, TgCb, TgArgs, TReq
# or
from TgrEzLi import *

# Initialization
bot = TEL()

# Some options
# Activate/Deactivate log saving
bot.setSaveLog(True)

# Set custom HTTP host and port; by default they are "localhost" and 9999
bot.setHost("127.0.0.1")
bot.setPort(8080)

# Connecting
# You can connect one or multiple chats
TOKEN = "123456789:ABCDEFGHIJKLMNO"
CHAT_ID = {
    "chat1": "123456789",
    "chat2": "789456123"
}

bot.connect(TOKEN, CHAT_ID)

# Basic commands to send Messages, Images, Files, Position, Log, Handlers, Bot Info
# Each method has a chat parameter, by defailt it's set to the first chat added to the dictionary
# You can either insert a specific chat name or a List 
bot.sendMsg(text, chat)
bot.sendImg(photo_path, caption, chat)
bot.sendFile(file_path, caption, chat)
bot.sendPosition(latitude, longitude, chat)
bot.replyToMsg(text, msg_id, chat_id)
bot.sendLog(limit, chat)
bot.sendInfo(chat)
bot.sendRegisteredHandlers(chat)

# Methods to create and send Inline Keyboards (simply called Buttons)
bot.sendButtons(text, buttons, chat)

# Handlers for Messages, Commands, and Callbacks
# Each method has a chat parameter, by defailt it's set to the first chat added to the dictionary
# You can either insert a specific chat name or a List 
@bot.onMessage(chat)
@bot.onCommand(command, chat)
@bot.onCallback(chat)
@bot.onApiReq(endpoint, args, host, port)

# Data Interfaces
# Each Handler has it's own integrated interface to easly access received data

# TgMsg gets received messages data for .onMessage() handler
TgMsg.text
    .msgId
    .chatId
    .userId
    .userName
    .timestamp
    .raw_update 

# TgCmd gets data and parameters for .onCommand() handler
TgCmd.command
    .args       # gives text outside the command
    .msgId
    .chatId
    .userId
    .userName
    .timestamp
    .raw_update

# TgCb gets data for .onCallback() handler
TgCb.text
    .value
    .msgId
    .chatId
    .userId
    .userName
    .timestamp
    .raw_update

# TgArgs gets parameters for .onApiReq() handler
TgArgs.get(key, default)


# Treq makes it really easy to send an api request
# It takes the endpoint path like "\action"
# .host and .port are optional, by default "localhost" and 9999
# you can add multiple .arg() methods to add parameters names and values
# or you can use .body() to send the full body
TReq(endpoint)\
    .host(host)\
    .port(port)\
    .arg(name, value)\
    .body(body_dict)\
    .send()

## Examples ##

# basic commands
bot.sendMsg("Message Test")
bot.sendImg("img.jpg", "Image Test", 'chat1')
bot.sendFile("file.pdf", "File Test", ['chat1', 'chat2'])
bot.sendPosition(45.4642, 9.1900, ['chat1', 'chat2'])


# Message Handler
@bot.onMessage()
def on_message_default_chat():
    bot.sendMsg(f"Hi {TgMsg.userName}! You wrote: {TgMsg.text}")
    reply = f"Message Id: {TgMsg.msgId} User Id: {TgMsg.userId} Raw: {TgMsg.raw_update}"
    bot.replyToMsg(reply, msg_id=TgMsg.msgId)


# Command Handler
@bot.onCommand("/start")
def handle_start():
    bot.sendMsg(f"Welcome to chat 1 {TgCmd.userName}!")
    if TgCmd.args : bot.sendMsg(f"You also wrote: {TgCmd.args}!")

@bot.onCommand("/start", 'chat2')
def handle_start():
    bot.sendMsg(f"Welcome to chat 2 {TgCmd.userName}!")


# Buttons
@bot.onCommand("/buttons", 'chat1')
def show_buttons():
    buttons = [
        [{"text": "Button 1", "value": "red"}],
        [{"text": "Button 2", "value": "yellow"}]
    ]
    bot.sendButtons("Scegli un colore:", buttons, "chat1")

# Callback Handler
@bot.onCallback("chat1")
def on_callback_chat1():
    match TgCb.value:
        case "red":
            bot.sendMsg(f"You pressed {TgCb.text} -> {TgCb.value}!", "chat1")
        case "yellow":
            bot.sendMsg(f"You pressed {TgCb.text} -> {TgCb.value}!", "chat1")


# Api Requests
@bot.onApiReq('/action', args=['chat','msg'])
def action():
    id = TgArgs.get('chat')
    msg = TgArgs.get('msg')
    bot.sendMsg(msg, id)

# TReq usage
TReq('/action')\
    .host('127.0.0.1')\
    .port(8080)\
    .arg('chat_id', 'chat1')\
    .arg('msg', 'Hello from TReq!')\
    .send()

```

## Development status

**TgrEzLi** is a work-in-progress personal project. Suggestions, feature requests, and constructive feedback are highly welcome. Feel free to open an issue or submit a pull request.