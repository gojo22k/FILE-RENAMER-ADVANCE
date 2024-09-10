from config import Config
from helper.database import Database
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
import os, sys, time, asyncio, logging, datetime

db = Database(Config.DB_URL, Config.DB_NAME)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@Client.on_message(filters.command(["stats", "status"]) & filters.user(Config.ADMIN))
async def get_stats(bot, message):
    total_users = await db.total_users_count()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - Config.BOT_UPTIME))    
    start_t = time.time()
    st = await message.reply('**Aᴄᴄᴇꜱꜱɪɴɢ Tʜᴇ Dᴇᴛᴀɪʟꜱ.....**')    
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await st.edit(text=f"**--Bᴏᴛ Sᴛᴀᴛᴜꜱ--** \n\n**⌚️ Bᴏᴛ Uᴩᴛɪᴍᴇ:** {uptime} \n**🐌 Cᴜʀʀᴇɴᴛ Pɪɴɢ:** `{time_taken_s:.3f} ᴍꜱ` \n**👭 Tᴏᴛᴀʟ Uꜱᴇʀꜱ:** `{total_users}`")

@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.ADMIN))
async def restart_bot(b, m):
    await m.reply_text("🔄__Rᴇꜱᴛᴀʀᴛɪɴɢ.....__")
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMIN) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    await bot.send_message(Config.LOG_CHANNEL, f"{m.from_user.mention} or {m.from_user.id} Iꜱ ꜱᴛᴀʀᴛᴇᴅ ᴛʜᴇ Bʀᴏᴀᴅᴄᴀꜱᴛ......")
    all_users = await db.getid()  # Get all user IDs
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("Bʀᴏᴀᴅᴄᴀꜱᴛ Sᴛᴀʀᴛᴇᴅ..!") 
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = len(all_users)
    
    for user_id in all_users:
        sts = await send_msg(user_id, broadcast_msg)
        if sts == 200:
           success += 1
        else:
           failed += 1
        if sts == 400:
           await db.delete(user_id)
        done += 1
        if not done % 20:
           await sts_msg.edit(f"Bʀᴏᴀᴅᴄᴀꜱᴛ Iɴ Pʀᴏɢʀᴇꜱꜱ: \nTᴏᴛᴀʟ Uꜱᴇʀꜱ {total_users} \nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFᴀɪʟᴇᴅ: {failed}")
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(f"Bʀᴏᴀᴅᴄᴀꜱᴛ Cᴏᴍᴩʟᴇᴛᴇᴅ: \nCᴏᴍᴩʟᴇᴛᴇᴅ Iɴ `{completed_in}`.\n\nTᴏᴛᴀʟ Uꜱᴇʀꜱ {total_users}\nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFᴀɪʟᴇᴅ: {failed}")

async def send_msg(user_id, message):
    try:
        await message.forward(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"{user_id} : Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ")
        return 400
    except UserIsBlocked:
        logger.info(f"{user_id} : Bʟᴏᴄᴋᴇᴅ Tʜᴇ Bᴏᴛ")
        return 400
    except PeerIdInvalid:
        logger.info(f"{user_id} : Uꜱᴇʀ Iᴅ Iɴᴠᴀʟɪᴅ")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500

@Client.on_message(filters.private & filters.user(Config.ADMIN) & filters.command(["addpremium"]))
async def buypremium(bot, message):
    await message.reply_text(
        "🦋 Select Plan To Upgrade.....",
        quote=True,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🪙 Basic", callback_data="vip1"),
                InlineKeyboardButton("⚡ Standard", callback_data="vip2"),
                InlineKeyboardButton("💎 Pro", callback_data="vip3"),
                InlineKeyboardButton("✖️ Cancel ✖️", callback_data="cancel")
            ]
        ])
    )

@Client.on_callback_query(filters.regex('vip1'))
async def vip1(bot, update):
    user_id = update.message.reply_to_message.text.split("/addpremium")[1].strip()
    inlimit = 21474836500
    await db.uploadlimit(int(user_id), inlimit)
    await db.usertype(int(user_id), "🪙 Basic")
    await db.addpre(int(user_id))
    await update.message.edit("Added Successfully To Premium Upload Limit 20 GB")
    await bot.send_message(user_id, "Hey You Are Upgraded To Basic. Check Your Plan Here /myplan")

@Client.on_callback_query(filters.regex('vip2'))
async def vip2(bot, update):
    user_id = update.message.reply_to_message.text.split("/addpremium")[1].strip()
    inlimit = 53687091200
    await db.uploadlimit(int(user_id), inlimit)
    await db.usertype(int(user_id), "⚡ Standard")
    await db.addpre(int(user_id))
    await update.message.edit("Added Successfully To Premium Upload Limit 50 GB")
    await bot.send_message(user_id, "Hey You Are Upgraded To Standard. Check Your Plan Here /myplan")

@Client.on_callback_query(filters.regex('vip3'))
async def vip3(bot, update):
    user_id = update.message.reply_to_message.text.split("/addpremium")[1].strip()
    inlimit = 107374182400
    await db.uploadlimit(int(user_id), inlimit)
    await db.usertype(int(user_id), "💎 Pro")
    await db.addpre(int(user_id))
    await update.message.edit("Added Successfully To Premium Upload Limit 100 GB")
    await bot.send_message(user_id, "Hey You Are Upgraded To Pro. Check Your Plan Here /myplan")

@Client.on_message(filters.command("ulist") & filters.user(Config.ADMIN))
async def user_list(bot: Client, message: Message):
    try:
        # Fetch the lists of users directly from the collection
        premium_users = await db.get_premium_users()
        non_premium_users = await db.get_non_premium_users()

        # Format the user list
        premium_list = "\n".join([f"**User ID:** `{user['_id']}` - **Plan:** {user['usertype']}" for user in premium_users])
        non_premium_list = "\n".join([f"**User ID:** `{user['_id']}` - **Plan:** Non-Premium" for user in non_premium_users])

        # Send the lists to the admin
        response = f"**Premium Users:**\n{premium_list if premium_list else 'No premium users found.'}\n\n" \
                   f"**Non-Premium Users:**\n{non_premium_list if non_premium_list else 'No non-premium users found.'}"

        await message.reply_text(response, quote=True)
    except Exception as e:
        logger.error(f"/ulist command error: {e}")
        await message.reply_text("An error occurred while fetching the user list.", quote=True)