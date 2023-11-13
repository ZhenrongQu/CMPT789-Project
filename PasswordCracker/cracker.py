import hashlib

#This function is used to store the password in hash value to improve the security. New password and password list will be stored as hash(SHA256).
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_to_file(password_list, content):
    hashed_content = hash_password(content)
    with open(password_list, 'a') as file:
        file.write(hashed_content + "\n")

def search_and_update_file(password_list, password):
    hashed_password = hash_password(password)
    with open(password_list, 'r') as file:
        hashes = file.read().splitlines()
        if hashed_password in hashes:
            return "The password '{password}' exists in the file."

    add_to_file(password_list, password)
    return "Password is considered safe and has been hashed and added to the file."
                

def main():
    password_list = "password-list.txt"
    while True:
        print("This program is used for detecting whether your password is being cracked or not")
        mode = input("Enter 'search' to search or 'add' to add content (or 'exit' to exit): ").strip().lower()
        
        if mode == "add":
            password = input("Enter password to add to the cracked list: ")
            add_to_file(password_list, password)
            print("New password is added to the password list.")
        
        elif mode == "search":
            password = input("Enter password to search: ")
            search_and_update_file(password_list, password)

        elif mode == "exit":
            break
        else:
            print("Error. Please enter 'search' or 'add' or 'exit'.")

if __name__ == "__main__":
    main()

