from .network.connection import Connection
from .objects.objs import *
from json import dumps
from time import sleep
from typing import Literal
import asyncio

message_types = Literal[
    'message',
    'photo',
    'video',
    'audio',
    'voice',
    'sticker',
    'document',
    'callback_query'
]

class UnexceptedServerError(Exception):...
class ChatNotFoundError(Exception):...
class PermissionDenied(Exception):...

class Client(object):
    def __init__(
        self,
        BotToken: str
    ):
        self.token = BotToken
        self.connection = Connection(self.token)
        self.handlers = []

    def getMe(self) -> User:
        _ = self.connection.createConnection("getMe")
        if _['ok']:
            return User(_['result'])
        
        raise UnexceptedServerError(dumps(_, ensure_ascii=False))
    
    def logout(self) -> dict:
        return self.connection.createConnection("logout")
    
    def close(self) -> dict:
        return self.connection.createConnection("close")
    
    def sendMessage(
        self,
        chat_id: Union[str, int],
        text: str,
        reply_to_message_id: int = None,
        reply_markup: Union[ InlineKeyboardMarkup, KeyboardMarkup ] = None
    ) -> SendMessage:
        
        _ = self.connection.createConnection(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": text,
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": None if reply_markup is None else {
                    "inline_keyboard" if isinstance(reply_markup, InlineKeyboardMarkup) else "keyboard": reply_markup.keybuttons
                }
            }
        )

        if _['ok']:return SendMessage(_)
        else:raise UnexceptedServerError(dumps(_, ensure_ascii=False))

    def getUpdates(
        self,
        offset: int = 0,
        limit: int = 1
    ):
        
        _ = self.connection.createConnection("getUpdates", { "offset": offset, "limit": limit })
        if _['ok']: return _['result'] #return Message(self.token, _['result'][0])
        else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

    def getRawUpdates(
        self,
        offset: int = 0,
        limit: int = 1
    ):
        
        _ = self.connection.createConnection("getUpdates", { "offset": offset, "limit": limit })
        if _['ok']: return _
        else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

    def forwardMessage(
        self,
        chat_id: Union[str, int],
        from_chat_id: Union[str, int],
        message_id: int
    ):
        
        _ = self.connection.createConnection(
            "forwardMessage",
            {
                "chat_id": chat_id,
                "from_chat_id": from_chat_id,
                "message_id": message_id
            }
        )

        if _['ok']: return ForwardMessage(_['result'])
        else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

    def sendPhoto(
        self,
        chat_id: Union[str, int],
        photos: Union[str, list],
        caption: str = "",
        reply_to_message_id: int = None,
        reply_markup: ReplyKeyboardMarkup = None
    ):
        
        if isinstance(photos, str):
            _ = self.connection.uploadSomething(
                photos,
                "photo",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup
            )

            if _['ok']: return [PhotoSize(ph) for ph in _['result']['photo']]
            else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

        elif isinstance(photos, list):
            states = {}

            for photo in photos:
                _ = self.connection.uploadSomething(
                photos,
                "photo",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup
            )

                if _['ok']: states[photo] = [PhotoSize(ph) for ph in _['result']['photo']]
                else: states[photo] = _
            
            return states
        else: raise ValueError("Invalid data type")

    def sendAudio(
        self,
        chat_id: Union[str, int],
        audios: Union[str, list],
        caption: str = "",
        reply_to_message_id: int = None,
        reply_markup: ReplyKeyboardMarkup = None
    ):
        
        if isinstance(audios, str):
            _ = self.connection.uploadSomething(
                audios,
                "audio",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup
            )

            if _['ok']: return Audio(_['result']['audio'])
            else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

        elif isinstance(audios, list):
            states = {}

            for audio in audios:
                _ = self.connection.uploadSomething(
                audios,
                "audio",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup
            )

                if _['ok']: states[audio] = Audio(_['result']['audio'])
                else: states[audio] = _
            
            return states
        else: raise ValueError("Invalid data type")

    def sendDocument(
        self,
        chat_id: Union[str, int],
        documents: Union[str, list],
        caption: str = "",
        reply_to_message_id: int = None,
        reply_markup: ReplyKeyboardMarkup = None
    ):
        
        if isinstance(documents, str):
            _ = self.connection.uploadSomething(
                documents,
                "document",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup
            )
            
            if _['ok']: return Document(_['result']['document'])
            else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

        elif isinstance(documents, list):
            states = {}

            for document in documents:
                _ = self.connection.uploadSomething(
                documents,
                "document",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup
            )

                if _['ok']: states[document] = Document(_['result']['document'])
                else: states[document] = _
            
            return states
        else: raise ValueError("Invalid data type")

    def sendVideo(
        self,
        chat_id: Union[str, int],
        videos: Union[str, list],
        caption: str = "",
        reply_to_message_id: int = None,
        reply_markup: ReplyKeyboardMarkup = None
    ):
        
        if isinstance(videos, str):
            _ = self.connection.uploadSomething(
                videos,
                "video",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup
            )

            if _['ok']: return Video(_['result']['video'])
            else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

        elif isinstance(videos, list):
            states = {}

            for video in videos:
                _ = self.connection.uploadSomething(
                videos,
                "video",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup
            )

                if _['ok']: states[video] = Video(_['result']['video'])
                else: states[video] = _
            
            return states
        else: raise ValueError("Invalid data type")

    def sendAnimation(
        self,
        chat_id: Union[str, int],
        animations: Union[str, list],
        caption: str = "",
        reply_to_message_id: int = None,
        reply_markup: ReplyKeyboardMarkup = None
    ):
        
        if isinstance(animations, str):
            _ = self.connection.uploadSomething(
                animations,
                "animation",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup
            )

            if _['ok']: return Animation(_['result']['animation'])
            else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

        elif isinstance(animations, list):
            states = {}

            for animation in animations:
                _ = self.connection.uploadSomething(
                animations,
                "animation",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup
            )

                if _['ok']: states[animation] = Animation(_['result']['animation'])
                else: states[animation] = _
            
            return states
        else: raise ValueError("Invalid data type")

    def sendVoice(
        self,
        chat_id: Union[str, int],
        voices: Union[str, list],
        caption: str = "",
        reply_to_message_id: int = None,
        reply_markup: ReplyKeyboardMarkup = None
    ):
        
        if isinstance(voices, str):
            _ = self.connection.uploadSomething(
                voices,
                "voice",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup
            )

            if _['ok']: return Voice(_['result']['voice'])
            else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

        elif isinstance(voices, list):
            states = {}

            for voice in voices:
                _ = self.connection.uploadSomething(
                voices,
                "voice",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup
            )

                if _['ok']: states[voice] = Voice(_['result']['voice'])
                else: states[voice] = _
            
            return states
        else: raise ValueError("Invalid data type")

    def sendLocation(
        self,
        chat_id: Union[str, int],
        latitude: float,
        longitude: float,
        horizontal_accuracy: float = None,
        reply_to_message_id: int = None,
        reply_markup: Union[ ReplyKeyboardMarkup, InlineKeyboardMarkup ] = None
    ):
        
        _ = self.connection.createConnection(
            "sendLocation",
            {
                "chat_id": chat_id,
                "latitude": latitude,
                "longitude": longitude,
                "horizontal_accuracy": horizontal_accuracy,
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": None if reply_markup is None else reply_markup.keybuttons
            }
        )

        if _['ok']: return Location(_['result']['location'])
        else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

    def sendContact(
        self,
        chat_id: Union[int, str],
        phone_number: str,
        first_name: str,
        last_name: str = None,
        reply_to_message_id: int = None,
        reply_markup: Union[ ReplyKeyboardMarkup, InlineKeyboardMarkup ] = None
    ):
        
        _ = self.connection.createConnection(
            "sendContact",
            {
                "chat_id": chat_id,
                "phone_number": phone_number,
                "first_name": first_name,
                "last_name": last_name,
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": None if reply_markup is None else reply_markup.keybuttons
            }
        )

        if _['ok']: return Contact(_['result']['contact'])
        else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

    def getFile(
        self,
        file_id: str
    ):
        
        _ = self.connection.createConnection(
            "getFile",
            {
                "file_id": file_id
            }
        )

        if _['ok']:return File(_['result'])
        else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

    def downloadFile(
        self,
        file_path: str,
        save_in_path: str
    ):
        try:
            content = self.connection._sync.get(
                self.connection.file_url+file_path
            ).text

            if not os.path.exists(save_in_path):open(save_in_path, 'a')
            open(save_in_path, "wb").write(content.encode())
            return { "ok": True }
        except Exception as ErrorWriting:
            return { "ok": False, "message": ErrorWriting }
        
    def getFileContent(
        self,
        file_path: str,
    ):
        return self.connection._sync.get(
                self.connection.file_url+file_path
            ).text
        
    def banChatMember(
        self,
        chat_id: Union[str, int],
        user_id: Union[str, int]
    ):
        
        _ = self.connection.createConnection(
            "banChatMember",
            {
                "chat_id": chat_id,
                "user_id": user_id
            }
        )

        if _['ok'] != True:
            if _['description'] == "Bad Request: message not found":
                raise ChatNotFoundError(f"Chat not found `{chat_id}`")
            elif _['description'] == "Forbidden: permission_denied":
                raise PermissionDenied("You do not have this premission to use")
        else:
            return _
        
    def unbanChatmember(
        self,
        chat_id: Union[str, int],
        user_id: Union[str, int],
        only_if_banned: bool = True
    ):
        
        _ = self.connection.createConnection(
            "unbanChatMember",
            {
                "chat_id": chat_id,
                "user_id": user_id,
                "only_if_banned": only_if_banned
            }
        )

        if _['ok'] != True:
            if _['description'] == "Bad Request: message not found":
                raise ChatNotFoundError(f"Chat not found `{chat_id}`")
            elif _['description'] == "Forbidden: permission_denied":
                raise PermissionDenied("You do not have this premission to use")
        else:
            return _
        
    def promoteChatMember(
        self,
        chat_id: Union[str, int],
        user_id: Union[str, int],
        can_change_info: bool = False,
        can_post_messages: bool = False,
        can_edit_messages: bool = False,
        can_delete_messages: bool = False,
        can_manage_video_chats: bool = False,
        can_invite_users: bool = False,
        can_restrict_members: bool = False
    ):
        
        _ = self.connection.createConnection(
            "promoteChatMember",
            {
                "chat_id": chat_id,
                "user_id": user_id,
                "can_change_info": can_change_info,
                "can_post_messages": can_post_messages,
                "can_edit_messages": can_edit_messages,
                "can_delete_messages": can_delete_messages,
                "can_manage_video_chats": can_manage_video_chats,
                "can_invite_users": can_invite_users,
                "can_restrict_members": can_restrict_members
            }
        )

        return _
    
    def setChatPhoto(
        self,
        chat_id: Union[str, int],
        photo: str
    ):
        
        if photo.startswith("http"):
            return self.connection._sync.post(
                self.connection.url+"/setChatPhoto",
                params={
                    "chat_id": chat_id,
                    "photo": photo
                }
            )
        elif os.path.exists(photo) and os.path.isfile(photo):
            return self.connection._sync.post(
                self.connection.url+"/setChatPhoto",
                params={
                    "chat_id": chat_id
                },
                files={
                    "photo": open(photo, 'rb').read()
                }
            )

        else: raise ValueError("{} is not URL or Doesnt exist in your Local Storage".format(
            photo
        ))

    def leaveChat(
        self,
        chat_id: Union[str, int]
    ):
        
        return self.connection.createConnection(
            "leaveChat",
            {
                "chat_id": chat_id
            }
        )
    
    def getChat(
        self,
        chat_id: Union[str, int]
    ):
        
        _ = self.connection.createConnection(
            "getChat",
            {
                "chat_id": chat_id
            }
        )

        if _['ok']:return Chat(_['result'])
        else:raise UnexceptedServerError(dumps(_, ensure_ascii=False))

    def getChatMembersCount(
        self,
        chat_id: Union[str, int]
    ):
        
        return self.connection.createConnection(
            "getChatMembersCount",
            {
                "chat_id": chat_id
            }
        )
    
    def pinMessage(
        self,
        chat_id: Union[str, int],
        message_id: int
    ):
        
        return self.connection.createConnection(
            "pinChatMessage",
            {
                "chat_id": chat_id,
                "message_id": message_id
            }
        )
    
    def unpinMessage(
        self,
        chat_id: Union[str, int],
        message_id: int
    ):
        
        return self.connection.createConnection(
            "unpinChatMessage",
            {
                "chat_id": chat_id,
                "message_id": message_id
            }
        )
    
    def unpinAllMessage(
        self,
        chat_id: Union[str, int]
    ):
        
        return self.connection.createConnection(
            "unpinAllChatMessages",
            {
                "chat_id": chat_id
            }
        )
    
    def setChatTitle(
        self,
        chat_id: Union[str, int],
        title: str
    ):
        
        return self.connection.createConnection(
            "setChatTitle",
            {
                "chat_id": chat_id,
                "title": title
            }
        )
    
    def setChatDescription(
        self,
        chat_id: Union[str, int],
        description: str
    ):
        
        return self.connection.createConnection(
            "setChatDescription",
            {
                "chat_id": chat_id,
                "description": description
            }
        )
        
    def deleteChatPhoto(
        self,
        chat_id: Union[str, int]
    ):
        
        return self.connection.createConnection(
            "deleteChatPhoto",
            {
                "chat_id": chat_id
            }
        )
    
    def createInviteLink(
        self,
        chat_id: Union[str, int]
    ):
        
        return self.connection.createConnection(
            "createChatInviteLink",
            {
                "chat_id": chat_id
            }
        )
    
    def revokeInviteLink(
        self,
        chat_id: Union[str, int],
        previous_invite_link: str
    ):
        
        return self.connection.createConnection(
            "revokeChatInviteLink",
            {
                "chat_id": chat_id,
                "invite_link": previous_invite_link
            }
        )
    
    def exportInviteLink(
        self,
        chat_id: Union[str, int]
    ):
        
        return self.connection.createConnection(
            "exportChatInviteLink",
            {
                "chat_id": chat_id
            }
        )
    
    def editMessageText(
        self,
        chat_id: Union[str, int],
        text: str,
        message_id: int,
        reply_markup: InlineKeyboardMarkup = None
    ):
        
        _ = self.connection.createConnection(
            "editMessageText",
            {
                "chat_id": chat_id,
                "text": text,
                "message_id": message_id,
                "reply_markup": None if reply_markup is None else reply_markup.keybuttons
            }
        )

        if _['ok']:return Message(self.token, _['result'])
        else:raise UnexceptedServerError(dumps(_, ensure_ascii=False))

    def deleteMessage(
        self,
        chat_id: Union[str, int],
        message_id: int
    ):
        
        return self.connection.createConnection(
            "deleteMessage",
            {
                "chat_id": chat_id,
                "message_id": message_id
            }
        )
    
    def uploadStickerFile(
        self,
        user_id: int,
        sticker: str
    ):
        
        if sticker.startswith("http"):
            return self.connection._sync.post(
                self.connection.url+"/uploadStickerFile",
                params={
                    "user_id": user_id,
                    "sticker": sticker
                }
            )
        elif os.path.exists(sticker) and os.path.isfile(sticker):
            return self.connection._sync.post(
                self.connection.url+"/uploadStickerFile",
                params={
                    "user_id": user_id
                },
                files={
                    "sticker": open(sticker, 'rb').read()
                }
            )

        else: raise ValueError("{} is not URL or Doesnt exist in your Local Storage".format(
            sticker
        ))

    def createStickerSet(
        self,
        user_id: int,
        name: str,
        title: str,
        sticker: list = []
    ):
        
        return self.connection.createConnection(
            "createNewStickerSet",
            {
                "user_id": user_id,
                "name": name,
                "title": title,
                "sticker": sticker
            }
        )
    
    def addStickerToSet(
        self,
        user_id: int,
        name: str,
        sticker: str
    ):
        
        if sticker.startswith("http"):
            return self.connection._sync.post(
                self.connection.url+"/addStickerToSet",
                params={
                    "user_id": user_id,
                    "name": name,
                    "sticker": sticker
                }
            )
        elif os.path.exists(sticker) and os.path.isfile(sticker):
            return self.connection._sync.post(
                self.connection.url+"/addStickerToSet",
                params={
                    "user_id": user_id,
                    "name": name
                },
                files={
                    "sticker": open(sticker, 'rb').read()
                }
            )

        else: raise ValueError("{} is not URL or Doesnt exist in your Local Storage".format(
            sticker
        ))

    def on(
        self,
        type: message_types = 'message',
        offset: int = -1,
        limit: int = 1,
        sleep: int = 0
    ):
        def decorate(func):
            self.handlers.append(
                {
                    "function": func,
                    "offset": offset,
                    "limit": limit,
                    "type": type,
                    "sleep": sleep
                }
            )
            return func
        return decorate
    
    def run(self):
        msg_ids = set()
        query_ids = set()
        while 1:
            for handler in self.handlers:
                func = handler['function']
                limit = handler['limit']
                offset = handler['offset']
                _sleep = handler['sleep']
                _type: message_types = handler['type']

                _ = self.getUpdates(offset, limit)
                _msg = Message(self.token, _[0])

                if _type == "message":
                    if not _msg.message_id in msg_ids:
                        msg_ids.add(_msg.message_id)
                        func(_msg)

                elif _type == "photo":
                    if len(_msg.photo) > 0:
                        if not _msg.message_id in msg_ids:
                            msg_ids.add(_msg.message_id)
                            func(_msg)

                elif _type == "video":
                    if _msg.video.result != {} or _msg.document.mime_type.startswith("video"):
                        if not _msg.message_id in msg_ids:
                            msg_ids.add(_msg.message_id)
                            func(_msg)

                elif _type == "audio":
                    if _msg.document.mime_type.startswith("audio"):
                        if not _msg.message_id in msg_ids:
                            msg_ids.add(_msg.message_id)
                            func(_msg)

                elif _type == "sticker":
                    if _msg.sticker.result != {}:
                        if not _msg.message_id in msg_ids:
                            msg_ids.add(_msg.message_id)
                            func(_msg)

                elif _type == "voice":
                    if _msg.voice.result != {}:
                        if not _msg.message_id in msg_ids:
                            msg_ids.add(_msg.message_id)
                            func(_msg)

                elif _type == "document":
                    if _msg.document.result != {}:
                        if not _msg.message_id in msg_ids:
                            msg_ids.add(_msg.message_id)
                            func(_msg)

                elif _type == "callback_query":
                    if not _msg.callback_query.id == 0:
                        if not _msg.callback_query.inline_id in query_ids:
                            query_ids.add(_msg.callback_query.inline_id)
                            func(_msg)


                sleep(_sleep) if not _sleep == 0 else ...

class AsyncClient(object):
    def __init__(
        self,
        BotToken: str
    ):
        self.token = BotToken
        self.connection = Connection(self.token)
        self.handlers = []

    async def getMe(self) -> User:
        _ = await self.connection.createAsyncConnection("getMe")
        if _['ok']:
            return User(_['result'])
        
        raise UnexceptedServerError(dumps(_, ensure_ascii=False))
    
    async def logout(self) -> dict:
        return await self.connection.createAsyncConnection("logout")
    
    async def close(self) -> dict:
        return await self.connection.createAsyncConnection("close")
    
    async def sendMessage(
        self,
        chat_id: Union[str, int],
        text: str,
        reply_to_message_id: int = None,
        reply_markup: Union[ InlineKeyboardMarkup, KeyboardMarkup ] = None
    ) -> SendMessage:
        
        _ = await self.connection.createAsyncConnection(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": text,
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": None if reply_markup is None else {
                    "inline_keyboard" if isinstance(reply_markup, InlineKeyboardMarkup) else "keyboard": reply_markup.keybuttons
                }
            }
        )

        if _['ok']:return SendMessage(_)
        else:raise UnexceptedServerError(dumps(_, ensure_ascii=False))

    async def getUpdates(
        self,
        offset: int = -1,
        limit: int = 1
    ):
        
        _ = await self.connection.createAsyncConnection("getUpdates", { "offset": offset, "limit": limit })
        if _['ok']: return _['result'] #return Message(self.token, _['result'][0])
        else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

    async def getRawUpdates(
        self,
        offset: int = -1,
        limit: int = 1
    ):
        
        _ = await self.connection.createAsyncConnection("getUpdates", { "offset": offset, "limit": limit })
        if _['ok']: return _
        else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

    async def forwardMessage(
        self,
        chat_id: Union[str, int],
        from_chat_id: Union[str, int],
        message_id: int
    ):
        
        _ = await self.connection.createAsyncConnection(
            "forwardMessage",
            {
                "chat_id": chat_id,
                "from_chat_id": from_chat_id,
                "message_id": message_id
            }
        )

        if _['ok']: return ForwardMessage(_['result'])
        else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

    async def sendPhoto(
        self,
        chat_id: Union[str, int],
        photos: Union[str, list],
        caption: str = "",
        reply_to_message_id: int = None,
        reply_markup: ReplyKeyboardMarkup = None,
        filename: str = ""
    ):
        
        if isinstance(photos, str):
            _ = await self.connection.uploadAsyncSomething(
                photos,
                "photo",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup,
                filename
            )

            if _['ok']: return [PhotoSize(ph) for ph in _['result']['photo']]
            else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

        elif isinstance(photos, list):
            states = {}

            for photo in photos:
                _ = await self.connection.uploadAsyncSomething(
                photos,
                "photo",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup,
                filename
            )

                if _['ok']: states[photo] = [PhotoSize(ph) for ph in _['result']['photo']]
                else: states[photo] = _
            
            return states
        else: raise ValueError("Invalid data type")

    async def sendAudio(
        self,
        chat_id: Union[str, int],
        audios: Union[str, list],
        caption: str = "",
        reply_to_message_id: int = None,
        reply_markup: ReplyKeyboardMarkup = None,
        filename: str = ""
    ):
        
        if isinstance(audios, str):
            _ = await self.connection.uploadAsyncSomething(
                audios,
                "audio",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup,
                filename
            )

            if _['ok']: return Audio(_['result']['audio'])
            else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

        elif isinstance(audios, list):
            states = {}

            for audio in audios:
                _ = await self.connection.uploadAsyncSomething(
                audios,
                "audio",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup,
                filename
            )

                if _['ok']: states[audio] = Audio(_['result']['audio'])
                else: states[audio] = _
            
            return states
        else: raise ValueError("Invalid data type")

    async def sendDocument(
        self,
        chat_id: Union[str, int],
        documents: Union[str, list],
        caption: str = "",
        reply_to_message_id: int = None,
        reply_markup: ReplyKeyboardMarkup = None,
        filename: str = None
    ):
        
        if isinstance(documents, str):
            _ = await self.connection.uploadAsyncSomething(
                thing=documents,
                thing_type="document",
                chat_id=chat_id,
                caption=caption,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                filename=filename
            )
            
            if _['ok']: return Document(_['result']['document'])
            else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

        elif isinstance(documents, list):
            states = {}

            for document in documents:
                _ = await self.connection.uploadAsyncSomething(
                documents,
                "document",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup,
                filename
            )

                if _['ok']: states[document] = Document(_['result']['document'])
                else: states[document] = _
            
            return states
        else: raise ValueError("Invalid data type")

    async def sendVideo(
        self,
        chat_id: Union[str, int],
        videos: Union[str, list],
        caption: str = "",
        reply_to_message_id: int = None,
        reply_markup: ReplyKeyboardMarkup = None,
        filename: str = ""
    ):
        
        if isinstance(videos, str):
            _ = await self.connection.uploadAsyncSomething(
                videos,
                "video",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup,
                filename
            )

            if _['ok']: return Video(_['result']['video'])
            else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

        elif isinstance(videos, list):
            states = {}

            for video in videos:
                _ = await self.connection.uploadAsyncSomething(
                videos,
                "video",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup,
                filename
            )

                if _['ok']: states[video] = Video(_['result']['video'])
                else: states[video] = _
            
            return states
        else: raise ValueError("Invalid data type")

    async def sendAnimation(
        self,
        chat_id: Union[str, int],
        animations: Union[str, list],
        caption: str = "",
        reply_to_message_id: int = None,
        reply_markup: ReplyKeyboardMarkup = None,
        filename: str = ""
    ):
        
        if isinstance(animations, str):
            _ = await self.connection.uploadAsyncSomething(
                animations,
                "animation",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup,
                filename
            )

            if _['ok']: return Animation(_['result']['animation'])
            else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

        elif isinstance(animations, list):
            states = {}

            for animation in animations:
                _ = await self.connection.uploadAsyncSomething(
                animations,
                "animation",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup,
                filename
            )

                if _['ok']: states[animation] = Animation(_['result']['animation'])
                else: states[animation] = _
            
            return states
        else: raise ValueError("Invalid data type")

    async def sendVoice(
        self,
        chat_id: Union[str, int],
        voices: Union[str, list],
        caption: str = "",
        reply_to_message_id: int = None,
        reply_markup: ReplyKeyboardMarkup = None,
        filename: str = ""
    ):
        
        if isinstance(voices, str):
            _ = await self.connection.uploadAsyncSomething(
                voices,
                "voice",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup,
                filename
            )

            if _['ok']: return Voice(_['result']['voice'])
            else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

        elif isinstance(voices, list):
            states = {}

            for voice in voices:
                _ = await self.connection.uploadAsyncSomething(
                voices,
                "voice",
                chat_id,
                caption,
                reply_to_message_id,
                reply_markup,
                filename
            )

                if _['ok']: states[voice] = Voice(_['result']['voice'])
                else: states[voice] = _
            
            return states
        else: raise ValueError("Invalid data type")

    async def sendLocation(
        self,
        chat_id: Union[str, int],
        latitude: float,
        longitude: float,
        horizontal_accuracy: float = None,
        reply_to_message_id: int = None,
        reply_markup: Union[ ReplyKeyboardMarkup, InlineKeyboardMarkup ] = None
    ):
        
        _ = await self.connection.createAsyncConnection(
            "sendLocation",
            {
                "chat_id": chat_id,
                "latitude": latitude,
                "longitude": longitude,
                "horizontal_accuracy": horizontal_accuracy,
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": None if reply_markup is None else reply_markup.keybuttons
            }
        )

        if _['ok']: return Location(_['result']['location'])
        else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

    async def sendContact(
        self,
        chat_id: Union[int, str],
        phone_number: str,
        first_name: str,
        last_name: str = None,
        reply_to_message_id: int = None,
        reply_markup: Union[ ReplyKeyboardMarkup, InlineKeyboardMarkup ] = None
    ):
        
        _ = await self.connection.createAsyncConnection(
            "sendContact",
            {
                "chat_id": chat_id,
                "phone_number": phone_number,
                "first_name": first_name,
                "last_name": last_name,
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": None if reply_markup is None else reply_markup.keybuttons
            }
        )

        if _['ok']: return Contact(_['result']['contact'])
        else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

    async def getFile(
        self,
        file_id: str
    ):
        
        _ = await self.connection.createAsyncConnection(
            "getFile",
            {
                "file_id": file_id
            }
        )

        if _['ok']:return File(_['result'])
        else: raise UnexceptedServerError(dumps(_, ensure_ascii=False))

    async def downloadFile(
        self,
        file_path: str,
        save_in_path: str
    ):
        try:
            content = await self.connection._async.get(
                self.connection.file_url+file_path
            )

            if not os.path.exists(save_in_path):open(save_in_path, 'a')
            open(save_in_path, "wb").write(content.text.encode())
            return { "ok": True }
        except Exception as ErrorWriting:
            return { "ok": False, "message": ErrorWriting }
        
    async def getFileContent(
        self,
        file_path: str,
    ):
        content = await self.connection._async.get(
                self.connection.file_url+file_path
            )
        
        return content.text

    async def banChatMember(
        self,
        chat_id: Union[str, int],
        user_id: Union[str, int]
    ):
        
        _ = await self.connection.createAsyncConnection(
            "banChatMember",
            {
                "chat_id": chat_id,
                "user_id": user_id
            }
        )

        if _['ok'] != True:
            if _['description'] == "Bad Request: message not found":
                raise ChatNotFoundError(f"Chat not found `{chat_id}`")
            elif _['description'] == "Forbidden: permission_denied":
                raise PermissionDenied("You do not have this premission to use")
        else:
            return _
        
    async def unbanChatmember(
        self,
        chat_id: Union[str, int],
        user_id: Union[str, int],
        only_if_banned: bool = True
    ):
        
        _ = await self.connection.createAsyncConnection(
            "unbanChatMember",
            {
                "chat_id": chat_id,
                "user_id": user_id,
                "only_if_banned": only_if_banned
            }
        )

        if _['ok'] != True:
            if _['description'] == "Bad Request: message not found":
                raise ChatNotFoundError(f"Chat not found `{chat_id}`")
            elif _['description'] == "Forbidden: permission_denied":
                raise PermissionDenied("You do not have this premission to use")
        else:
            return _
        
    async def promoteChatMember(
        self,
        chat_id: Union[str, int],
        user_id: Union[str, int],
        can_change_info: bool = False,
        can_post_messages: bool = False,
        can_edit_messages: bool = False,
        can_delete_messages: bool = False,
        can_manage_video_chats: bool = False,
        can_invite_users: bool = False,
        can_restrict_members: bool = False
    ):
        
        _ = await self.connection.createAsyncConnection(
            "promoteChatMember",
            {
                "chat_id": chat_id,
                "user_id": user_id,
                "can_change_info": can_change_info,
                "can_post_messages": can_post_messages,
                "can_edit_messages": can_edit_messages,
                "can_delete_messages": can_delete_messages,
                "can_manage_video_chats": can_manage_video_chats,
                "can_invite_users": can_invite_users,
                "can_restrict_members": can_restrict_members
            }
        )

        return _
    
    async def setChatPhoto(
        self,
        chat_id: Union[str, int],
        photo: str
    ):
        
        if photo.startswith("http"):
            return await self.connection._async.post(
                self.connection.url+"/setChatPhoto",
                params={
                    "chat_id": chat_id,
                    "photo": photo
                }
            )
        elif os.path.exists(photo) and os.path.isfile(photo):
            return await self.connection._async.post(
                self.connection.url+"/setChatPhoto",
                params={
                    "chat_id": chat_id
                },
                files={
                    "photo": open(photo, 'rb').read()
                }
            )

        else: raise ValueError("{} is not URL or Doesnt exist in your Local Storage".format(
            photo
        ))

    async def leaveChat(
        self,
        chat_id: Union[str, int]
    ):
        
        return await self.connection.createAsyncConnection(
            "leaveChat",
            {
                "chat_id": chat_id
            }
        )
    
    async def getChat(
        self,
        chat_id: Union[str, int]
    ):
        
        _ = await self.connection.createAsyncConnection(
            "getChat",
            {
                "chat_id": chat_id
            }
        )

        if _['ok']:return Chat(_['result'])
        else:raise UnexceptedServerError(dumps(_, ensure_ascii=False))

    async def getChatMembersCount(
        self,
        chat_id: Union[str, int]
    ):
        
        return await self.connection.createAsyncConnection(
            "getChatMembersCount",
            {
                "chat_id": chat_id
            }
        )
    
    async def pinMessage(
        self,
        chat_id: Union[str, int],
        message_id: int
    ):
        
        return await self.connection.createAsyncConnection(
            "pinChatMessage",
            {
                "chat_id": chat_id,
                "message_id": message_id
            }
        )
    
    async def unpinMessage(
        self,
        chat_id: Union[str, int],
        message_id: int
    ):
        
        return await self.connection.createAsyncConnection(
            "unpinChatMessage",
            {
                "chat_id": chat_id,
                "message_id": message_id
            }
        )
    
    async def unpinAllMessage(
        self,
        chat_id: Union[str, int]
    ):
        
        return await self.connection.createAsyncConnection(
            "unpinAllChatMessages",
            {
                "chat_id": chat_id
            }
        )
    
    async def setChatTitle(
        self,
        chat_id: Union[str, int],
        title: str
    ):
        
        return await self.connection.createAsyncConnection(
            "setChatTitle",
            {
                "chat_id": chat_id,
                "title": title
            }
        )
    
    async def setChatDescription(
        self,
        chat_id: Union[str, int],
        description: str
    ):
        
        return await self.connection.createAsyncConnection(
            "setChatDescription",
            {
                "chat_id": chat_id,
                "description": description
            }
        )
        
    async def deleteChatPhoto(
        self,
        chat_id: Union[str, int]
    ):
        
        return await self.connection.createAsyncConnection(
            "deleteChatPhoto",
            {
                "chat_id": chat_id
            }
        )
    
    async def createInviteLink(
        self,
        chat_id: Union[str, int]
    ):
        
        return await self.connection.createAsyncConnection(
            "createChatInviteLink",
            {
                "chat_id": chat_id
            }
        )
    
    async def revokeInviteLink(
        self,
        chat_id: Union[str, int],
        previous_invite_link: str
    ):
        
        return await self.connection.createAsyncConnection(
            "revokeChatInviteLink",
            {
                "chat_id": chat_id,
                "invite_link": previous_invite_link
            }
        )
    
    async def exportInviteLink(
        self,
        chat_id: Union[str, int]
    ):
        
        return await self.connection.createAsyncConnection(
            "exportChatInviteLink",
            {
                "chat_id": chat_id
            }
        )
    
    async def editMessageText(
        self,
        chat_id: Union[str, int],
        text: str,
        message_id: int,
        reply_markup: InlineKeyboardMarkup = None
    ):

        _ = await self.connection.createAsyncConnection(
            "editMessageText",
            {
                "chat_id": chat_id,
                "text": text,
                "message_id": message_id,
                "reply_markup": None if reply_markup is None else reply_markup.keybuttons
            }
        )

        if _['ok']:return Message(self.token, _['result'])
        else:raise UnexceptedServerError(dumps(_, ensure_ascii=False))

    async def deleteMessage(
        self,
        chat_id: Union[str, int],
        message_id: int
    ):
        
        return await self.connection.createAsyncConnection(
            "deleteMessage",
            {
                "chat_id": chat_id,
                "message_id": message_id
            }
        )
    
    async def uploadStickerFile(
        self,
        user_id: int,
        sticker: str
    ):
        
        if sticker.startswith("http"):
            return await self.connection._async.post(
                self.connection.url+"/uploadStickerFile",
                params={
                    "user_id": user_id,
                    "sticker": sticker
                }
            )
        elif os.path.exists(sticker) and os.path.isfile(sticker):
            return await self.connection._async.post(
                self.connection.url+"/uploadStickerFile",
                params={
                    "user_id": user_id
                },
                files={
                    "sticker": open(sticker, 'rb').read()
                }
            )

        else: raise ValueError("{} is not URL or Doesnt exist in your Local Storage".format(
            sticker
        ))

    async def createStickerSet(
        self,
        user_id: int,
        name: str,
        title: str,
        sticker: list = []
    ):
        
        return await self.connection.createAsyncConnection(
            "createNewStickerSet",
            {
                "user_id": user_id,
                "name": name,
                "title": title,
                "sticker": sticker
            }
        )
    
    async def addStickerToSet(
        self,
        user_id: int,
        name: str,
        sticker: str
    ):
        
        if sticker.startswith("http"):
            return await self.connection._async.post(
                self.connection.url+"/addStickerToSet",
                params={
                    "user_id": user_id,
                    "name": name,
                    "sticker": sticker
                }
            )
        elif os.path.exists(sticker) and os.path.isfile(sticker):
            return await self.connection._async.post(
                self.connection.url+"/addStickerToSet",
                params={
                    "user_id": user_id,
                    "name": name
                },
                files={
                    "sticker": open(sticker, 'rb').read()
                }
            )

        else: raise ValueError("{} is not URL or Doesnt exist in your Local Storage".format(
            sticker
        ))

    def on(
        self,
        type: message_types = 'message',
        offset: int = -1,
        limit: int = 1,
        sleep: int = 0
    ):
        def decorate(func):
            self.handlers.append(
                {
                    "function": func,
                    "offset": offset,
                    "limit": limit,
                    "type": type,
                    "sleep": sleep
                }
            )
            return func
        return decorate
    
    async def run(self):
        msg_ids = set()
        query_ids = set()
        while 1:
            for handler in self.handlers:
                func = handler['function']
                limit = handler['limit']
                offset = handler['offset']
                _sleep = handler['sleep']
                _type: message_types = handler['type']

                _ = await self.getUpdates(offset, limit)
                _msg = Message(self.token, _[0])

                if _type == "message":
                    if not _msg.message_id in msg_ids:
                        msg_ids.add(_msg.message_id)
                        await func(_msg)

                elif _type == "photo":
                    if len(_msg.photo) > 0:
                        if not _msg.message_id in msg_ids:
                            msg_ids.add(_msg.message_id)
                            await func(_msg)

                elif _type == "video":
                    if _msg.video.result != {} or _msg.document.mime_type.startswith("video"):
                        if not _msg.message_id in msg_ids:
                            msg_ids.add(_msg.message_id)
                            await func(_msg)

                elif _type == "audio":
                    if _msg.document.mime_type.startswith("audio"):
                        if not _msg.message_id in msg_ids:
                            msg_ids.add(_msg.message_id)
                            await func(_msg)

                elif _type == "sticker":
                    if _msg.sticker.result != {}:
                        if not _msg.message_id in msg_ids:
                            msg_ids.add(_msg.message_id)
                            await func(_msg)

                elif _type == "voice":
                    if _msg.voice.result != {}:
                        if not _msg.message_id in msg_ids:
                            msg_ids.add(_msg.message_id)
                            await func(_msg)

                elif _type == "document":
                    if _msg.document.result != {}:
                        if not _msg.message_id in msg_ids:
                            msg_ids.add(_msg.message_id)
                            await func(_msg)

                elif _type == "callback_query":
                    if not _msg.callback_query.id == 0:
                        if not _msg.callback_query.inline_id in query_ids:
                            query_ids.add(_msg.callback_query.inline_id)
                            await func(_msg)


                asyncio.sleep(_sleep) if not _sleep == 0 else ...
