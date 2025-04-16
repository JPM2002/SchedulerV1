import os
import time
import questionary
from datetime import datetime
from core.config import save_api_key, setup_calendar_folder, reset_config
from core.utils import clear_screen, print_logo, print_fun_header, get_time_left_message
from core.canvas_api import print_assignments_due_today


def main():
    while True:
        clear_screen()
        print_logo()

        choice = questionary.select(
            "🧠 What do you want to do?",
            choices=[
                "🔑 Add new API key",
                "📁 Setup calendar folder with .ics file",
                "📅 What is due today? (Oh, there’s still time… maybe)",
                "🚀 Let’s get ahead (Lol. Nobody uses this)",
                "🔄 Reset configuration (Danger zone!)",
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

        elif choice == "📁 Setup calendar folder with .ics file":
            setup_calendar_folder()

        elif choice == "📅 What is due today? (Oh, there’s still time… maybe)":
            clear_screen()
            print_fun_header("due")
            print(get_time_left_message())
            print("📌 Fetching assignments...\n")
            time.sleep(1)
            print_assignments_due_today()
            input("\nPress Enter to return to menu.")

        elif choice == "🚀 Let’s get ahead (Lol. Nobody uses this)":
            clear_screen()
            print_fun_header("ahead")
            print("📚 Let's pretend you'll work ahead... Sure, Jan.")
            print("Feature coming soon... if we ever get ahead.")
            input("\nPress Enter to return to menu.")

        elif choice == "🔄 Reset configuration (Danger zone!)":
            reset_config()

        elif choice == "❌ Exit (Procrastinate responsibly)":
            clear_screen()
            print_fun_header("exit")
            print("👋 Bye bye now. Don’t forget to *actually* do your homework.")
            break


if __name__ == "__main__":
    main()