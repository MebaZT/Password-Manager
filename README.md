# Password Manager
#### Video Demo: https://youtu.be/GoHa1Vtmx6E

#### Description
Hi, This is my CS50 final project and it is a password manager. The password manager I built is a terminal-based program that allows you to **create**, **edit**, **remove**, and **observe** the accounts you saved in the terminal. All saved files are stored in a CSV file called **"storage.csv"**.

The library I used to manage the terminal-based commands is **argparse**, which allows you to detect flags and get arguments. After getting those arguments, the Python program looks at the flag and sends it to its corresponding function using the main function. These functions read and edit the `storage.csv` file using the **csv** library.

It also has a help menu called by the flag **-h** or **--help**. If you are in the middle of running the program and want to exit, you can do so by pressing **Ctrl + D**.

### Features

1.  **Add Account (`-a` / `--add`)**:
    - Asks for a username (max 30 characters, no duplicates).
    - Asks for a password:
        - **"m"**: Manually enter a password.
        - **"r"**: Generate a random password (6-20 digits) using the **password_generator** library.
    - Saves data to `storage.csv`.

2.  **Edit Account (`-e` / `--edit`)**:
    - Asks for the username of the account to edit.
    - Press **"u"** to edit the username or **"p"** to edit the password.

3.  **Remove Account (`-r` / `--remove`)**:
    - Removes a specific username and its password from the storage.

4.  **Show All (`-s` / `--show`)**:
    - Displays all usernames and passwords in a tabular form using the **tabulate** library.

5.  **Search Username (`-sn` / `--search_username`)**:
    - Shows a specific username's password.
    - Usage: `python project.py -sn [username]` or just `-sn` to be prompted.

6.  **Search Password (`-sp` / `--search_password`)**:
    - Reverse search: Input a password to see which accounts use it.
    - Usage: `python project.py -sp [password]` or just `-sp` to be prompted.
