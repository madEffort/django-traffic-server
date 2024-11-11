from decouple import config

# Mongo 클라이언트 설정
MONGO_USER = config("MONGO_USER")
MONGO_PASSWORD = config("MONGO_PASSWORD")
MONGO_HOST = config("MONGO_HOST")
MONGO_PORT = config("MONGO_PORT")
MONGO_DB_NAME = config("MONGO_DB_NAME")
