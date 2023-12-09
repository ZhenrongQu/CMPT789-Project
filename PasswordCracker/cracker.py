import pymongo
import hashlib
import datetime

# Replace 'your_mongodb_url' with your actual MongoDB URL
MONGO_URL = "mongodb://localhost:27017/"
client = pymongo.MongoClient(MONGO_URL)

# Connect to the specific database and collections
db = client['CMPT789-Project']
local_db = client['local']
admin_info_collection = local_db['adminInfo']
password_list_collection = local_db['Password-list1']
hashed_password_list_collection = local_db['hashedPassword-list1']
event_log_collection = local_db['event_log']

# Function to hash a password
def hash_input(input):
    return hashlib.sha256(input.encode()).hexdigest()

# Function to check user credentials
def check_user_credential(input_user_name, input_password):
    
    # 这里的字段名'Username'和'Password'是根据您的MongoDB集合中的字段来的
    user_document = admin_info_collection.find_one({'Username': input_user_name, 'Password': input_password})
    hashed_user_document = admin_info_collection.find_one({'Username': hash_input(input_user_name), 'Password': hash_input(input_password)})
    if user_document or hashed_user_document:
        # 如果找到匹配的文档，则返回对应的Role
        print("Login success! Welcome, " + input_user_name)
        log_event("Login as: " + input_user_name, " success!")
        return user_document['Role']        
    else:
        # 如果没有找到匹配的文档，则返回错误信息
        return 'error'

# Function to create a new user
def create_user(input_user_name, input_password):
    new_user_name = admin_info_collection.find_one({'Username': input_user_name})
    if  new_user_name:
        log_event("Create new user: " + input_user_name, " failed! User already exist.")
        print("User already exists!")
    else:
        admin_info_collection.insert_one({
            'Username': input_user_name,
            'Password': hash_input(input_password),
            'Role': 'user'
        })
        log_event("Create new user: " + input_user_name, " success!")
        return "User created!"

# Function to search for a password
def search_password(input_password):
    plain_password = input_password
    hashed_password = hash_input(plain_password)
    if (password_list_collection.find_one({'Password': input_password}) or
            hashed_password_list_collection.find_one({'Password': hashed_password})):
        log_event("Search Password :" + input_password, "Password exist")
        return True
    else:
        add_password(hashed_password)
        log_event("Search Password :" + input_password, "Password not exist")
        return False

# Function to add a password
def add_password(input_password):
    plain_password = input_password
    hashed_password = hash_input(plain_password)
    password_list_collection.insert_one({'Password': input_password})
    hashed_password_list_collection.insert_one({'Password': hashed_password})
    log_event("Add Password: " + input_password, " success!")

    

# Function to log events
def log_event(event, result):
    with open("password_cracker_log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] Event: {event}, Result: {result}\n")

# Main program logic
def main():
    while True:
        print("This program is used for detecting whether your password is being cracked or not")
        print("Choose option: 1. Existing user 2. New user 3. Exit")
        choice = input()
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = check_user_credential(username, password)
            if role == 'error':
                print("Invalid credentials. Do you want to create a new user? (yes/no)")
                if input().lower() == 'yes':
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    create_user(username, password)             
                else:
                    print("Invalid input, please try again. Do you want to create a new user? (yes/no)")
            else:
                while True:
                    if role == 'admin':
                        print("Choose mode: 1. Search 2. Add 3. Check log 4. Log out")
                        admin_choice = input()
                        if admin_choice == '1':
                            password = input("Enter password to search: ")
                            if search_password(password):
                                print("Password already exist, please choose another password.")
                            else:
                                print("Password not been used yet, congratulations.")
                                add_password(password)
                        elif admin_choice == '2':
                            password = input("Enter password to add into the database: ")
                            add_password(password)
                            print("Add password into DB successful")
                        elif admin_choice == '3':
                            # Retrieve and display logs
                            pass
                        elif admin_choice == '4':
                            print("Log out as" + username)
                            log_event("Log out as: " + username, " success!")
                            break
                    elif role == 'user':
                        user_choice = input("Choose mode:1. Search  2. Exit")
                        if user_choice == '1':
                            password = input("Enter password to search: ")
                            if search_password(password):
                                print("Password exists.")
                            else:
                                print("Password is safe.")
                        elif user_choice == '2':
                            return
                else:
                    break
        elif choice == '2':
            username = input("Enter new username: ")
            password = input("Enter new password: ")
            print(create_user(username, password))
        elif choice == '3':
            print("Good bye.")
            break
        else:
            print("Invalid input, please try again.")

if __name__ == "__main__":
    main()
