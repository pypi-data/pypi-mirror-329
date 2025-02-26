import logging, traceback, threading, asyncio, json
import requests
from functools import wraps
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# Logging configuration
logger = logging.getLogger("TgrEzLi")
logger.setLevel(logging.DEBUG)
_file_handler = logging.FileHandler("TgrEzLi.log", encoding="utf-8")
_file_handler.setLevel(logging.DEBUG)
_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s - %(message)s")
_file_handler.setFormatter(_formatter)
logger.addHandler(_file_handler)
_console_handler = logging.StreamHandler()
_console_handler.setLevel(logging.INFO)
_console_handler.setFormatter(_formatter)
logger.addHandler(_console_handler)

# Thread-local storage
import threading
_local = threading.local()

class _TgMsgData:
    def __init__(self, text, msg_id, chat_id, user_id, user_name, timestamp, raw_update):
        self.text = text
        self.msgId = msg_id
        self.chatId = chat_id
        self.userId = user_id
        self.userName = user_name
        self.timestamp = timestamp
        self.raw_update = raw_update

class _TgCmdData:
    def __init__(self, command, args, msg_id, chat_id, user_id, user_name, timestamp, raw_update):
        self.command = command
        self.args = args
        self.msgId = msg_id
        self.chatId = chat_id
        self.userId = user_id
        self.userName = user_name
        self.timestamp = timestamp
        self.raw_update = raw_update

class _TgCbData:
    def __init__(self, text, value, msg_id, chat_id, user_id, user_name, timestamp, raw_update):
        self.text = text
        self.value = value
        self.msgId = msg_id
        self.chatId = chat_id
        self.userId = user_id
        self.userName = user_name
        self.timestamp = timestamp
        self.raw_update = raw_update

class _TgArgsData:
    def __init__(self, data_dict: dict):
        self._data = data_dict
    def get(self, key, default=None):
        return self._data.get(key, default)

class _TgMsgProxy:
    def __getattr__(self, item):
        if not hasattr(_local, "TgMsg") or _local.TgMsg is None:
            raise AttributeError("TgMsg not available in this context.")
        return getattr(_local.TgMsg, item)

class _TgCmdProxy:
    def __getattr__(self, item):
        if not hasattr(_local, "TgCmd") or _local.TgCmd is None:
            raise AttributeError("TgCmd not available in this context.")
        return getattr(_local.TgCmd, item)

class _TgCbProxy:
    def __getattr__(self, item):
        if not hasattr(_local, "TgCb") or _local.TgCb is None:
            raise AttributeError("TgCb not available in this context.")
        return getattr(_local.TgCb, item)

class _TgArgsProxy:
    def __getattr__(self, item):
        if not hasattr(_local, "TgArgs") or _local.TgArgs is None:
            raise AttributeError("TgArgs not available in this context.")
        return getattr(_local.TgArgs, item)

TgMsg = _TgMsgProxy()
TgCmd = _TgCmdProxy()
TgCb = _TgCbProxy()
TgArgs = _TgArgsProxy()

class TEL:
    def __init__(self):
        self.chat_ids = {}
        self.default_chat_name = None
        self._message_handlers = []
        self._command_handlers = {}
        self._callback_handlers = []
        self._api_routes = {}
        self._api_server_thread = None
        self._api_server_running = False

        self.application = None
        self._loop = None
        self._polling_thread = None
        self._connected = False

        self._save_log = True
        self._api_host = "localhost"
        self._api_port = 8080
        printBanner('TgrEzLi', 'v0.1.1', 'by eaannist', '█')

    def setSaveLog(self, flag: bool):
        self._save_log = flag
        if not flag:
            if _file_handler in logger.handlers:
                logger.removeHandler(_file_handler)
        else:
            if _file_handler not in logger.handlers:
                logger.addHandler(_file_handler)

    def setHost(self, host: str):
        self._api_host = host

    def setPort(self, port: int):
        self._api_port = port

    def connect(self, token, chat_dict: dict):
        logger.info("Initialyzing BOT...")
        if not chat_dict:
            raise ValueError("Chat dictionary is empty.")
        self.chat_ids = {str(k): str(v) for k, v in chat_dict.items()}
        self.default_chat_name = next(iter(self.chat_ids))
        self._loop = asyncio.new_event_loop()
        self.application = ApplicationBuilder().token(token).build()
        self.application.add_handler(MessageHandler(filters.COMMAND, self._command_handler), group=0)
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._message_handler), group=1)
        self.application.add_handler(CallbackQueryHandler(self._callback_handler), group=2)
        self.application.add_error_handler(self._error_handler)
        self._polling_thread = threading.Thread(target=self._run_loop, daemon=True)
        self._polling_thread.start()
        self._connected = True
        logger.info("BOT Connected and polling activated.")

    def _run_loop(self):
        try:
            asyncio.set_event_loop(self._loop)
            logger.info("Starting run_polling() thread...")
            self._loop.run_until_complete(self.application.run_polling())
        except Exception as e:
            logger.error(f"Error while run_polling(): {e}")
            logger.debug(traceback.format_exc())
        finally:
            logger.info("Closing event loop.")
            self._loop.run_until_complete(self.application.shutdown())
            self._loop.close()

    async def _message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message: return
        chat_id = str(update.effective_chat.id)
        chat_name = self._get_chat_name_by_id(chat_id)
        if not chat_name: return
        text = update.message.text or ""
        tgmsg_data = _TgMsgData(text, update.message.message_id, chat_id,
                                 update.effective_user.id if update.effective_user else None,
                                 update.effective_user.username if update.effective_user else None,
                                 update.message.date, update)
        for (chats, func) in self._message_handlers:
            if chat_name in chats:
                self._call_user_function(func, TgMsg=tgmsg_data)

    async def _command_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message: return
        text = update.message.text or ""
        parts = text.strip().split(maxsplit=1)
        command_part = parts[0].lower()
        args_part = parts[1] if len(parts) > 1 else ""
        if '@' in command_part:
            command_part = command_part.split('@',1)[0]
        command_name = command_part.lstrip("/")
        chat_id = str(update.effective_chat.id)
        chat_name = self._get_chat_name_by_id(chat_id)
        if not chat_name: return
        tgcmd_data = _TgCmdData(command_part, args_part, update.message.message_id, chat_id,
                                    update.effective_user.id if update.effective_user else None,
                                    update.effective_user.username if update.effective_user else None,
                                    update.message.date, update)
        if command_name in self._command_handlers:
            for (chats, func) in self._command_handlers[command_name]:
                if chat_name in chats:
                    self._call_user_function(func, TgCmd=tgcmd_data)

    async def _callback_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.callback_query: return
        chat_id = str(update.effective_chat.id)
        chat_name = self._get_chat_name_by_id(chat_id)
        if not chat_name: return
        cb_query = update.callback_query
        button_text = None
        if cb_query.message and cb_query.message.reply_markup:
            for row in cb_query.message.reply_markup.inline_keyboard:
                for btn in row:
                    if btn.callback_data == cb_query.data:
                        button_text = btn.text; break
        tgcb_data = _TgCbData(button_text, cb_query.data, 
                               cb_query.message.message_id if cb_query.message else None,
                               chat_id,
                               cb_query.from_user.id if cb_query.from_user else None,
                               cb_query.from_user.username if cb_query.from_user else None,
                               cb_query.message.date if cb_query.message else None,
                               update)
        await cb_query.answer()
        for (chats, func) in self._callback_handlers:
            if chat_name in chats:
                self._call_user_function(func, TgCb=tgcb_data)

    def onMessage(self, chat=None):
        def decorator(func):
            self._message_handlers.append((self._parse_chat(chat), func))
            return func
        return decorator

    def onCommand(self, command, chat=None):
        cmd = command.lstrip("/")
        def decorator(func):
            self._command_handlers.setdefault(cmd, []).append((self._parse_chat(chat), func))
            return func
        return decorator

    def onCallback(self, chat=None):
        def decorator(func):
            self._callback_handlers.append((self._parse_chat(chat), func))
            return func
        return decorator

    def onApiReq(self, endpoint, args=None, host=None, port=None):
        if args is None: args = []
        host = host or self._api_host
        port = port or self._api_port
        def decorator(func):
            self._api_routes[endpoint] = {"args": args, "func": func}
            if not self._api_server_running:
                self._start_api_server(host, port)
            return func
        return decorator

    def sendMsg(self, text, chat=None):
        self._send(self.application.bot.send_message, {"text": text}, chat)

    def replyToMsg(self, text, msg_id, chat=None):
        self._send(self.application.bot.send_message, {"text": text, "reply_to_message_id": msg_id}, chat)

    def sendImg(self, photo_path, caption=None, chat=None):
        self._send(self.application.bot.send_photo, {"photo": photo_path, "caption": caption}, chat)

    def sendFile(self, file_path, caption=None, chat=None):
        self._send(self.application.bot.send_document, {"document": file_path, "caption": caption}, chat)

    def sendPosition(self, latitude, longitude, chat=None):
        self._send(self.application.bot.send_location, {"latitude": latitude, "longitude": longitude}, chat)

    def sendButtons(self, text, buttons, chat=None):
        kb = [[InlineKeyboardButton(btn["text"], callback_data=btn["value"]) for btn in row] for row in buttons]
        markup = InlineKeyboardMarkup(kb)
        self._send(self.application.bot.send_message, {"text": text, "reply_markup": markup}, chat)

    def _send(self, send_func, params: dict, chat):
        if not self._connected:
            raise RuntimeError("Not connected. Use connect() before using other methods.")
        for chat_name in self._parse_chat(chat):
            if chat_name not in self.chat_ids:
                logger.error(f"Chat '{chat_name}' not found. Not sent.")
                continue
            params["chat_id"] = self.chat_ids[chat_name]
            coro = send_func(**params)
            asyncio.run_coroutine_threadsafe(coro, self._loop)

    def sendLog(self, limit=None, chat=None):
        try:
            with open("TgrEzLi.log", "r", encoding="utf-8") as f:
                lines = f.readlines()
            text = "".join(lines[-limit:]) if limit else "".join(lines)
        except Exception as e:
            text = f"Errore nella lettura del log: {e}"
        self.sendMsg(text, chat)

    def sendInfo(self, chat=None):
        info = "Bot Info:\n"
        info += f"Chat IDs: {self.chat_ids}\n"
        info += f"onMessage handlers: {len(self._message_handlers)}\n"
        info += f"onCommand handlers: { {cmd: len(funcs) for cmd, funcs in self._command_handlers.items()} }\n"
        info += f"onCallback handlers: {len(self._callback_handlers)}\n"
        info += f"API Routes: {list(self._api_routes.keys())}\n"
        info += f"API Server: {self._api_host}:{self._api_port}\n"
        info += f"Salvataggio Log: {self._save_log}"
        self.sendMsg(info, chat)

    def sendRegisteredHandlers(self, chat=None):
        txt = "Handlers registrati:\n\nonMessage:\n"
        for chats, func in self._message_handlers:
            txt += f" - {func.__name__} su {chats}\n"
        txt += "\nonCommand:\n"
        for cmd, lst in self._command_handlers.items():
            for chats, func in lst:
                txt += f" - /{cmd} -> {func.__name__} su {chats}\n"
        txt += "\nonCallback:\n"
        for chats, func in self._callback_handlers:
            txt += f" - {func.__name__} su {chats}\n"
        txt += "\nAPI Routes:\n"
        for route in self._api_routes:
            txt += f" - {route}\n"
        self.sendMsg(txt, chat)

    def _parse_chat(self, chat):
        if chat is None:
            return {self.default_chat_name}
        elif isinstance(chat, str):
            return {chat}
        elif isinstance(chat, (list, tuple, set)):
            return set(chat)
        else:
            raise ValueError(f"Invalid parameter: {chat}")

    def _get_chat_name_by_id(self, chat_id):
        for name, cid in self.chat_ids.items():
            if cid == chat_id:
                return name
        return None

    def _call_user_function(self, func, TgMsg=None, TgCmd=None, TgCb=None, TgArgs=None):
        def worker():
            try:
                _local.TgMsg = TgMsg; _local.TgCmd = TgCmd; _local.TgCb = TgCb; _local.TgArgs = TgArgs
                func()
            except Exception as e:
                logger.error(f"User handler error: {e}")
                logger.debug(traceback.format_exc())
            finally:
                _local.TgMsg = _local.TgCmd = _local.TgCb = _local.TgArgs = None
        threading.Thread(target=worker, daemon=True).start()

    async def _error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        logger.error("Unmanaged error!")
        logger.error(context.error)
        logger.debug(traceback.format_exc())

    def _start_api_server(self, host, port):
        self._api_server_running = True
        class _ApiRequestHandler(BaseHTTPRequestHandler):
            def do_POST(self_inner):
                path = self_inner.path
                length = int(self_inner.headers.get('Content-Length', 0))
                raw_body = self_inner.rfile.read(length) if length > 0 else b''
                try:
                    data = json.loads(raw_body.decode('utf-8'))
                except:
                    data = {}
                if path in self._api_routes:
                    route_info = self._api_routes[path]
                    func = route_info["func"]
                    TgArgsDataObj = _TgArgsData(data)
                    self._call_user_function(func, TgArgs=TgArgsDataObj)
                    self_inner.send_response(200)
                    self_inner.send_header("Content-type", "application/json; charset=utf-8")
                    self_inner.end_headers()
                    resp = {"status": "ok", "path": path, "data_received": data}
                    self_inner.wfile.write(json.dumps(resp).encode('utf-8'))
                else:
                    self_inner.send_response(404)
                    self_inner.send_header("Content-type", "application/json; charset=utf-8")
                    self_inner.end_headers()
                    resp = {"status": "error", "message": "Route not found"}
                    self_inner.wfile.write(json.dumps(resp).encode('utf-8'))
        def serve_forever():
            class ReusableHTTPServer(HTTPServer):
                allow_reuse_address = True
            with ReusableHTTPServer((host, port), _ApiRequestHandler) as httpd:
                logger.info(f"HTTP API listening on http://{host}:{port}")
                httpd.serve_forever()
        self._api_server_thread = threading.Thread(target=serve_forever, daemon=True)
        self._api_server_thread.start()

class TReq:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self._host = "localhost"
        self._port = 9999
        self._body = {}

    def host(self, host: str):
        self._host = host
        return self

    def port(self, port: int):
        self._port = port
        return self

    def arg(self, name: str, value):
        self._body[name] = value
        return self

    def body(self, body_dict: dict):
        self._body = body_dict
        return self

    def send(self):
        url = f"http://{self._host}:{self._port}{self.endpoint}"
        try:
            response = requests.post(url, json=self._body)
            return response
        except Exception as e:
            raise Exception(f"Error sending request {url}: {e}")

def printBanner(nome, versione, autore, filler):
    versione_width = len(versione)
    inner_width = max(len(nome) + versione_width, len(f">> {autore}")) + 4
    border = '    ' + filler * (inner_width + 4)
    line2 = f"    {filler}{filler} {nome.ljust(inner_width - versione_width -2)}{versione.rjust(versione_width-2)} {filler}{filler}"
    line3 = f"    {filler}{filler} {f">> {autore}".rjust(inner_width-2)} {filler}{filler}"
    banner = f"\n{border}\n{line2}\n{line3}\n{border}\n"
    print(banner)