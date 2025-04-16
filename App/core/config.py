import os
import shutil
import questionary

CONFIG_FOLDER = "config"
API_KEY_FILE = os.path.join(CONFIG_FOLDER, "api_key.txt")
CALENDAR_FOLDER = os.path.join("ICS", "calendar")


def save_api_key(key: str):
    os.makedirs(CONFIG_FOLDER, exist_ok=True)
    with open(API_KEY_FILE, "w") as f:
        f.write(key.strip())


def load_api_key():
    if not os.path.exists(API_KEY_FILE):
        return None
    try:
        with open(API_KEY_FILE, "r") as f:
            return f.read().strip()
    except Exception as e:
        print(f"⚠️ Could not read API key: {e}")
        return None


def setup_calendar_folder():
    from core.utils import clear_screen, print_fun_header

    clear_screen()
    print_fun_header("calendar")
    os.makedirs(CALENDAR_FOLDER, exist_ok=True)
    file_path = questionary.text("📂 Enter full path to your .ics calendar file:").ask()

    if not os.path.isfile(file_path):
        print("❌ That file doesn't exist.")
    elif not file_path.lower().endswith(".ics"):
        print("❌ That doesn't look like a .ics file.")
    else:
        try:
            shutil.copy(file_path, CALENDAR_FOLDER)
            print(f"✅ File copied to {CALENDAR_FOLDER} successfully!")
        except Exception as e:
            print(f"⚠️ Something went wrong: {e}")

    input("\nPress Enter to return to menu.")


def reset_config():
    from core.utils import clear_screen, print_fun_header

    clear_screen()
    print_fun_header("exit")
    print("⚠️ This will delete your saved API key and calendar file.")
    confirm = questionary.text("Type 'RESTART' to confirm reset:").ask()

    if confirm != "RESTART":
        print("❌ Cancelled. No changes made.")
    else:
        try:
            if os.path.exists(API_KEY_FILE):
                os.remove(API_KEY_FILE)
                print("🗑️ API key removed.")
            if os.path.exists(CALENDAR_FOLDER):
                shutil.rmtree(CALENDAR_FOLDER)
                print("🗑️ Calendar folder removed.")
        except Exception as e:
            print(f"⚠️ Something went wrong: {e}")
        else:
            print("✅ Reset complete.")
    input("\nPress Enter to return to menu.")
