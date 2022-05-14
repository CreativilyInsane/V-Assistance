from cryptography.fernet import Fernet



def write_key(key):

    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key(Filename):
    with open(Filename+":key.key", "rb") as key:
        key = key.read()
    return key

def encrypt(filename):
    key = Fernet.generate_key()
    write_key(key)
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)
    hide_key(filename)


def decrypt(filename):
    key = load_key(filename)
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(filename, "wb") as file:
        file.write(decrypted_data)

def hide_key(filename, keyname="key.key"):
    import os
    cmd = "type "+ keyname +" > "+filename+":"+keyname
    os.system(cmd),os.system("del key.key")


def gmail_crediential_encrypt(email, password):
    encrypted_string = []
    key = Fernet.generate_key()
    f = Fernet(key)
    write_key(key)
    email = f.encrypt(email)
    password = f.encrypt(password)
    hide_key("Data/email.csv")
    return email, password

def gmail_crediential_decrypt(email, password):
    decrypted_string = []
    key = load_key("Data/email.csv")
    f = Fernet(key)
    email = f.decrypt(email)
    password = f.decrypt(password)
    return email, password
