from pymongo import MongoClient

from information_technologies.settings import MONGO_USERNAME, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT, MONGO_NAME

client = MongoClient(
    f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_NAME}?authSource=admin'
)

db = client[MONGO_NAME]

students_collection = db.students
