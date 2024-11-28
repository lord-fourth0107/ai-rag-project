from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Adjust the connection string as needed
client = MongoClient("mongodb://admin:#rag_project@localhost:27017/?authSource=admin")

db = client['admin']  # Replace 'myDatabase' with your database name
collection = db['local']  # Replace 'myCollection' with your collection name

# Read the text file
with open("/Users/sreeharshnamani/Downloads/Assignments_NYU/ai_rag/sentences.txt", "r") as file:  # Replace with the path to your text file
    file_content = file.read()

# Create a document
document = {
    "file_name": "sentences.txt",  # You can include the file name
    "content": file_content  # Store the file content as a string
}

# Insert the document into the collection
result = collection.insert_one(document)
print(f"Document inserted with ID: {result.inserted_id}")
