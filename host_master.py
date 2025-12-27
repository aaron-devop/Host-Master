#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import ssl
import socket
import datetime

# --- CONFIG ---
WEB_ROOT = "/var/www/html"  # Alapértelmezett webgyökér
LOG_FILE = "hosting_fix.log"

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def log_action(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def run_cmd(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        return None

def check_service(name):
    status = run_cmd(f"systemctl is-active {name}")
    if status == "active":
        print(f"[{Colors.GREEN}OK{Colors.ENDC}] {name} fut.")
    else:
        print(f"[{Colors.FAIL}HIBA{Colors.ENDC}] {name} LEÁLLT! Újraindítás...")
        run_cmd(f"systemctl restart {name}")
        log_action(f"Service {name} restarted.")

def check_disk_space():
    print(f"\n{Colors.BOLD}--- LEMEZ TERÜLET (Disk Space) ---{Colors.ENDC}")
    total, used, free = shutil.disk_usage("/")
    percent = (used / total) * 100
    print(f"Gyökér (/) foglaltság: {percent:.2f}%")
    if percent > 90:
        print(f"{Colors.FAIL}[!] KRITIKUS: A lemez majdnem tele van!{Colors.ENDC}")
    else:
        print(f"{Colors.GREEN}[OK] Van elég hely.{Colors.ENDC}")

def check_mail_queue():
    print(f"\n{Colors.BOLD}--- LEVELEZÉS (Mail Queue) ---{Colors.ENDC}")
    # Postfix ellenőrzés
    queue_count = run_cmd("mailq | grep -v 'Mail queue is empty' | wc -l")
    if not queue_count: queue_count = "0"
    
    print(f"Várakozó levelek száma: {Colors.BLUE}{queue_count}{Colors.ENDC}")
    if int(queue_count) > 50:
        print(f"{Colors.WARNING}[!] FIGYELEM: Magas levélszám! Spam gyanús.{Colors.ENDC}")

def fix_permissions():
    print(f"\n{Colors.WARNING}--- JOGOSULTSÁGOK JAVÍTÁSA (Permissions) ---{Colors.ENDC}")
    print(f"Célkönyvtár: {WEB_ROOT}")
    confirm = input("Biztosan futtatod? (y/n): ")
    if confirm.lower() == 'y':
        print("Fájlok beállítása 644-re...")
        os.system(f"find {WEB_ROOT} -type f -exec chmod 644 {{}} \;")
        print("Mappák beállítása 755-re...")
        os.system(f"find {WEB_ROOT} -type d -exec chmod 755 {{}} \;")
        print(f"{Colors.GREEN}[KÉSZ] Jogosultságok alaphelyzetbe állítva.{Colors.ENDC}")
        log_action("Permissions fixed in webroot.")
    else:
        print("Megszakítva.")

def check_ssl_cert():
    print(f"\n{Colors.BOLD}--- SSL TANÚSÍTVÁNY ELLENŐRZÉS ---{Colors.ENDC}")
    domain = input("Add meg a domaint (pl. atw.hu): ")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expire_date = cert['notAfter']
                print(f"Domain: {domain}")
                print(f"Lejárat: {Colors.GREEN}{expire_date}{Colors.ENDC}")
    except:
        print(f"{Colors.FAIL}[HIBA] Nem sikerült kapcsolódni vagy nincs SSL.{Colors.ENDC}")

def main_menu():
    os.system('clear')
    print(f"{Colors.BLUE}{Colors.BOLD}")
    print(r"""
  _    _  ____   _____ _______      __  __           _____ _______ ______ _____  
 | |  | |/ __ \ / ____|__   __|    |  \/  |   /\    / ____|__   __|  ____|  __ \ 
 | |__| | |  | | (___    | | ______| \  / |  /  \  | (___    | |  | |__  | |__) |
 |  __  | |  | |\___ \   | ||______| |\/| | / /\ \  \___ \   | |  |  __| |  _  / 
 | |  | | |__| |____) |  | |       | |  | |/ ____ \ ____) |  | |  | |____| | \ \ 
 |_|  |_|\____/|_____/   |_|       |_|  |_/_/    \_\_____/   |_|  |______|_|  \_\
                                                    v1.0 | Hosting Helper @ aaron-devop
    """)
    print(f"{Colors.ENDC}")
    
    while True:
        print(f"\n{Colors.BOLD}Válassz feladatot:{Colors.ENDC}")
        print("1. Szolgáltatások ellenőrzése (Apache/Nginx/MySQL)")
        print("2. Webes Jogosultságok Javítása (Fix Permissions)")
        print("3. Levelezés Diagnosztika (Mail Queue)")
        print("4. SSL Tanúsítvány Ellenőrzés")
        print("5. Lemezterület Ellenőrzés")
        print("9. Kilépés")
        
        choice = input(f"\n{Colors.BLUE}HostMaster > {Colors.ENDC}")
        
        if choice == '1':
            check_service("nginx")
            check_service("apache2")
            check_service("mysql")
            check_service("php*-fpm")
        elif choice == '2':
            fix_permissions()
        elif choice == '3':
            check_mail_queue()
        elif choice == '4':
            check_ssl_cert()
        elif choice == '5':
            check_disk_space()
        elif choice == '9':
            sys.exit()

if __name__ == "__main__":
    if os.geteuid() != 0:
        print(f"{Colors.FAIL}Ezt a scriptet ROOT-ként (sudo) kell futtatni!{Colors.ENDC}")
        sys.exit()
    main_menu()
      
