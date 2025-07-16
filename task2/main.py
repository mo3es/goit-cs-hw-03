from pymongo import MongoClient
from pymongo.server_api import ServerApi
from crud_files import menu

connection_string = (
    "mongodb+srv://<username>:<passwd>@mo3escluster.fk7q6nz.mongodb.net/"
)
client = MongoClient(connection_string, server_api=ServerApi("1"))

db = client.animals


if __name__ == "__main__":
    menu.menu(db)
