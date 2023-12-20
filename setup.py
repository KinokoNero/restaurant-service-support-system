from pymongo import MongoClient
from security import hash_password
from gridfs import GridFS

client = MongoClient('mongodb://localhost:27017/')
db = client['r3s']
fs = GridFS(db)

# Database QR code clearing
fs_files = fs.find()
for fs_file in fs_files:
    fs.delete(fs_file._id)

# Database setup
collections = ['menu', 'orders', 'requests', 'users']
for collection in collections:
    db[collection].drop()
    if collection not in db.list_collection_names():
        db.create_collection(collection)
        print(f'Kolekcja "{collection}" została utworzona pomyślnie.')
    else:
        print(f'Kolekcja "{collection}" już istnieje.')


# Admin user setup
def get_non_empty_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.strip():
            return user_input
        else:
            print('Wartość nie może być pusta!')


admin_username = get_non_empty_input('Podaj nazwę użytkownika do logowania administratora: ')
admin_password = get_non_empty_input('Podaj hasło do logowania administratora: ')
hashed_password, salt = hash_password(admin_password)

admin_document = {
    'name': admin_username,
    'password': hashed_password,
    'salt': salt,
    'role': 'admin'
}

result = db['users'].insert_one(admin_document)
if result.acknowledged:
    print('Pomyślnie utworzono konto administratora.')
else:
    print('Nie udało się utworzyć konta administratora!')

print('Inicjalizacja systemu zakończona pomyślnie!')
