import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# Configurations
api_id = "25064357"
api_hash = "cda9f1b3f9da4c0c93d1f5c23ccb19e2"
bot_token = "7519139941:AAE6jFCGiqvhLu1i7HoNL9qdQRZgrQm6HqM"
mongo_url = "mongodb+srv://tanjiro1564:tanjiro1564@cluster0.pp5yz4e.mongodb.net/?retryWrites=true&w=majority"
db_name = "telegram_bot"
collection_name = "user_data"

# Create a Pyrogram Client
app = Client("group_watcher_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# MongoDB setup
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]
collection = db[collection_name]

# Function to log user changes
async def log_user_changes(user_id, username, name):
    now = datetime.utcnow()
    update = {
        "$set": {
            "user_id": user_id,
            "username": username,
            "name": name,
            "last_modified": now
        },
        "$push": {
            "change_history": {
                "username": username,
                "name": name,
                "modified_at": now
            }
        }
    }
    await collection.update_one({"user_id": user_id}, update, upsert=True)

# Command handler for /start
@app.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message):
    # Send an image first
    await message.reply_photo(
        "https://telegra.ph//file/919714d04904fae43ffd0.jpg"
    )
    
    # Welcome message
    welcome_text = "Welcome to the bot! Please choose an option below:"
    
    # Inline keyboard with buttons arranged vertically
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("My Master", url="http://t.me/sung_jinwo4")],
            [InlineKeyboardButton("Support", url="http://t.me/beyondlimit7")],
            [InlineKeyboardButton("Destroyer", url="http://t.me/souls_borns")],
            [InlineKeyboardButton("Network", url="http://t.me/soul_networks")],
        ]
    )
    
    # Sending the message with the inline keyboard
    await message.reply(welcome_text, reply_markup=keyboard)
# Event handler for new messages
@app.on_message(filters.group)
async def handle_message(client: Client, message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    name = message.from_user.first_name + (f" {message.from_user.last_name}" if message.from_user.last_name else "")
    
    # Fetch previous data
    user_data = await collection.find_one({"user_id": user_id})
    
    # Check for changes in username or name
    if user_data:
        if user_data.get("username") != username or user_data.get("name") != name:
            await log_user_changes(user_id, username, name)
            await message.reply(f"{user_data.get('name')} has changed username/name to {username or name}")
    else:
        await log_user_changes(user_id, username, name)

# Non-filter command handling
    if message.text and message.text.startswith("/rape"):
        user_id = message.from_user.id
        await message.reply("Processing the /rape command...")

        # Fetch user data
        user_data = await collection.find_one({"user_id": user_id})
        
        if not user_data or "change_history" not in user_data:
            await message.reply("No changes recorded for this user.")
        else:
            history = user_data["change_history"]
            response = f"Change history for {user_data.get('name')}:\n\n"
            for change in history:
                response += f"Name: {change.get('name')} | Username: {change.get('username')} | Modified At: {change.get('modified_at').strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
            await message.reply(response)

# Non-filter command handling for /maachuda
    if message.reply_to_message and message.text and message.text.startswith("/maachuda"):
        target_user_id = message.reply_to_message.from_user.id
        target_username = message.reply_to_message.from_user.username
        target_name = message.reply_to_message.from_user.first_name + (f" {message.reply_to_message.from_user.last_name}" if message.reply_to_message.from_user.last_name else "")
        
        # Fetch target user data
        target_user_data = await collection.find_one({"user_id": target_user_id})
        
        if not target_user_data:
            await message.reply(f"No data recorded for {target_name} ({target_username}).")
        else:
            response = f"Information for {target_name} ({target_username}):\n\n"
            response += f"User ID: {target_user_data.get('user_id')}\n"
            response += f"Current Name: {target_user_data.get('name')}\n"
            response += f"Current Username: {target_user_data.get('username')}\n"
            response += f"Last Modified: {target_user_data.get('last_modified').strftime('%Y-%m-%d %H:%M:%S')} UTC\n\n"
            
            # Append change history
            history = target_user_data.get("change_history", [])
            if history:
                response += "Change history:\n"
                for change in history:
                    response += f"Name: {change.get('name')} | Username: {change.get('username')} | Modified At: {change.get('modified_at').strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
            else:
                response += "No changes recorded."
            
            # Send the response along with an inline button
            await message.reply(
                response,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Go to Profile", url="http://t.me/sung_jinwo4")]]
                )
            )

# Command handler for /bkl (non-filter)
@app.on_message()
async def handle_bkl(client: Client, message: Message):
    if message.text and message.text.startswith("/bkl"):
        if message.reply_to_message and message.reply_to_message.text:
            target_message = message.reply_to_message
            target_user = target_message.from_user
            quote_text = f"\"{target_message.text}\"\n- {target_user.first_name}"
            
            # Send the quote
            await message.reply(quote_text)
        else:
            await message.reply("Please reply to a text message to create a quote.")

# command for quotly

try:
    from aiohttp import ContentTypeError
except ImportError:
    ContentTypeError = None

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    import cv2
except ImportError:
    cv2 = None
try:
    import numpy as np
except ImportError:
    np = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


class Quotly:
    _API = "https://bot.lyo.su/quote/generate"
    _entities = {
        types.MessageEntityPhone: "phone_number",
        types.MessageEntityMention: "mention",
        types.MessageEntityBold: "bold",
        types.MessageEntityCashtag: "cashtag",
        types.MessageEntityStrike: "strikethrough",
        types.MessageEntityHashtag: "hashtag",
        types.MessageEntityEmail: "email",
        types.MessageEntityMentionName: "text_mention",
        types.MessageEntityUnderline: "underline",
        types.MessageEntityUrl: "url",
        types.MessageEntityTextUrl: "text_link",
        types.MessageEntityBotCommand: "bot_command",
        types.MessageEntityCode: "code",
        types.MessageEntityPre: "pre",
    }

    async def _format_quote(self, event, reply=None, sender=None, type_="private"):
        async def telegraph(file_):
            file = file_ + ".png"
            Image.open(file_).save(file, "PNG")
            files = {"file": open(file, "rb").read()}
            uri = (
                "https://telegra.ph"
                + (
                    await async_searcher(
                        "https://telegra.ph/upload", post=True, data=files, re_json=True
                    )
                )[0]["src"]
            )
            os.remove(file)
            os.remove(file_)
            return uri

        if reply:
            reply = {
                "name": get_display_name(reply.sender) or "Deleted Account",
                "text": reply.raw_text,
                "chatId": reply.chat_id,
            }
        else:
            reply = {}
        is_fwd = event.fwd_from
        name = None
        last_name = None
        if sender and sender.id not in DEVLIST:
            id_ = get_peer_id(sender)
            name = get_display_name(sender)
        elif not is_fwd:
            id_ = event.sender_id
            sender = await event.get_sender()
            name = get_display_name(sender)
        else:
            id_, sender = None, None
            name = is_fwd.from_name
            if is_fwd.from_id:
                id_ = get_peer_id(is_fwd.from_id)
                try:
                    sender = await event.client.get_entity(id_)
                    name = get_display_name(sender)
                except ValueError:
                    pass
        if sender and hasattr(sender, "last_name"):
            last_name = sender.last_name
        entities = []
        if event.entities:
            for entity in event.entities:
                if type(entity) in self._entities:
                    enti_ = entity.to_dict()
                    del enti_["_"]
                    enti_["type"] = self._entities[type(entity)]
                    entities.append(enti_)
        message = {
            "entities": entities,
            "chatId": id_,
            "avatar": True,
            "from": {
                "id": id_,
                "first_name": (name or (sender.first_name if sender else None))
                or "Deleted Account",
                "last_name": last_name,
                "username": sender.username if sender else None,
                "language_code": "en",
                "title": name,
                "name": name or "Unknown",
                "type": type_,
            },
            "text": event.raw_text,
            "replyMessage": reply,
        }
        if event.document and event.document.thumbs:
            file_ = await event.download_media(thumb=-1)
            uri = await telegraph(file_)
            message["media"] = {"url": uri}

        return message
        async def create_quotly(
        self,
        event,
        url="https://qoute-api-akashpattnaik.koyeb.app/generate",
        reply={},
        bg=None,
        sender=None,
        OQAPI=True,
        file_name="quote.webp",
    ):
        
        if not isinstance(event, list):
            event = [event]
        if OQAPI:
            url = Quotly._API
        if not bg:
            bg = "#1b1429"
        content = {
            "type": "quote",
            "format": "webp",
            "backgroundColor": bg,
            "width": 512,
            "height": 768,
            "scale": 2,
            "messages": [
                await self._format_quote(message, reply=reply, sender=sender)
                for message in event
            ],
        }
        try:
            request = await async_searcher(url, post=True, json=content, re_json=True)
        except ContentTypeError as er:
            if url != self._API:
                return await self.create_quotly(
                    self._API, post=True, json=content, re_json=True
                )
            raise er
        if request.get("ok"):
            with open(file_name, "wb") as file:
                image = base64.decodebytes(request["result"]["image"].encode("utf-8"))
                file.write(image)
            return file_name
        raise Exception(str(request))


 quotly = Quotly()

try:
    import certifi
except ImportError:
    certifi = None

try:
    import numpy as np
except ImportError:
    np = None


async def async_searcher(
    url: str,
    post: bool = None,
    headers: dict = None,
    params: dict = None,
    json: dict = None,
    data: dict = None,
    ssl=None,
    re_json: bool = False,
    re_content: bool = False,
    real: bool = False,
    *args,
    **kwargs,
):
    try:
        import aiohttp
    except ImportError:
        raise DependencyMissingError(
            "'aiohttp' is not installed!\nthis function requires aiohttp to be installed."
        )
    async with aiohttp.ClientSession(headers=headers) as client:
        if post:
            data = await client.post(
                url, json=json, data=data, ssl=ssl, *args, **kwargs
            )
        else:
            data = await client.get(url, params=params, ssl=ssl, *args, **kwargs)
        if re_json:
            return await data.json()
        if re_content:
            return await data.read()
        if real:
            return data
        return await data.text()


def _unquote_text(text):
    return text.replace("'", "'").replace('"', '"')


def json_parser(data, indent=None, ascii=False):
    parsed = {}
    try:
        if isinstance(data, str):
            parsed = json.loads(str(data))
            if indent:
                parsed = json.dumps(
                    json.loads(str(data)), indent=indent, ensure_ascii=ascii
                )
        elif isinstance(data, dict):
            parsed = data
            if indent:
                parsed = json.dumps(data, indent=indent, ensure_ascii=ascii)
    except JSONDecodeError:
        parsed = eval(data)
    return parsed


def check_filename(filroid):
    if os.path.exists(filroid):
        no = 1
        while True:
            ult = "{0}_{2}{1}".format(*os.path.splitext(filroid) + (no,))
            if os.path.exists(ult):
                no += 1
            else:
                return ult
    return filroid


# edit or reply for telethon
async def eor(event, text=None, **args):
    time = args.get("time", None)
    edit_time = args.get("edit_time", None)
    if "edit_time" in args:
        del args["edit_time"]
    if "time" in args:
        del args["time"]
    if "link_preview" not in args:
        args["link_preview"] = False
    args["reply_to"] = event.reply_to_msg_id or event
    if event.out and not isinstance(event, MessageService):
        if edit_time:
            await sleep(edit_time)
        if "file" in args and args["file"] and not event.media:
            await event.delete()
            try:
                ok = await event.client.send_message(event.chat_id, text, **args)
            except MessageNotModifiedError:
                pass
        else:
            try:
                try:
                    del args["reply_to"]
                except KeyError:
                    pass
                ok = await event.edit(text, **args)
            except MessageNotModifiedError:
                pass
    else:
        ok = await event.client.send_message(event.chat_id, text, **args)

    if time:
        await sleep(time)
        return await ok.delete()
    return ok


async def eod(event, text=None, **kwargs):
    kwargs["time"] = kwargs.get("time", 8)
    return await eor(event, text, **kwargs)


async def _try_delete(event):
    try:
        return await event.delete()
    except MessageDeleteForbiddenError:
        pass
    except BaseException as er:
        from . import LOGS

        LOGS.error("❍ ᴇʀʀᴏʀ ᴡʜɪʟᴇ ᴅᴇʟᴇᴛɪɴɢ ᴍᴇssᴀɢᴇ..")
        LOGS.exception(er)


setattr(Message, "eor", eor)
setattr(Message, "try_delete", _try_delete)


@register(pattern="^/q(?: |$)(.*)")
async def quott_(event):
    match = event.pattern_match.group(1).strip()
    if not event.is_reply:
        return await event.eor("❍ ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ")
    msg = await event.reply("⚡️")
    reply = await event.get_reply_message()
    replied_to, reply_ = None, None
    if match:
        spli_ = match.split(maxsplit=1)
        if (spli_[0] in ["r", "reply"]) or (
            spli_[0].isdigit() and int(spli_[0]) in range(1, 21)
        ):
            if spli_[0].isdigit():
                if not event.client._bot:
                    reply_ = await event.client.get_messages(
                        event.chat_id,
                        min_id=event.reply_to_msg_id - 1,
                        reverse=True,
                        limit=int(spli_[0]),
                    )
                else:
                    id_ = reply.id
                    reply_ = []
                    for msg_ in range(id_, id_ + int(spli_[0])):
                        msh = await event.client.get_messages(event.chat_id, ids=msg_)
                        if msh:
                            reply_.append(msh)
            else:
                replied_to = await reply.get_reply_message()
            try:
                match = spli_[1]
            except IndexError:
                match = None
    user = None
    if not reply_:
        reply_ = reply
    if match:
        match = match.split(maxsplit=1)
    if match:
        if match[0].startswith("@") or match[0].isdigit():
            try:
                match_ = await event.client.parse_id(match[0])
                user = await event.client.get_entity(match_)
            except ValueError:
                pass
            match = match[1] if len(match) == 2 else None
        else:
            match = match[0]
    if match == "random":

        
            
# Start the bot
app.run()
