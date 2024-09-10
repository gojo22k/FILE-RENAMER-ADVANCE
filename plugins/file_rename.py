import random
from helper.ffmpeg import fix_thumb, take_screen_shot
from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.utils import progress_for_pyrogram, convert, humanbytes
from helper.database import db
from helper.database import Database
from PIL import Image
import asyncio
import os
import time
from helper.utils import add_prefix_suffix
from config import Config
from utils import verify_user, check_token, check_verification, get_token

db = Database(Config.DB_URL, Config.DB_NAME)

app = Client("test", api_id=Config.STRING_API_ID,
             api_hash=Config.STRING_API_HASH, session_string=Config.STRING_SESSION)

# New methods to set and get media type
async def set_media_type(user_id, media_type):
    """Set the media type preference for a user."""
    await db.col.update_one(
        {"_id": user_id},
        {"$set": {"media_type": media_type}},
        upsert=True
    )

async def get_media_type(user_id):
    """Retrieve the media type preference for a user."""
    user_data = await db.col.find_one({"_id": user_id})
    media_type = user_data.get("media_type") if user_data else None
    return media_type

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def prompt_rename(client, message):
    # Check if verification is enabled
    if Config.VERIFY:
        # Check if the user is verified
        is_verified = await check_verification(client, message.from_user.id)
        if not is_verified:
            # Send verification message and return
            verification_url = await get_token(client, message.from_user.id, f"https://t.me/{Config.BOT_USERNAME}?start=")
            await message.reply_text(
                "You need to verify your account before you can use this feature. Please verify your account using the following link:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('🔗 Verify Now', url=verification_url)]
                ])
            )
            return
    
    await message.reply_text("✏️ Eɴᴛᴇʀ Nᴇᴡ Fɪʟᴇ Nᴀᴍᴇ...",
                             reply_to_message_id=message.id,
                             reply_markup=ForceReply(True))
    
    
@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    try:
        reply_message = message.reply_to_message

        if isinstance(reply_message.reply_markup, ForceReply):
            new_name = message.text
            await message.delete()

            msg = await client.get_messages(message.chat.id, reply_message.id)
            file = msg.reply_to_message

            if not file:
                await message.reply_text("⚠️ This message doesn't contain any downloadable media.")
                return

            media = getattr(file, file.media.value, None)
            if not media:
                await message.reply_text("⚠️ This message doesn't contain any media.")
                return

            # Handle file extension
            if not "." in new_name:
                if "." in media.file_name:
                    extn = media.file_name.rsplit('.', 1)[-1]
                else:
                    extn = "mkv"
                new_name = new_name + "." + extn

            await reply_message.delete()

            user_id = message.from_user.id
            media_type = await get_media_type(user_id)
            if not media_type:
                media_type = 'document'  # Default if no media type is found

            # Normalize media_type to lowercase
            media_type = media_type.lower()

            # Skip the "OK" button step and directly process the file
            await process_file(client, message, media, new_name, media_type)

    except Exception as e:
        await message.reply_text(f"⚠️ Error Occurred ☹️\n\n{e}")

async def process_file(client, message, media, new_name, media_type):
    """Process the file after getting the new name and media type."""

    # Initialize variables
    file_path = f"downloads/{new_name}"
    metadata_path = None
    ph_path = None

    try:
        # Download the file
        ms = await message.reply_text("⚙️ Tʀyɪɴɢ Tᴏ Dᴏᴡɴʟᴏᴀᴅɪɴɢ")
        path = await client.download_media(message=media, file_name=file_path, progress=progress_for_pyrogram, progress_args=("⚠️ __**Please wait...**__\n\n❄️ **Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....**", ms, time.time()))
    except Exception as e:
        if ms:
            await ms.edit(f"⚠️ Error Occurred ☹️\n\n{e}")
        return

    _bool_metadata = await db.get_metadata(message.chat.id)

    if _bool_metadata:
        metadata_path = f"Metadata/{new_name}"
        metadata = await db.get_metadata_code(message.chat.id)
        if metadata:
            try:
                await ms.edit("I Fᴏᴜɴᴅ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ\n\n__**Aᴅᴅɪɴɢ Mᴇᴛᴀᴅᴀᴛᴀ Tᴏ Fɪʟᴇ....**")
                cmd = f"""ffmpeg -i "{path}" {metadata} "{metadata_path}" """
                process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                stdout, stderr = await process.communicate()
                er = stderr.decode()
                if er:
                    return await ms.edit(f"{er}\n\n**Error**")
            except Exception as e:
                return await ms.edit(f"⚠️ Error Occurred ☹️\n\n{e}")
        await ms.edit("**Metadata added to the file successfully ✅**\n\n⚠️ __**Tʀyɪɴɢ Tᴏ Uᴩʟᴏᴀᴅɪɴɢ....**")
    else:
        await ms.edit("⚠️ __**Please wait...**__\n\n\n**Tʀyɪɴɢ Tᴏ Uᴩʟᴏᴀᴅɪɴɢ....**")

    duration = 0
    try:
        parser = createParser(file_path)
        metadata = extractMetadata(parser)
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        parser.close()
    except Exception as e:
        pass

    c_caption = await db.get_caption(message.chat.id)
    c_thumb = await db.get_thumbnail(message.chat.id)

    if c_caption:
        try:
            caption = c_caption.format(filename=new_name, filesize=humanbytes(media.file_size), duration=convert(duration))
        except Exception as e:
            return await ms.edit(text=f"Yᴏᴜʀ Cᴀᴩᴛɪᴏɴ Eʀʀᴏʀ Exᴄᴇᴩᴛ Kᴇʏᴡᴏʀᴅ Aʀɢᴜᴇɴᴛ ●> ({e})")
    else:
        caption = f"**{new_name}**"

    if media.thumbs or c_thumb:
        if c_thumb:
            ph_path = await client.download_media(c_thumb)
            width, height, ph_path = await fix_thumb(ph_path)
        else:
            try:
                ph_path_ = await take_screen_shot(file_path, os.path.dirname(os.path.abspath(file_path)), random.randint(0, duration - 1))
                width, height, ph_path = await fix_thumb(ph_path_)
            except Exception as e:
                ph_path = None

    # Initialize file to ensure it's defined in the retry loop
    filw = None

    # Retry logic for sending the file
    max_retries = 3
    for attempt in range(max_retries):
        try:
            if media.file_size > 4000 * 1024 * 1024:
                if media_type == "document":
                    filw = await client.send_document(
                        message.chat.id,
                        document=metadata_path if _bool_metadata else file_path,
                        thumb=ph_path,
                        caption=caption,
                        progress=progress_for_pyrogram,
                        progress_args=("⚠️ __**Please wait...**__\n\n❄️ **Uᴩʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....**", ms, time.time())
                    )
                else:
                    filw = await client.send_video(
                        message.chat.id,
                        video=metadata_path if _bool_metadata else file_path,
                        thumb=ph_path,
                        caption=caption,
                        progress=progress_for_pyrogram,
                        progress_args=("⚠️ __**Please wait...**__\n\n❄️ **Uᴩʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....**", ms, time.time())
                    )
            else:
                if media_type == "document":
                    filw = await client.send_document(
                        message.chat.id,
                        document=metadata_path if _bool_metadata else file_path,
                        thumb=ph_path,
                        caption=caption,
                        progress=progress_for_pyrogram,
                        progress_args=("⚠️ __**Please wait...**__\n\n❄️ **Uᴩʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....**", ms, time.time())
                    )
                else:
                    filw = await client.send_video(
                        message.chat.id,
                        video=metadata_path if _bool_metadata else file_path,
                        thumb=ph_path,
                        caption=caption,
                        progress=progress_for_pyrogram,
                        progress_args=("⚠️ __**Please wait...**__\n\n❄️ **Uᴩʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....**", ms, time.time())
                    )
            break  # Exit loop if successful
        except Exception as e:
            if attempt < max_retries - 1:
                continue  # Retry
            else:
                await ms.edit(f"⚠️ Error Occurred ☹️\n\n{e}")
                return

    if ms:
        await ms.delete()

    if ph_path and os.path.exists(ph_path):
        os.remove(ph_path)

    if metadata_path and os.path.exists(metadata_path):
        os.remove(metadata_path)

    if os.path.exists(file_path):
        os.remove(file_path)
