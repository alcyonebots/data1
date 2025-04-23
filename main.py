import asyncio
import os
from telethon import TelegramClient, events
from colorama import init, Fore

init(autoreset=True)

# == Your API credentials ==
API_ID = int(input(Fore.CYAN + "Enter your API ID: "))
API_HASH = input(Fore.CYAN + "Enter your API HASH: ")
SESSION_NAME = "users_session"

# == Channel where to send saved users ==
CHANNEL_ID = -1002454508589  # <-- Yaha apne PRIVATE CHANNEL ka ID daalna (with -100)

# == Allowed groups to monitor ==
ALLOWED_GROUP_LINKS = [
    "https://t.me/+kLjsw-WqpuFkZjM1",
    "https://t.me/BUZZ_IGCC_CHATS",
    "https://t.me/+F9Pp5_gHDB9jYzQ1",
    "https://t.me/BuzzEscrowe",
    "https://t.me/+mcMK_XK6J4M1NDE1",
    "https://t.me/+3khxeH9j6pViMjU9",
]

# == Save users file ==
SAVED_USERS_FILE = "saved_users1.txt"
if not os.path.exists(SAVED_USERS_FILE):
    open(SAVED_USERS_FILE, "w").close()

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

group_ids = []  # yeh list banayenge group IDs store karne ke liye

async def login():
    print(Fore.YELLOW + "Logging into your Telegram account...")
    await client.connect()
    if not await client.is_user_authorized():
        phone = input(Fore.CYAN + "Enter your phone number (with country code): ")
        await client.send_code_request(phone)
        code = input(Fore.CYAN + "Enter the OTP sent to your Telegram: ")
        try:
            await client.sign_in(phone, code)
        except Exception as e:
            print(Fore.RED + f"Login failed: {e}")
            exit()

async def get_group_ids():
    global group_ids
    for link in ALLOWED_GROUP_LINKS:
        try:
            entity = await client.get_entity(link)
            group_ids.append(entity.id)
            print(Fore.GREEN + f"✅ Joined group: {link}")
        except Exception as e:
            print(Fore.RED + f"⚠️ Failed to fetch group {link}: {e}")

@client.on(events.NewMessage)
async def handler(event):
    if not event.is_group:
        return

    if event.chat_id not in group_ids:
        return

    sender = await event.get_sender()

    if sender.bot or sender.deleted or sender.is_self:
        return

    try:
        user_id = str(sender.id)

        with open(SAVED_USERS_FILE, "r") as f:
            saved_ids = f.read().splitlines()

        if user_id in saved_ids:
            return  # Already saved

        name = (sender.first_name or "") + " " + (sender.last_name or "")
        username = f"@{sender.username}" if sender.username else "No Username"

        text = f"👤 Name: {name}\n🔗 Username: {username}\n🆔 ID: {user_id}"

        # Save locally
        with open(SAVED_USERS_FILE, "a") as f:
            f.write(user_id + "\n")

        # Send to private channel
        await client.send_message(CHANNEL_ID, text)

        print(Fore.GREEN + f"✅ Saved & Sent: {user_id} ({name})")

    except Exception as e:
        print(Fore.RED + f"⚠️ Error: {e}")

async def main():
    await login()
    await get_group_ids()
    print(Fore.GREEN + "✅ Logged in successfully!")
    print(Fore.YELLOW + "✅ Bot is running. Collecting user data...")

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
