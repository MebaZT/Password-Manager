import sys
import argparse # For managing the command inputs and output
from tabulate import tabulate # For formatting and making the names and passwords in a table
from password_generator import PasswordGenerator # Generates a random password if needed
import csv # Manages the storing and editing of the csv file

pwo = PasswordGenerator()

storage = []
with open("storage.csv", "r") as file: # Gets the username and password as a dict
    reader = csv.DictReader(file)
    for row in reader:
        storage.append(row)
users = []
for items in storage: # Gets a list of usernames from the storage
    users.append(items.get("username"))

passwords = []
for items in storage: # Gets a list of passwords from the storage
    passwords.append(items.get("password"))

def main():
    global storage, users, passwords
    try:
        parse = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('''\
                    Password Manager
   -----------------------------------------------------
   Allows the user to manage their username and password
        '''),
        epilog="NOTE:- You can only run one command at a time" \
      "\n     - You can exit by pressing Ctrl + D")
        manager = parse.add_mutually_exclusive_group(required=True)
        manager.add_argument("-a", "--add", help="Requires a username and password, can generate a password or allows to be inputted manually, " \
                                                    "then inputs the information into a file",
                                            action="store_true")
        manager.add_argument("-e", "--edit", help="Allows the user to edit a username's password",
                                            action="store_true")
        manager.add_argument("-r", "--remove", help="Allows the user to remove a certain username with it's password",
                                            action="store_true")
        manager.add_argument("-s", "--show", help="Show specific all of the names and passwords",
                                            action="store_true")
        manager.add_argument("-sn", "--search_username", dest="username", metavar="username", nargs="?", const=True,
                                                help="Shows a specific username's password, unless a duplicate")
        manager.add_argument("-sp", "--search_password", dest="password", metavar="password", nargs="?", const=True,
                                                help="Allows the user to reverse search a specific name/s by inputting its password, even if duplicates exist")
        manage = parse.parse_args()

        if manage.add:
            user, password = adding()
            with open("storage.csv", "a") as file: # Appends the output to the last line
                writer = csv.DictWriter(file, fieldnames=["username","password"])
                writer.writerow({"username": user, "password": password})
        elif manage.edit:
            storage_new = editing()
            with open("storage.csv", "w") as file:
                writer = csv.DictWriter(file, fieldnames=["username","password"])
                writer.writeheader()
                for row in storage_new:
                    writer.writerow(row)
        elif manage.remove:
            remove_user = removing()
            with open("storage.csv", "w") as file:
                writer = csv.DictWriter(file, fieldnames=["username","password"])
                writer.writeheader()
                for row in storage:
                    if row["username"] != remove_user:
                        writer.writerow(row)
                print(f"Successfully removed the account with user {remove_user}")
        elif manage.show:
            print(showing())
        elif manage.username:
            table = [searching_name(manage.username)]
            print(tabulate(table, headers="keys",tablefmt="grid"))
        elif manage.password:
            tables = searching_password(manage.password)
            print(tabulate(tables, headers="keys", tablefmt="grid"))


    except EOFError:
        warning(3)

def warning(n): # A function that can be called to warn the user
    if n == 1:
        print("Type c to cancel and exit or Press ctrl + D to exit the program")
    if n == 2:
        print("All of your usernames and passwords will be revealed. Are you sure do you want to continue?")
    if n == 3:
        sys.exit("\nProgram exited")

def check_user(user):
    if user in users:
        return True
    if user:
        return True

def check_password(password):
    if " " in password:
        return False
    if 4 <= len(password) <= 20:
        return True
    else:
        return False


def adding():
    global storage, users, passwords
    user = None
    password = None
    while True: # Validates the username, by empty checking and if it already exists
        user = input("What is the username/name: ").strip()
        if user in users:
            print("The username already exists, please input a valid one")
            continue
        elif (not user) or " " in user:
            print("Please input a valid username")
            continue
        if 1 <= len(user) <= 30:
            break
    choice = input("Do you want a random password generation or manually enter it? (r/m): ").lower().strip()
    while True:
        if choice == "r": # Generates a random password
            pwo.maxlen = 20
            pwo.excludeschars = "\"\'<>&\\()[]{}|^;:`~#.,"
            password = pwo.generate()
            print(f"Here is your randomly generated password: {password}")
            break
        elif choice == "m": # Adds the entered password
            password = input("Please enter your password: ").strip()
            if check_password(password):
                print(f"Password set: {password}")
                break
            else:
                print("Invalid password, please input a valid password")
        elif choice == "c":
            warning(3)
        else:
            print("Please enter a valid response")
            choice = input("Random generation or Manual or Cancel? (r/m/c): ").lower().strip()
    return (user, password)


def editing():
    global storage, users, passwords
    choice = input("Do you want to edit your password or username? (u/p): ").lower().strip()
    while True:
        if choice == "u": # Edits the username
            user = input("The username you want to edit: ").strip()
            if user in users:
                new_user = input("The new username you want to assign: ").strip()
                if " " in new_user:
                    print("Please input a valid username")
                    continue
                if new_user in users:
                    print("Username already exists, Input a valid one")
                    continue
                for item in storage:
                    if item["username"] == user:
                        item["username"] = new_user
                break
            else:
                print("User not found")
        elif choice == "p": # Edits the password
            user = input("The username you want to edit: ").strip()
            if user in users:
                new_password = input("The new password you want to assign: ").strip()
                while True:
                    if check_password(new_password):
                        break
                    else:
                        new_password = input("Invalid password, please input a valid one: ").strip()
                for item in storage:
                    if item["username"] == user:
                        item["password"] = new_password
                break
            else:
                print("User not found")
        else:
            print("Invalid choice")
            choice = input("Please choose password or username? (u/p): ").lower().strip()
    return storage


def removing():
    global storage, users, passwords
    while True:
        remove_user = input("The user you want to remove: ").strip()
        if check_user(remove_user):
            if remove_user in users:
                return remove_user
            else:
                print("User not found")
        else:
            print("User not found")


def showing():
    global storage, users, passwords
    answer = input("Are you sure, All your passwords will be shown? (y/n): ").lower().strip()
    if answer == "yes" or answer == "y":
        table_all = tabulate(storage, headers="keys", tablefmt="grid")
        return table_all
    else:
        warning(3)


def searching_name(user):
    global storage, users, passwords
    if user != True:
        pass
    elif user == True:
        user = input("The username you want to see the password of: ").strip()
    if user in users:
        for item in storage:
            if item["username"] == user:
                return item
    else:
        sys.exit("User not found")


def searching_password(password):
    global storage, users, passwords
    requests = []
    if password != True:
        pass
    elif password == True:
        password = input("The password you want to see the username/s of: ").strip()
    if password in passwords:
        for item in storage:
            if item["password"] == password:
                requests.append(item)
    else:
        sys.exit("Password not found")
    return requests



if __name__ == "__main__":
    main()
