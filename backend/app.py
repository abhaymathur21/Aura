from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from bson import json_util
import json
from chatbot import llm_model, rag_llm
import base64
import io
import os
import bcrypt
from pydub import AudioSegment
from keras.models import load_model
from voice_recognition import classify_audio
from functionalities.text_conversion import read_text_from_pdf, read_text_from_image
from flask_cors import CORS,cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type' 
uri = "mongodb+srv://abhaymathur21:itsmeright@codeshastra.lxorakw.mongodb.net/?retryWrites=true&w=majority&appName=Codeshastra"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client["Accounts"]
source_folder = r"C:\Users\a21ma\OneDrive\Desktop"
# source_folder = "C:/Users/a21ma/OneDrive/Desktop"

#define a global variable for personID every time voice is recognized
personName = "Abhay"    

@app.route("/add_person", methods=['POST'])
def add_person():
    
    document = request.get_json()
    
    # Create a new collection or get the existing collection
    collection = db["User"+document["userID"]]
    # documents = collection.find({})
    # result = [json.loads(json_util.dumps(doc)) for doc in documents]  # Convert ObjectId to string
    # print(result)
    document["password"] = bcrypt.hashpw(document["password"].encode("utf-8"), bcrypt.gensalt())

    # Insert the document into the collection
    collection.insert_one(document)
    
    message = "Document inserted successfully."
    
    # Example Input:
    # {
    #     "personID": "1",
    #     "personName": "person1",
    #     "userID": "1",
    #     "userName": "User1",
    #     "password": "password",
    #     "chatHistory": "chat_history",
    #     "location": "location",
    #     "modelName": "model_name.h5"
    # }
    
    print(message)
    return message


@app.route("/update_person/<int:userID>", methods=['POST'])
def update_person(userID):
    
    data = request.get_json()
    
    chat_history = data["messages"]
        
    collection = db["User"+str(userID)]
    # Find the document to update
    
    query = {"personName": personName} #personID is a global variable that is set every time voice is recognized
    
    document = collection.find_one(query)
    print(document)
    if document:
        # Update the fields of the document
        # document["personName"] = data["personName"] if data["personName"] else document["personName"]
        document["chatHistory"] = chat_history if chat_history else document["chatHistory"]

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
    

@app.route("/upload_file", methods=['POST'])
@cross_origin()
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files.get('file')
    user_input = request.files.get('message')
    
    # Validate file
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400  

    # Check if file type is supported
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".pdf")):
        return jsonify({"error": "Unsupported file format"}), 400

    
    if file.filename.lower().endswith(".pdf"):
        
        # filename = os.path.join(source_folder, r"Codeshastra X\backend\uploaded_pdfs", file.filename)
        # filename = f"{source_folder}/Codeshastra X/backend/uploaded_pdfs/{file.filename}"
        filename = "backend/uploaded_pdfs/" + file.filename

        file.save(filename)
        file_text = read_text_from_pdf(filename)
        
 
    if file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
        
        file_text = read_text_from_image(file) 
        
        
    rag_response = rag_llm(user_input, file_text)
    
    return jsonify({"data": rag_response}), 200
        
        
@app.route("/audio/<int:userID>", methods=['POST'])
def audio(userID):
    
    if 'audio' not in request.files:
        return jsonify({"error": "No audio uploaded"}), 400
    
    blob_data= request.files['audio']
    
    # file_path = os.path.join(source_folder, r"Codeshastra X\backend\uploaded_audios", blob_data.filename)
    # full_file_path = f"{source_folder}/Codeshastra X/backend/uploaded_audios/{blob_data.filename}"
    file_path = "backend/uploaded_audios/" + blob_data.filename
    blob_data.save(file_path)
    print(file_path)
    # audio_seg = AudioSegment.from_file(file_path, format="wav")
    
    model_path = r"backend\audio_classification_model.h5"
    model = load_model(model_path)
    
    full_file_path = "backend\\uploaded_audios\\" + blob_data.filename
    
    prediction_name = classify_audio(full_file_path, model)
    print(prediction_name)
    
    global personName
    personName = prediction_name
    
    if personName == "None":
        return jsonify({"data": "You are not authorized into the system"}), 400
    
    collection = db["User"+str(userID)]
    # Query the collection for documents where the modelName matches prediction_name
    matching_document = collection.find({"personName": personName})

    # chat_history = matching_document["chatHistory"]
    
    return jsonify({"classification": prediction_name}), 200


@app.route("/llm_chatbot/<int:userID>", methods=['POST'])
def llm_chatbot(userID):
    
    data = request.get_json()
    input_string = data.get("message")
    
    print('Received string:', input_string)
    
    if personName == "None":
        return jsonify({"data": "You are not authorized into the system"}), 400
    
    collection = db["User"+str(userID)]
    
    query = {"personName": personName} #personName is a global variable that is set every time voice is recognized
    
    document = collection.find_one(query)
    
    chat_history = document["chatHistory"]
    location = document["location"]
    print(chat_history)

    
    response = llm_model(input_string, chat_history, location)
    # print(response)
    return jsonify({"data":response})
    

if __name__ == '__main__':
    app.run(debug=True)