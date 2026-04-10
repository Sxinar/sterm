#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------
# Proje: STerm - Terminal Ecosystem
# Ekip: Kapsül Serix Takımı
# Versiyon: 1.2 (GUI, Otomatik Rehber ve Tüm Fonksiyonlar)
# ------------------------------------------------------------------

import os
import sys
import getpass
import socket
import subprocess
import tkinter as tk
from tkinter import messagebox

def get_distro():
    if os.path.exists("/usr/bin/pacman"): return "Arch"
    elif os.path.exists("/usr/bin/apt"): return "Debian/Ubuntu"
    return "Generic Linux"

def show_gui():
    """v1.0'dan geri gelen GUI Arayüzü"""
    root = tk.Tk()
    root.title("STerm v1.2 - Kapsül Denetim Masası")
    root.geometry("400x300")
    root.configure(bg="#1e1e1e")

    label = tk.Label(root, text="KAPSÜL SERIX TERM", fg="#00ccff", bg="#1e1e1e", font=("Arial", 14, "bold"))
    label.pack(pady=20)

    def run_cmd(c):
        messagebox.showinfo("Komut Çalıştırıldı", f"Komut: {c}\nTerminalden devam edin.")
        root.destroy()

    tk.Button(root, text="Sistem Analizi (Check)", command=lambda: run_cmd("check"), width=25).pack(pady=5)
    tk.Button(root, text="Hız Testi (Speed)", command=lambda: run_cmd("speed"), width=25).pack(pady=5)
    tk.Button(root, text="Güncelleme Denetle", command=lambda: run_cmd("sterm-update"), width=25).pack(pady=5)
    tk.Button(root, text="Kapat", command=root.destroy, width=25, bg="#ff4444").pack(pady=20)
    
    root.mainloop()

def print_help():
    """Açılışta ve istendiğinde görünen komut rehberi"""
    print("\n\033[1;35m--- STerm v1.2 KOMUT REHBERİ ---")
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
    print("  gui          : Kontrol Panelini Açar")
    print("  sterm-update : OTA Güncelleme Yapar")
    print("  exit         : Güvenli Çıkış")
    print("\033[1;35m--------------------------------\033[0m\n")

def self_update():
    if not os.path.exists(".git"):
        print("\033[1;31m[HATA] .git klasörü yok!\033[0m")
        return
    print("\033[1;33m[OTA] Güncelleniyor...\033[0m")
    subprocess.run(["git", "pull", "origin", "main"])
    os.execv(sys.executable, ['python3'] + sys.argv)

def main():
    user = getpass.getuser()
    hostname = socket.gethostname()
    distro = get_distro()
    
    os.system('clear')
    print("\033[1;36m" + "="*55)
    print("  ⚡ STerm v1.2 - KAPSÜL SERIX (FULL LEGACY + GUI) ⚡")
    print(f"  CORE: {distro} | STATUS: Active | DEV: kefe3")
    print("  " + "="*55 + "\033[0m")
    
    # AÇILIŞTA KOMUTLARI GÖSTER
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

            if cmd == "yd":
                try: os.chdir(parts[1] if len(parts) > 1 else os.path.expanduser("~"))
                except: print("Dizin bulunamadı.")
            elif cmd == "pd": os.system(f"cp -r {args}")
            elif cmd == "my": os.system(f"nano {args}")
            elif cmd == "he": os.system(f"mv {args}")
            elif cmd == "serix-get":
                if distro == "Arch": os.system(f"sudo pacman -S {args}")
                else: os.system(f"sudo apt update && sudo apt install -y {args}")
            elif cmd == "check": os.system("neofetch" if os.path.exists("/usr/bin/neofetch") else "uname -a")
            elif cmd == "speed": os.system("speedtest-cli" if os.path.exists("/usr/bin/speedtest-cli") else "ping -c 4 google.com")
            elif cmd == "gui": show_gui()
            elif cmd == "help": print_help()
            elif cmd == "sterm-update": self_update()
            elif cmd == "exit": break
            else: os.system(user_input)
        
        except KeyboardInterrupt: print("\nÇıkış için 'exit' yazın.")
        except EOFError: break

if __name__ == "__main__":
    main()
