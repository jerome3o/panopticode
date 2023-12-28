import os


MONGODB_CONNECTION_STRING = os.environ.get(
    "MONGODB_CONNECTION_STRING",
    "mongodb://localhost:27017",
)
MONGODB_DATABASE = os.environ.get(
    "MONGODB_DATABASE",
    "panopticode",
)


MONGODB_COLLECTION_NAME = "daily_self_report"
