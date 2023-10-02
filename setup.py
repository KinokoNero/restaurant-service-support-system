from pymongo import MongoClient
from security import hash_password
from qr import qr_codes_directory
from gridfs import GridFS
import os

client = MongoClient("mongodb://localhost:27017/")
db = client["r3s"]
fs = GridFS(db)

# Database and disk QR code clearing
fs_files = fs.find()
for fs_file in fs_files:
    fs.delete(fs_file._id)

disk_files = os.listdir(qr_codes_directory)
for filename in disk_files:
    file_path = os.path.join(qr_codes_directory, filename)
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file: {file_path}, {e}")

# Database setup
collections = ["menu", "orders", "users"]
for collection in collections:
    db[collection].drop()
    if collection not in db.list_collection_names():
        db.create_collection(collection)
        print(f"Collection '{collection}' created successfully.")
    else:
        print(f"Collection '{collection}' already exists!")

# Admin user setup
admin_username = input("Podaj nazwę użytkownika do logowania administratora: ")
admin_password = input("Podaj hasło do logowania administratora: ")
hashed_password, salt = hash_password(admin_password)

admin_document = {
    'username': admin_username,
    'password': hashed_password,
    'salt': salt,
    'role': 'Admin'
}

result = db["users"].insert_one(admin_document)
if result.acknowledged:
    print('Admin user added successfully.', 'success')
else:
    print('Failed to add admin user!', 'danger')