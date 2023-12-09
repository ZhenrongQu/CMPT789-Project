import hashlib

def generate_rainbow_table():
    rainbow_table = {}
    
    # For simplicity, create a small set of passwords
    passwords = ['password', '123456', 'qwerty', 'letmein', 'admin', 'welcome']

    for password in passwords:
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        rainbow_table[hashed_password] = password

    return rainbow_table

def rainbow_table_cracker(hashed_password, rainbow_table):
    if hashed_password in rainbow_table:
        return rainbow_table[hashed_password]
    else:
        return None

# Example usage
if __name__ == "__main__":
    # Generate a rainbow table (precomputed hash values)
    my_rainbow_table = generate_rainbow_table()

    # Hashed password to crack (you would replace this with the actual hash you want to test)
    target_hash = hashlib.md5('letmein'.encode()).hexdigest()

    # Attempt to crack the password using the rainbow table
    cracked_password = rainbow_table_cracker(target_hash, my_rainbow_table)

    if cracked_password:
        print(f"Password cracked: {cracked_password}")
    else:
        print("Password not found in the rainbow table.")
