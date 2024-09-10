from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from helper.database import db  # Use the db instance from database.py
import importlib.util
import sys

# Dynamically import the module with special characters
module_name = "thumb_&_cap"
module_path = "./plugins/thumb_&_cap.py"

spec = importlib.util.spec_from_file_location(module_name, module_path)
thumb_and_cap = importlib.util.module_from_spec(spec)
sys.modules[module_name] = thumb_and_cap
spec.loader.exec_module(thumb_and_cap)

handle_set_caption = thumb_and_cap.handle_set_caption
handle_delete_caption = thumb_and_cap.handle_delete_caption
handle_see_caption = thumb_and_cap.handle_see_caption
handle_view_thumbnail = thumb_and_cap.handle_view_thumbnail
handle_delete_thumbnail = thumb_and_cap.handle_delete_thumbnail

@Client.on_message(filters.private & filters.command("settings"))
async def settings_command(client: Client, message: Message):
    user_id = message.from_user.id
    user_media_type = await db.get_media_type(user_id) or "Video"  # Fetch using db instance

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("sᴇᴛ ᴍᴇᴅɪᴀ", callback_data="set_media")],
        [
            InlineKeyboardButton("sᴇᴛ ᴄᴀᴩᴛɪᴏɴ", callback_data="set_caption"),
            InlineKeyboardButton("ᴠɪᴇᴡ ᴄᴀᴩᴛɪᴏɴ", callback_data="see_caption"),
            InlineKeyboardButton("ᴅᴇʟᴇᴛᴇ ᴄᴀᴩᴛɪᴏɴ", callback_data="delete_caption")
        ],
        [
            InlineKeyboardButton("sᴇᴛ ᴛʜᴜᴍʙɴᴀɪʟ", callback_data="set_thumbnail"),
            InlineKeyboardButton("ᴠɪᴇᴡ ᴛʜᴜᴍʙɴᴀɪʟ", callback_data="view_thumbnail"),
            InlineKeyboardButton("ᴅᴇʟᴇᴛᴇ ᴛʜᴜᴍʙɴᴀɪʟ", callback_data="delete_thumbnail")
        ],
        [
            InlineKeyboardButton("sᴇᴛ ᴘʀᴇғɪx", callback_data="set_prefix"),
            InlineKeyboardButton("ᴅᴇʟᴇᴛᴇ ᴘʀᴇғɪx", callback_data="del_prefix"),
            InlineKeyboardButton("sᴇᴇ ᴘʀᴇғɪx", callback_data="see_prefix")
        ],
        [
            InlineKeyboardButton("sᴇᴛ sᴜғғɪx", callback_data="set_suffix"),
            InlineKeyboardButton("ᴅᴇʟᴇᴛᴇ sᴜғғɪx", callback_data="del_suffix"),
            InlineKeyboardButton("sᴇᴇ sᴜғғɪx", callback_data="see_suffix")
        ],
        [InlineKeyboardButton("ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ", callback_data="auto_rename")]
    ])
    
    await message.reply_photo(
        photo="https://graph.org/file/0a1de3013521eb6e7ee02.jpg",  # Your image link
        caption="**⚙️ Sᴇᴛᴛɪɴɢs Mᴇɴᴜ**\n\nSᴇʟᴇᴄᴛ ᴀɴ Oᴘᴛɪᴏɴ:",
        reply_markup=keyboard
    )

@Client.on_callback_query()
async def callback_handler(client: Client, callback_query):
    data = callback_query.data
    user_id = callback_query.from_user.id

    if data == "set_media":
        user_media_type = await db.get_media_type(user_id) or "Video"  # Fetch using db instance
        media_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Video ✅" if user_media_type == "Video" else "Video", callback_data="media_video"),
                InlineKeyboardButton("Document ✅" if user_media_type == "Document" else "Document", callback_data="media_document")
            ],
            [InlineKeyboardButton("⪻ʙᴀᴄᴋ", callback_data="main_menu")]
        ])
        await callback_query.message.edit_text("Sᴇʟᴇᴄᴛ Mᴇᴅɪᴀ Tʏᴘᴇ:", reply_markup=media_keyboard)
    elif data.startswith("media_"):
        media_type = data.split("_")[1].capitalize()
        await db.set_media_type(user_id, media_type)  # Set using db instance
        await callback_query.message.edit_text(f"Selected media type: {media_type}")
    elif data == "main_menu":
        await settings_command(client, callback_query.message)
