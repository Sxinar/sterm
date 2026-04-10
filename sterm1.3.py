#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------
# Proje: STerm - Terminal Ecosystem
# Ekip: Kapsül Serix Takımı
# Versiyon: 1.3 (GUI & OTA Removed - Performance Focused)
# ------------------------------------------------------------------

import os
import sys
import getpass
import socket
import subprocess

def get_distro():
    if os.path.exists("/usr/bin/pacman"): return "Arch"
    elif os.path.exists("/usr/bin/apt"): return "Debian/Ubuntu"
    return "Generic Linux"

def print_help():
    """Açılışta ve 'help' yazıldığında komutları listeler"""
    print("\n\033[1;35m--- STerm v1.3 KOMUT REHBERİ ---")
    print("\033[1;36m[Kapsül Kısayolları]")
    print("  yd [dizin]   : Yer Değiştir (cd)")
    print("  pd [dosya]   : Parça Depola (cp -r)")
    print("  my [dosya]   : Metin Yaz (nano)")
    print("  he [hedef]   : Hedefe Eriştir (mv)")
    print("\033[1;32m[Temel İşlevler]")
    print("  serix-get    : Akıllı Paket Yükleyici")
    print("  check        : Sistem Analizi")
    print("  speed        : Ağ Hız Testi")
    print("\033[1;33m[Sistem]")
    print("  help         : Bu rehberi gösterir")
    print("  exit         : Güvenli Çıkış")
    print("\033[1;35m--------------------------------\033[0m\n")

def main():
    user = getpass.getuser()
    hostname = socket.gethostname()
    distro = get_distro()
    
    os.system('clear')
    print("\033[1;36m" + "="*55)
    print("  ⚡ STerm v1.3 - KAPSÜL SERIX (PURE PERFORMANCE) ⚡")
    print(f"  CORE: {distro} | STATUS: Optimized | DEV: kefe3")
    print("  " + "="*55 + "\033[0m")
    
    # Açılışta komut rehberini göster
    print_help()

    while True:
        try:
            cwd = os.getcwd().replace(os.path.expanduser("~"), "~")
            prompt = f"\033[1;33m[SERIX]\033[0m \033[1;32m{user}@{hostname}\033[0m:\033[1;34m{cwd}\033[0m$ "
            
            user_input = input(prompt).strip()
            if not user_input: continue
            
            parts = user_input.split()
            cmd = parts[0]
            args = " ".join(parts[1:])

            # Kapsül Kısayolları
            if cmd == "yd":
                try: os.chdir(parts[1] if len(parts) > 1 else os.path.expanduser("~"))
                except: print("\033[1;31mDizin bulunamadı.\033[0m")
            elif cmd == "pd": os.system(f"cp -r {args}")
            elif cmd == "my": os.system(f"nano {args}")
            elif cmd == "he": os.system(f"mv {args}")
            
            # Ana Fonksiyonlar
            elif cmd == "serix-get":
                if distro == "Arch": os.system(f"sudo pacman -S {args}")
                else: os.system(f"sudo apt update && sudo apt install -y {args}")
            elif cmd == "check":
                os.system("neofetch" if os.path.exists("/usr/bin/neofetch") else "uname -a")
            elif cmd == "speed":
                os.system("speedtest-cli" if os.path.exists("/usr/bin/speedtest-cli") else "ping -c 4 google.com")
            
            # Yardım ve Çıkış
            elif cmd == "help": print_help()
            elif cmd == "exit": break
            
            # Tanınmayan komutları Linux'a pasla
            else:
                os.system(user_input)
        
        except KeyboardInterrupt:
            print("\n\033[1;31mÇıkış için 'exit' yazın.\033[0m")
        except EOFError:
            break

if __name__ == "__main__":
    main()
