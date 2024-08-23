from cryptography.fernet import Fernet
from prettytable import PrettyTable
import textwrap3
import sys
import os


# ----- Colors -----
RED = "\033[0;31m"
BLUE = "\033[0;34m"
BOLD= "\033[01;01m"
RESET = "\033[00m"
# -----------------


# Add a password in the file
def add_password():
    key = load_key()
    cipher_suite = Fernet(key)

    try:
        platform = input("\nEnter the platform  : ")
        site = input("Enter your email    : ")
        password = input("Enter your password : ")
    except KeyboardInterrupt:
        main()

    encrypted_pw = cipher_suite.encrypt(password.encode())

    with open("passwords.txt", "a") as file:
        file.write(f"{platform} | {site} | {encrypted_pw.decode()}\n")
    input(f"{BLUE}{BOLD}[+]{RESET} The Password has been successfully added!\nPress [ENTER] to continue.")



# Load all the passwords
def load_all_passwords():
    key = load_key()
    cipher_suite = Fernet(key)

    if not os.path.exists("passwords.txt"):
        input(f"{RED}{BOLD}[!]{RESET} There is no Password file, Can't load the passwords.\nPress [ENTER] to continue.")
        return
    
    try:
        table = PrettyTable(["Platform", "Email", "Password"])
        with open("passwords.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                platform, site, encrypted_password = line.strip().split(' | ')
                decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
                table.add_row([platform, site, decrypted_password])

        print()
        print(table)
        input("\nPress [ENTER] to continue.")
    except Exception as e:
        input(f"{RED}{BOLD}[!]{RESET} There is no Password written in the password file.\nPress [ENTER] to continue.")



# Delete all the passwords
def delete_all_passwords():
    try:
        with open("passwords.txt", "r") as file:
            pw = file.read()
    except FileNotFoundError:
        input(f"{RED}{BOLD}[!]{RESET} There is no any Password file.\nPress [ENTER] to continue.")
        main()

        if pw == " ":
            input(f"{RED}{BOLD}[!]{RESET} The Passwords have already been deleted.\nPress [ENTER] to continue.")
            main()

    choice = str(input(f"\n{BOLD}Are you sure you want to proceed? (Y/N):{RESET} ").lower()).strip()

    if choice == "y" or choice == "yes":
        with open("passwords.txt", "w") as file:
            file.write(" ")
            input(f"{BLUE}{BOLD}[+]{RESET} The Passwords were successfully deleted!\nPress [ENTER] to continue.")
    elif choice == "n" or choice == "no":
        main()
    else:
        input(f"{RED}{BOLD}[!]{RESET} Please type Yes or No.\nPress [ENTER] to continue.")
        delete_all_passwords()



# Delete the password file
def delete_password_file():
    if not os.path.exists("passwords.txt"):
        input(f"{RED}{BOLD}[!]{RESET} There is no any Password file.\nPress [ENTER] to continue.")
        main()

    choice = str(input(f"\n{BOLD}Are you sure you want to proceed? (Y/N):{RESET} ").lower()).strip()

    if choice == "y" or choice == "yes":
        os.remove("passwords.txt")
        input(f"{BLUE}{BOLD}[+]{RESET} The Password file was successfully deleted!\nPress [ENTER] to continue.")
    elif choice == "n" or choice == "no":
        main()
    else:
        input(f"{RED}{BOLD}[!]{RESET} Please type Yes or No.\nPress [ENTER] to continue.")



# Create a new key
def create_key():
    key = Fernet.generate_key()
    with open("secret.key", 'wb') as file:
        file.write(key)
    input(f"{BLUE}{BOLD}[+]{RESET} The key has been successfully generated!\nPress [ENTER] to continue.")



# Load the key
def load_key():
    with open("secret.key", "rb") as file:
        keyfile = file.read()
        return keyfile



# Delete the key
def delete_key():
    if not os.path.exists("secret.key"):
        input(f"{RED}{BOLD}[!]{RESET} There is no any Key file.\nPress [ENTER] to continue.")
    else:
        os.remove("secret.key")
        input(f"{BLUE}{BOLD}[+]{RESET} The Key has been successfully deleted!\nPress [ENTER] to continue.")



# Main
def main():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", 'wb') as file:
            file.write(key)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        logo = f"""
        {RED}██████╗ ██╗    ██╗    ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗ 
        ██╔══██╗██║    ██║    ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗
        ██████╔╝██║ █╗ ██║    ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝
        ██╔═══╝ ██║███╗██║    ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗
        ██║     ╚███╔███╔╝    ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║
        ╚═╝      ╚══╝╚══╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝{RESET}
        ===================================================================================={RESET}
         {RED}Author{RESET} : Swifter5                                                      Version {RED}1.0{RESET} 
        ===================================================================================={RESET}"""
        menu = f"""
        [{RED}1{RESET}] Add a new Password
        [{RED}2{RESET}] Load all the Passwords 
        [{RED}3{RESET}] Delete the all Passwords
        [{RED}4{RESET}] Delete the Password file
        [{RED}5{RESET}] Make a new Key 
        [{RED}6{RESET}] Delete the Key
        [{RED}7{RESET}] Exit"""
        
        logo = textwrap3.dedent(logo)
        menu = textwrap3.dedent(menu)
        print(logo)
        print(menu)

        try:
            choice = int(input("\nOption: "))
        except ValueError:
            input(f"{RED}{BOLD}[!]{RESET} Invalid option! Press [ENTER] to try again.")
            continue
        except KeyboardInterrupt:
            print()
            sys.exit(1)

        if choice == 1:
            add_password()
        elif choice == 2:
            load_all_passwords()
        elif choice == 3:
            delete_all_passwords()
        elif choice == 4:
            delete_password_file()
        elif choice == 5:
            create_key()
        elif choice == 6:
            delete_key()
        elif choice == 7:
            print()
            sys.exit(1)
        else:
            input(f"{RED}{BOLD}[!]{RESET} Invalid option! Press [ENTER] to try again.")


try:
    if __name__ == "__main__":
        main() 
except KeyboardInterrupt:
    print()
    sys.exit(1)