from pymongo import MongoClient
from django.conf import settings
from bson import ObjectId
from datetime import datetime

class WebsiteManager:
    def __init__(self):
        client = MongoClient(settings.MONGO_URI)
        self.db = client[settings.MONGO_DB_NAME]
        self.websites = self.db.websites

    def create_website(self, user_id, business_type, industry, structure):
        website = {
            'user_id': user_id,
            'business_type': business_type,
            'industry': industry,
            'structure': structure,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        result = self.websites.insert_one(website)
        return str(result.inserted_id)

    def get_website(self, website_id):
        return self.websites.find_one({'_id': ObjectId(website_id)})

    def get_user_websites(self, user_id):
        return list(self.websites.find({'user_id': user_id}))

    def update_website(self, website_id, data):
        data['updated_at'] = datetime.now()
        return self.websites.update_one(
            {'_id': ObjectId(website_id)},
            {'$set': data}
        )

    def delete_website(self, website_id):
        return self.websites.delete_one({'_id': ObjectId(website_id)})