from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from bson import json_util
import json
from chatbot import llm_model

app = Flask(__name__)

uri = "mongodb+srv://abhaymathur21:itsmeright@codeshastra.lxorakw.mongodb.net/?retryWrites=true&w=majority&appName=Codeshastra"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client["Accounts"]
    
@app.route("/add_person", methods=['POST'])
def add_person():
    
    document = request.get_json()
    
    # Create a new collection or get the existing collection
    collection = db["User"+document["userID"]]
    # documents = collection.find({})
    # result = [json.loads(json_util.dumps(doc)) for doc in documents]  # Convert ObjectId to string
    # print(result)
    
    # Insert the document into the collection
    collection.insert_one(document)
    
    message = "Document inserted successfully."
    
    # Example Input:
    # {
    #     "personID": "1",
    #     "personName": "person1",
    #     "userID": "1",
    #     "userName": "User1",
    #     "chatHistory": "chat_history",
    #     "modelName": "model_name.h5"
    # }
    
    print(message)
    return message


@app.route("/update_person", methods=['POST'])
def update_person():
    
    data = request.get_json()
    
    collection = db["User"+data["userID"]]
    # Find the document to update
    
    query = {"personID": data["personID"]}
    
    document = collection.find_one(query)
    print(document)
    if document:
        # Update the fields of the document
        document["personName"] = data["personName"] if data["personName"] else document["personName"]
        document["chatHistory"] = data["chatHistory"] if data["chatHistory"] else document["chatHistory"]
        document["modelName"] = data["modelName"] if data["modelName"] else document["modelName"]

        document = {
            "$set": document
        }
        
        # Save the updated document
        collection.update_one(query, document)
        
        message = "Document updated successfully."

        
    else:
        message = "Document not found."
        
    # Example input: 
    # {
    #     "personID": "1",
    #     "personName": "",
    #     "userID": "1",
    #     "chatHistory": "updated_chat_history",
    #     "modelName": ""

    # }    
    
    print(message)
    return message
    
    
@app.route("/delete_person", methods=['POST'])
def delete_person():
    
    data = request.get_json()
    
    collection = db["User"+data["userID"]]
    # Find the document to delete
    document = collection.find_one({"personID": data["personID"]})
    
    if document:
        # Delete the document
        collection.delete_one({"personID": data["personID"]})
        
        message = "Document deleted successfully."
    else:
        message = "Document not found."
        
    # Example input:
    # {
    #     "personID": "1",
    #     "userID": "1"
    # }
    
    print(message)
    return message
    

@app.route("/llm_chatbot", methods=['GET', 'POST'])
def llm_chatbot():
    
    if request.method == "POST":
        data = request.get_json()
        input_string = data.get('message')
        
        print('Received string:', input_string)
        
        response = llm_model(input_string)
        # print(response)
        return response



if __name__ == '__main__':
    app.run(debug=True)