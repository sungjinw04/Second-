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
            
            
# Start the bot
app.run()
