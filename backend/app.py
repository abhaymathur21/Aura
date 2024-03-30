
from flask import Flask, jsonify
from pymongo.mongo_client import MongoClient
from bson import json_util
import json

app = Flask(__name__)

uri = "mongodb+srv://abhaymathur21:itsmeright@codeshastra.lxorakw.mongodb.net/?retryWrites=true&w=majority&appName=Codeshastra"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client["Accounts"]

    
@app.route('/', methods=['GET','POST'])
def index():
    
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        # Example: Retrieve documents from a collection
    collection = db["User1"]
    # documents = collection.find({})
    # result = [json.loads(json_util.dumps(doc)) for doc in documents]  # Convert ObjectId to string
    # print(result)
    
    document = {
        "userID": 1,
        "userName": "Abhay Mathur",
        "chatHistory": "example_text",
        "modelName": "example_model.h5"
    }

    # Insert the document into the collection
    collection.insert_one(document)
    
    message = "Document inserted successfully."
    return message


if __name__ == '__main__':
    app.run(debug=True)