#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------
# Proje: STerm - Terminal Ecosystem (Titan-Pro)
# Ekip: Kapsül Serix Takımı
# Versiyon: 1.3 (Sistem Güç Komutları & Root Erişimi)
# ------------------------------------------------------------------

import os
import sys
import getpass
import socket
import shutil
import platform
import datetime

def show_banner():
    os.system('clear')
    print("\033[1;36m" + "█"*60)
    print("  ⚡ STerm v1.3 TITAN-PRO - KAPSÜL SERIX ECOSYSTEM ⚡")
    print(f"  SYSTEM: {platform.system()} | ROOT ACCESS: Enabled | DEV: kefe3")
    print("  " + "█"*60 + "\033[0m")

def print_help():
    print("\n\033[1;35m--- ⚙️ SİSTEM YÖNETİM KOMUTLARI ---")
    print("\033[1;31m[GÜÇ SEÇENEKLERİ]")
    print("  kapat         : Bilgisayarı tamamen kapatır")
    print("  yeniden       : Bilgisayarı yeniden başlatır")
    print("  oturumu-kapat : Mevcut kullanıcı oturumunu sonlandırır")
    print("  kilitle       : Ekranı kilitler (Güvenlik modu)")
    print("\033[1;32m[YETKİ VE ERİŞİM]")
    print("  serix-kök     : Kök kullanıcı (Root) yetkisi al (sudo su)")
    print("\033[1;36m[DİĞER]")
    print("  gezgin, analiz, günlük, temizle")
    print("\033[1;35m------------------------------------\033[0m\n")

def main():
    show_banner()
    print_help()

    while True:
        try:
            cwd = os.getcwd().replace(os.path.expanduser("~"), "~")
            # Root kontrolü (Eğer root ise prompt değişir)
            if os.geteuid() == 0:
                prompt = f"\033[1;31m[KÖK-SERIX]\033[0m \033[1;32m{getpass.getuser()}\033[0m:\033[1;34m{cwd}\033[0m# "
            else:
                prompt = f"\033[1;33m[SERIX-TITAN]\033[0m \033[1;32m{getpass.getuser()}\033[0m:\033[1;34m{cwd}\033[0m$ "
            
            user_input = input(prompt).strip()
            if not user_input: continue
            
            parts = user_input.split()
            cmd = parts[0]
            args = " ".join(parts[1:])

            # --- GÜÇ KOMUTLARI ---
            if cmd == "kapat":
                os.system("sudo shutdown -h now")
            elif cmd == "yeniden":
                os.system("sudo reboot")
            elif cmd == "oturumu-kapat":
                # Dağıtıma göre logout komutu değişebilir (GNOME için)
                os.system("gnome-session-quit --logout --no-prompt")
            elif cmd == "kilitle":
                # Ekran kilitleme (Linux genel)
                os.system("xdg-screensaver lock")
            
            # --- YETKİ KOMUTLARI ---
            elif cmd == "serix-kök":
                print("\033[1;31m[UYARI] Kök erişimi başlatılıyor. Dikkatli olun!\033[0m")
                os.system("sudo -s")
            
            # --- ÖNCEKİ SÜRÜM ÖZELLİKLERİ ---
            elif cmd == "yd":
                try: os.chdir(parts[1] if len(parts) > 1 else os.path.expanduser("~"))
                except: print("Dizin bulunamadı.")
            elif cmd == "pd": os.system(f"cp -r {args}")
            elif cmd == "my": os.system(f"nano {args}")
            elif cmd == "he": os.system(f"mv {args}")
            elif cmd == "gezgin":
                items = os.listdir('.')
                for i in items: print(f"-> {i}")
            elif cmd == "analiz":
                print(f"Sistem: {platform.uname().system}")
            elif cmd == "temizle":
                show_banner()
            elif cmd == "exit":
                break
            else:
                os.system(user_input)
        
        except KeyboardInterrupt:
            print("\nÇıkış için 'exit' yazın.")
        except Exception as e:
            print(f"Hata: {e}")

if __name__ == "__main__":
    main()
