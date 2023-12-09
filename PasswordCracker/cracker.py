import hashlib
import os
import datetime


def log_event(event, result):
    with open("password_cracker_log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] Event: {event}, Result: {result}\n")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_file_exists(filename):
    return os.path.exists(filename)

def add_to_file(resource, content):
    hashed_content = hash_password(content)
    with open(resource, 'a') as file:
        file.write(hashed_content + "\n")
        log_event("Add Password", f"Password added: {content}")

def search_and_update_file(resource, password):
    hashed_password = hash_password(password)
    with open(resource, 'r') as file:
        lines = file.read().splitlines()
        if password in lines:
            return f"The password '{password}' exists in the database, please choose another password."
        if hashed_password in lines:
            return f"The password '{password}' exists in the database, please choose another password."
        log_event("Search Password", f"Password exist: {password}")

    add_to_file(resource, password)
    return "Password is considered safe and has been hashed and added to the database."

def main():
    print("This program is used for detecting whether your password is being cracked or not")
    resource = input("Enter the filename for the password list: ")
    if not check_file_exists(resource):
        print("Error: File not found.")
        return
    
    while True:
        mode = input("Enter 'search' to search or 'add' to add content (or 'exit' to exit): ").strip().lower()
        
        if mode == "add":
            password = input("Enter password to add to the cracked list: ")
            add_to_file(resource, password)
            print("New password is added to the password list.")
        
        elif mode == "search":
            password = input("Enter password to search: ")
            result = search_and_update_file(resource, password)
            print(result)

        elif mode == "exit":
            break
        else:
            print("Error. Please enter 'search', 'add', or 'exit'.")

if __name__ == "__main__":
    main()
