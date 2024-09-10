import datetime
import motor.motor_asyncio
from config import Config

class Database:
    def __init__(self, uri, database_name):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client[database_name]
        self.col = self.db['users']  # Reference to the specific collection

    async def uploadlimit(self, chat_id, limit):
        await self.col.update_one({"_id": chat_id}, {"$set": {"uploadlimit": limit}})

    async def usertype(self, chat_id, user_type):
        await self.col.update_one({"_id": chat_id}, {"$set": {"usertype": user_type}})

    async def addpre(self, chat_id):
        date = self.add_date()
        await self.col.update_one({"_id": chat_id}, {"$set": {"prexdate": date[0]}})

    async def addpredata(self, chat_id):
        await self.col.update_one({"_id": chat_id}, {"$set": {"prexdate": None}})

    async def find_one(self, chat_id):
        user = await self.col.find_one({"_id": chat_id})
        print(f"Data found for user ID {chat_id}: {user}")
        return user

    async def get_premium_users(self):
        return await self.col.find({'usertype': {'$ne': 'Non-Premium'}}).to_list(length=None)

    async def get_non_premium_users(self):
        return await self.col.find({'usertype': 'Non-Premium'}).to_list(length=None)

    async def total_users_count(self):
        return await self.col.count_documents({})

    def add_date(self):
        now = datetime.datetime.now()
        return now, now.date()

    async def getid(self):
        values = []
        async for key in self.col.find():
            id = key["_id"]
            values.append(id)
        return values

    async def delete(self, id):
        await self.col.delete_one({"_id": id})

    async def used_limit(self, chat_id, used):
        await self.col.update_one({"_id": chat_id}, {"$set": {"used_limit": used}})

    def new_user(self, id):
        return dict(
            _id=int(id),
            file_id=None,
            caption=None,
            prefix=None,
            suffix=None,
            metadata=False,
            metadata_code=""" -map 0 -c:s copy -c:a copy -c:v copy -metadata title="Powered By:- @Kdramaland" -metadata author="@Snowball_Official" -metadata:s:s title="Subtitled By :- @Kdramaland" -metadata:s:a title="By :- @Kdramaland" -metadata:s:v title="By:- @Snowball_Official" """
        )

    async def add_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id)
            await self.col.insert_one(user)
            await send_log(b, u)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'_id': int(user_id)})

    async def set_thumbnail(self, id, file_id):
        await self.col.update_one({'_id': int(id)}, {'$set': {'file_id': file_id}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('file_id', None)

    async def set_caption(self, id, caption):
        await self.col.update_one({'_id': int(id)}, {'$set': {'caption': caption}})

    async def get_caption(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('caption', None)

    async def set_prefix(self, id, prefix):
        await self.col.update_one({'_id': int(id)}, {'$set': {'prefix': prefix}})

    async def get_prefix(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('prefix', None)

    async def set_suffix(self, id, suffix):
        await self.col.update_one({'_id': int(id)}, {'$set': {'suffix': suffix}})

    async def get_suffix(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('suffix', None)

    async def set_metadata(self, id, bool_meta):
        await self.col.update_one({'_id': int(id)}, {'$set': {'metadata': bool_meta}})

    async def get_metadata(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('metadata', None)

    async def set_metadata_code(self, id, metadata_code):
        await self.col.update_one({'_id': int(id)}, {'$set': {'metadata_code': metadata_code}})

    async def get_metadata_code(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('metadata_code', None)

    # New methods to set and get media type
    async def set_media_type(self, user_id, media_type):
        """Set the media type preference for a user."""
        await self.col.update_one(
            {"_id": user_id},
            {"$set": {"media_type": media_type}},
            upsert=True
        )

    async def get_media_type(self, user_id):
        """Retrieve the media type preference for a user."""
        user_data = await self.col.find_one({"_id": user_id})
        return user_data.get("media_type") if user_data else None

db = Database(Config.DB_URL, Config.DB_NAME)
