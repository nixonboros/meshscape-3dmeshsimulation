from pymongo import UpdateOne
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from urllib.parse import quote_plus
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from documentSchema import create_document_schema

username = quote_plus('nixonboros')
password = quote_plus('qgZs4gYLGEGUJ6Ng')
cluster_url = '3dmeshgen.eqmrnic.mongodb.net'

uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = AsyncIOMotorClient(uri)

# Send a ping to confirm a successful connection
async def check_connection():
    try:
        # Send a ping to confirm a successful connection
        await client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print("Failed to connect:", e)

# Get the database and collection
db = client['3dmeshgen']  
collection = db['parameters']  

async def insert_document(*args):
    document = create_document_schema(*args)
    result = collection.insert_one(document)
    return result.inserted_id

async def delete_document(document_ids):
    result = collection.delete_many({'_id': {'$in': [ObjectId(id) for id in document_ids]}})
    return result.deleted_count

async def update_document(updates):
    # Prepare bulk update operations
    operations = []
    for update in updates:
        doc_filter = {'_id': ObjectId(update['documentId'])}
        updated_values = {'$set': update['update_values']}
        operations.append(UpdateOne(doc_filter, updated_values))
    
    if operations:
        result = await collection.bulk_write(operations)
        return result.bulk_api_result
    return None

async def find_document(query):
    cursor = collection.find(query)
    documents = collection.find(query)
    return list(documents)

# Master function to handle database operations
async def database(operation_type, entry):
    await client.start_session()
    try:
        result = None
        if operation_type == 'insert':
            result = await insert_document(*entry)
            print("Inserted IDs:", result)
        elif operation_type == 'delete':
            result = await delete_document(entry)
            print("Deleted count:", result)
        elif operation_type == 'find':
            result = await find_document(entry)
            print("Found documents:", result)
        elif operation_type == 'update':
            result = await update_document(entry)
            print("Updated count:", result)
        else:
            print("Invalid operation type.")
    finally:
        pass  # Handle any cleanup if necessary

# Example usage:
"""
if __name__ == "__main__":
    asyncio.run(check_connection())
"""