from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
import boto3
import os
from dotenv import load_dotenv

# Access MongoDB Atlas Cluster
load_dotenv()
connection_string: str = os.environ.get("CONNECTION_STRING")
access_id: str = os.environ.get("aws_access_key_id")
access_key: str = os.environ.get("aws_secret_access_key")

app = Flask(__name__)

app.config["MONGO_URI"] = connection_string
mongo = PyMongo(app)

cors = CORS(app)

s3_resource = boto3.resource(
    service_name = "s3",
    region_name = 'us-east-1',
    aws_access_key_id = access_id,
    aws_secret_access_key = access_key

)
s3_client = boto3.client(
    service_name = "s3",
    region_name = 'us-east-1',
    aws_access_key_id = access_id,
    aws_secret_access_key = access_key)

from app import routes