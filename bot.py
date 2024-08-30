import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
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

# Command handler to fetch change history
@app.on_message(filters.command("rape") & filters.group)
async def handle_rape_command(client: Client, message: Message):
    user_id = message.from_user.id
    
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

# Start the bot
app.run()

