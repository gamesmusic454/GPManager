import os
from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

DB_USERNAME = os.getenv("DB_ROOTUSERNAME")
DB_PASSWORD = os.getenv("DB_ROOTPASSWORD")
DB_NAME = 'Inventory'
MONGO_HOST = 'localhost:27020'

MONGO_URI = f"mongodb://{quote_plus(DB_USERNAME)}:{quote_plus(DB_PASSWORD)}@{MONGO_HOST}/{DB_NAME}?authSource=admin"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

app = FastAPI()

@app.get("/")
async def root():
    return {"body": "Hello World"}

@app.get("/products")
async def get_products():
    result = []
    for product in db.get_collection('ProductData').find({}):
        result.append(product)

    return {"products": str(result)}
        


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)