from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.private & filters.command(["upgrade"]))
async def upgradecm(bot, message):
    text = """**📦 Uᴘɢʀᴀᴅᴇ Yᴏᴜʀ 𝙿𝚕𝚊𝚗!**

**🔓 Fʀᴇᴇ 𝙿𝚕𝚊𝚗**  
**💰 Pʀɪᴄᴇ**: **₹0 / month**  
- 📁 **Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Lɪᴍɪᴛ**: 2 GB per day  
- 🔒 **Tᴏᴋᴇɴ Vᴇʀɪꜰɪᴄᴀᴛɪᴏɴ**: Needed every day  
- 🏷️ **Dᴀɪʟʏ Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Cᴀᴘᴀᴄɪᴛʏ**: 10 GB

**🪙 Bᴀsɪᴄ 𝙿𝚕𝚊𝚗**  
**💰 Pʀɪᴄᴇ**: **₹49 / month**  
- 📁 **Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Lɪᴍɪᴛ**: 4 GB per day  
- 🔒 **Tᴏᴋᴇɴ Vᴇʀɪꜰɪᴄᴀᴛɪᴏɴ**: Needed every day  
- 🏷️ **Dᴀɪʟʏ Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Cᴀᴘᴀᴄɪᴛʏ**: 50 GB

**⚡ Sᴛᴀɴᴅᴀʀᴅ 𝙿𝚕𝚊𝚗**  
**💰 Pʀɪᴄᴇ**: **₹99 / month**  
- 📁 **Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Lɪᴍɪᴛ**: 4 GB per day  
- ✅ **Tᴏᴋᴇɴ Vᴇʀɪꜰɪᴄᴀᴛɪᴏɴ**: Not needed  
- 🏷️ **Dᴀɪʟʏ Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Cᴀᴘᴀᴄɪᴛʏ**: 100 GB

**💎 Pʀᴏ 𝙿𝚕𝚊𝚗**  
**💰 Pʀɪᴄᴇ**: **₹199 / month**  
- 📁 **Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Lɪᴍɪᴛ**: 4 GB per day  
- ✅ **Tᴏᴋᴇɴ Vᴇʀɪꜰɪᴄᴀᴛɪᴏɴ**: Not needed  
- 🏷️ **Dᴀɪʟʏ Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Cᴀᴘᴀᴄɪᴛʏ**: ♾️ Unlimited

🔹 **Pᴀʏᴍᴇɴᴛ Iɴsᴛʀᴜᴄᴛɪᴏɴs**  
Pay using UPI ID: `rasanandamohapatra2014@okhdfcbank`  
After payment, send screenshots of the transaction to Admin: [@AniflixAnkit](https://t.me/AniflixAnkit)

📩 **Cᴏɴᴛᴀᴄᴛ Aᴅᴍɪɴ ғᴏʀ Assɪsᴛᴀɴᴄᴇ**  
"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Contact Admin", url="https://t.me/AniflixAnkit")],
        [InlineKeyboardButton("Cancel", callback_data="cancel")]
    ])
    
    await message.reply_text(text=text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex('upgrade'))
async def upgrade(bot, update):
    text = """**📦 Uᴘɢʀᴀᴅᴇ Yᴏᴜʀ 𝙿𝚕𝚊𝚗!**

**🔓 Fʀᴇᴇ 𝙿𝚕𝚊𝚗**  
**💰 Pʀɪᴄᴇ**: **₹0 / month**  
- 📁 **Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Lɪᴍɪᴛ**: 2 GB per day  
- 🔒 **Tᴏᴋᴇɴ Vᴇʀɪꜰɪᴄᴀᴛɪᴏɴ**: Needed every day  
- 🏷️ **Dᴀɪʟʏ Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Cᴀᴘᴀᴄɪᴛʏ**: 10 GB

**🪙 Bᴀsɪᴄ 𝙿𝚕𝚊𝚗**  
**💰 Pʀɪᴄᴇ**: **₹49 / month**  
- 📁 **Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Lɪᴍɪᴛ**: 4 GB per day  
- 🔒 **Tᴏᴋᴇɴ Vᴇʀɪꜰɪᴄᴀᴛɪᴏɴ**: Needed every day  
- 🏷️ **Dᴀɪʟʏ Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Cᴀᴘᴀᴄɪᴛʏ**: 50 GB

**⚡ Sᴛᴀɴᴅᴀʀᴅ 𝙿𝚕𝚊𝚝**  
**💰 Pʀɪᴄᴇ**: **₹99 / month**  
- 📁 **Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Lɪᴍɪᴛ**: 4 GB per day  
- ✅ **Tᴏᴋᴇɴ Vᴇʀɪꜰɪᴄᴀᴛɪᴏɴ**: Not needed  
- 🏷️ **Dᴀɪʟʏ Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Cᴀᴘᴀᴄɪᴛʏ**: 100 GB

**💎 Pʀᴏ 𝙿𝚕𝚊𝚗**  
**💰 Pʀɪᴄᴇ**: **₹199 / month**  
- 📁 **Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Lɪᴍɪᴛ**: 4 GB per day  
- ✅ **Tᴏᴋᴇɴ Vᴇʀɪꜰɪᴄᴀᴛɪᴏɴ**: Not needed  
- 🏷️ **Dᴀɪʟʏ Fɪʟᴇ Rᴇɴᴀᴍɪɴɢ Cᴀᴘᴀᴄɪᴛʏ**: ♾️ Unlimited

🔹 **Pᴀʏᴍᴇɴᴛ Iɴsᴛʀᴜᴄᴛɪᴏɴs**  
Pay using UPI ID: `rasanandamohapatra2014@okhdfcbank`  
After payment, send screenshots of the transaction to Admin: [@AniflixAnkit](https://t.me/AniflixAnkit)

📩 **Cᴏɴᴛᴀᴄᴛ Aᴅᴍɪɴ ғᴏʀ Assɪsᴛᴀɴᴄᴇ**  
"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Contact Admin", url="https://t.me/AniflixAnkit")],
        [InlineKeyboardButton("Cancel", callback_data="cancel")]
    ])
    
    await update.message.edit(text=text, reply_markup=keyboard)
