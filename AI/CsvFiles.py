import os
from cryptography.fernet import Fernet, MultiFernet
from AI import EncryptionDecryption
import csv
from AI.Indexing import remove_dup
from AI.SpeakAndListen import *


def write_file(ADDRESSES, FileAddress="./AI/Searching/App/Index"):
    if not os.path.isdir(FileAddress.split("/")[0]):
        cmd = "mkdir " + FileAddress.replace(FileAddress.split("/")[-1], "")
        os.system(cmd)
    fields = ['name', 'address']
    with open(FileAddress + '.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(ADDRESSES)
        file.close()

    EncryptionDecryption.encrypt(FileAddress + ".csv")


def read_files(filename, fileaddress=""):
    try:
        results = []
        filename = "./" + fileaddress + "/" + filename + ".csv"
        EncryptionDecryption.decrypt(filename)
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for r in csv_reader:
                detail = {"name": r[0], "address": r[1]}
                results.append(detail)
            csv_file.close()
        EncryptionDecryption.encrypt(filename)

        return results
    except FileNotFoundError:
        return []


def append_files(newcontact, filename):
    contacts = read_files(filename, filename)
    contacts.append(newcontact)
    # contacts = remove_dup(contacts)
    write_file(contacts, filename)

# print(read_files("Index.csv", "Searching\\App"))
