# TERMUX FORK BY @NOLABJFJDJ ON GITHUB

try: # Trying to import the required packages & functions
    from config import TiktokUsernameChecker
    from config import os, time
    from config import Fore, init
    from username_generator import username_generator
    from checker import checker_main
    from update_title import update_title
    from clear_usernames import clear_usernames

except ImportError as package_not_installed: # If ImportError is raised, error message is sent.
    input(f"{package_not_installed} is installed. Please follow the instructions on github.\nPress enter to exit the program.")
    raise SystemExit(0)


def main():
    """
    Main function which holds the main menu for the program.
    """
    while True:
        update_title("main")
        time.sleep(0.5)
        print("\n\n" + TiktokUsernameChecker.title + "\n\n")
        print("[1] Start the TikTok Username Checker")
        print("[2] Username Generator")
        print("[3] Clear 'usernames.txt' and cache")
        print("[4] Exit\n")

        while True:
            event = input("Your choice: ").strip()
            if event in ["1", "2", "3", "4"]:
                menu = int(event)
                break
            print(Fore.RED + "\nChoose either 1, 2, 3 or 4.\n")

        if menu == 1:
            while True:
                print("How many threads do you want to use? (1-9)\n")
                threads = input("Your choice: ").strip()
                if threads.isdigit() and 1 <= int(threads) <= 9:
                    TiktokUsernameChecker.threads = int(threads)
                    break
                print(Fore.RED + "\nYou must choose an integer between 1-9.\n")
            checker_main()

        elif menu == 2:
            username_generator()

        elif menu == 3:
            clear_usernames()

        elif menu == 4:
            raise SystemExit(0)


if __name__ == "__main__":
    init(autoreset=True) # Initiate colorama in terminal

    latest_version = TiktokUsernameChecker.check_for_updates(update=False)
    if latest_version == TiktokUsernameChecker.version: # If user has the latest version - continue
        pass
    else:
        while True:
            update = input(f"You are using an outdated version!\nVersion installed: {TiktokUsernameChecker.version}\nLatest version: {latest_version}\n\nDo you want to update to the latest version? (yes/no)\n\nYour choice: ").lower()
            if update == "yes":
                latest_url = TiktokUsernameChecker.check_for_updates(update=True)
                print(Fore.GREEN + f"\nHere you can download the latest version: {latest_url}\n")
                input("Press enter to exit the program.")
                raise SystemExit(0)
            elif update == "no":
                break
            else:
                print(Fore.RED + "\nYou must choose either yes or no.\n")
                time.sleep(2.5)

    while True:
        try:
            f = TiktokUsernameChecker.WriteOrRead("usernames.txt", "r")
            TiktokUsernameChecker.usernames = {line.strip() for line in f}
            f.close()
        except FileNotFoundError:
            f = TiktokUsernameChecker.WriteOrRead("usernames.txt", "x")
            f.close()

        main()
