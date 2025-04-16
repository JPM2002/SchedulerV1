import os
import time
import questionary
from datetime import datetime


CONFIG_FOLDER = "config"
API_KEY_FILE = os.path.join(CONFIG_FOLDER, "api_key.txt")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_logo():
    logo = r"""
   ______                               ________    ____  
  / ____/___ _____ _   ______ ______   / ____/ /   /  _/  
 / /   / __ `/ __ \ | / / __ `/ ___/  / /   / /    / /    
/ /___/ /_/ / / / / |/ / /_/ (__  )  / /___/ /____/ /     
\____/\__,_/_/ /_/|___/\__,_/____/   \____/_____/___/     
"""
    print(f"\033[1;35m{logo}\033[0m")  # Purple bold


def print_fun_header(section):
    headers = {
        "api": r"""
     ___      .__   __.   _______ 
    /   \     |  \ |  |  /  _____|
   /  ^  \    |   \|  | |  |  __  
  /  /_\  \   |  . `  | |  | |_ | 
 /  _____  \  |  |\   | |  |__| | 
/__/     \__\ |__| \__|  \______| 
    """,
        "due": r"""
 ____   ___  _   _ _____    ____  _   _ ___ _   _ 
|  _ \ / _ \| \ | | ____|  |  _ \| | | |_ _| \ | |
| | | | | | |  \| |  _|    | | | | | | || ||  \| |
| |_| | |_| | |\  | |___   | |_| | |_| || || |\  |
|____/ \___/|_| \_|_____|  |____/ \___/|___|_| \_|
    """,
        "ahead": r"""
  _____      _            _       _     _           
 |_   _|__  | | ___   ___| | __  | |__ (_)_ __  ___  
   | |/ _ \ | |/ _ \ / __| |/ /  | '_ \| | '_ \/ __| 
   | | (_) || | (_) | (__|   <   | | | | | | | \__ \ 
   |_|\___(_)_|\___/ \___|_|\_\  |_| |_|_|_| |_|___/ 
    """,
        "exit": r"""
  ________  ________  ___  ___  ________     
 |\   __  \|\   __  \|\  \|\  \|\   __  \    
 \ \  \|\  \ \  \|\  \ \  \\\  \ \  \|\  \   
  \ \   ____\ \   __  \ \  \\\  \ \   ____\  
   \ \  \___|\ \  \ \  \ \  \\\  \ \  \___|  
    \ \__\    \ \__\ \__\ \_______\ \__\     
     \|__|     \|__|\|__|\|_______|\|__|     
    """
    }
    print(f"\033[1;36m{headers.get(section, '')}\033[0m")


def get_time_left_message():
    now = datetime.now()
    end = now.replace(hour=23, minute=59, second=59, microsecond=0)
    delta = end - now
    hours, remainder = divmod(delta.seconds, 3600)
    minutes = remainder // 60
    return f"🕒 Only {hours}h {minutes}m left until midnight!"


def save_api_key(key: str):
    os.makedirs(CONFIG_FOLDER, exist_ok=True)
    with open(API_KEY_FILE, "w") as f:
        f.write(key.strip())


def main():
    while True:
        clear_screen()
        print_logo()

        choice = questionary.select(
            "🧠 What do you want to do?",
            choices=[
                "🔑 Add new API key",
                "📅 What is due today? (Oh, there’s still time… maybe)",
                "🚀 Let’s get ahead (Lol. Nobody uses this)",
                "❌ Exit (Procrastinate responsibly)"
            ]
        ).ask()

        if choice == "🔑 Add new API key":
            clear_screen()
            print_fun_header("api")
            api_key = questionary.text("🔐 Enter your Canvas API key:").ask()
            save_api_key(api_key)
            print("✅ API key saved successfully in ./config/api_key.txt!")
            input("\nPress Enter to return to menu.")

        elif choice == "📅 What is due today? (Oh, there’s still time… maybe)":
            clear_screen()
            print_fun_header("due")
            print(get_time_left_message())
            print("📌 Fetching assignments...\n")
            time.sleep(1)
            os.system("python Scripts/due_today.py")
            input("\nPress Enter to return to menu.")

        elif choice == "🚀 Let’s get ahead (Lol. Nobody uses this)":
            clear_screen()
            print_fun_header("ahead")
            print("📚 Let's pretend you'll work ahead... Sure, Jan.")
            print("Feature coming soon... if we ever get ahead.")
            input("\nPress Enter to return to menu.")

        elif choice == "❌ Exit (Procrastinate responsibly)":
            clear_screen()
            print_fun_header("exit")
            print("👋 Bye bye now. Don’t forget to *actually* do your homework.")
            break


if __name__ == "__main__":
    main()
