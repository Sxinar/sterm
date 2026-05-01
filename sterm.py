#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------
# [STerm] - Terminal Ecosystem v3.0
# Optimized for: Fedora / Linux / Universal
# ------------------------------------------------------------------

import os, sys, getpass, socket, shutil, platform, datetime
import webbrowser, subprocess, string, random, json, time

# --- OK TUŞLARI VE GEÇMİŞ DESTEĞİ ---
try:
    import readline
    HISTORY_PATH = os.path.expanduser("~/.sterm_history")
    if os.path.exists(HISTORY_PATH):
        try: readline.read_history_file(HISTORY_PATH)
        except: pass
    readline.set_history_length(1000)
    readline.parse_and_bind("tab: complete")
except ImportError: pass

class Style:
    # Cyberpunk Renk Paleti
    CYAN = '\033[38;5;51m'
    BLUE = '\033[38;5;39m'
    PURPLE = '\033[38;5;141m'
    GOLD = '\033[38;5;220m'
    RED = '\033[38;5;196m'
    GREEN = '\033[38;5;82m'
    GRAY = '\033[38;5;240m'
    WHITE = '\033[38;5;255m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    CLEAR = '\033[2J\033[H'

NOTLAR_FILE = "sterm_notlar.txt"

def banner_goster():
    print(Style.CLEAR, end="")
    # Büyük STerm Logosu
    print(f"""
    {Style.CYAN}{Style.BOLD}     ██████╗████████╗███████╗██████╗ ███╗   ███╗
    {Style.CYAN}    ██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
    {Style.BLUE}    ╚█████╗    ██║   █████╗  ██████╔╝██╔████╔██║
    {Style.BLUE}     ╚═══██╗   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║
    {Style.PURPLE}    ██████╔╝   ██║   ███████╗██║  ██║██║ ╚═╝ ██║
    {Style.PURPLE}    ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ {Style.WHITE}v3.0{Style.RESET}""")

    # Alt Bilgi Satırı
    info = f"{Style.GRAY}Host: {Style.WHITE}{socket.gethostname()} {Style.GRAY}| User: {Style.WHITE}{getpass.getuser()} {Style.GRAY}| OS: {Style.WHITE}{platform.system()}"
    print(f"\n{info.center(75)}")
    print(f"{Style.GRAY}─" * 70)
    print(f" {Style.GREEN}»{Style.RESET} Sistem hazır. Komut listesi için {Style.GOLD}'yardim'{Style.RESET} yazın.")
    print(f" {Style.GREEN}»{Style.RESET} Geçmişte gezmek için {Style.GOLD}Üst/Alt Ok{Style.RESET} tuşlarını kullanın.{Style.RESET}\n")

def yardim_listele():
    print(f"\n{Style.PURPLE}╔═════════════════════════ KOMUT REHBERİ ═════════════════════════╗{Style.RESET}")

    rehber = [
        ("analiz", "Sistem donanımı ve yazılım detaylarını raporlar."),
        ("saat", "Saniyelik hassasiyetle güncel zamanı gösterir."),
        ("temizle", "Ekranı temizler ve STerm arayüzünü yeniler."),
        ("gezgin", "Bulunduğunuz dizindeki dosya ve klasörleri listeler."),
        ("yd [yol]", "Dizinler arası geçiş yapar (Örn: yd /home)."),
        ("oku [dosya]", "Metin tabanlı dosyaların içeriğini ekrana basar."),
        ("boyut [dosya]", "Dosyanın diskte kapladığı alanı (KB/MB) hesaplar."),
        ("hava [şehir]", "Belirtilen şehrin anlık hava durumunu çeker."),
        ("hesapla [işlem]", "Matematiksel işlemleri anında çözer (Örn: 25*4)."),
        ("parola", "14 karakterli, sembol içeren güvenli şifre üretir."),
        ("ip_bul", "Yerel ağ (Local IP) adresinizi görüntüler."),
        ("not-al [not]", "Hızlıca not alır ve veritabanına kaydeder."),
        ("notlari-gor", "Kaydettiğiniz tüm notları kronolojik listeler."),
        ("not-duzenle", "Not dosyasını sistemin varsayılan editörüyle açar."),
        ("web [url]", "Belirtilen adresi varsayılan tarayıcıda açar."),
        ("çıkış", "STerm oturumunu güvenli bir şekilde sonlandırır.")
    ]

    for cmd, desc in rehber:
        print(f"{Style.PURPLE}║ {Style.CYAN}{cmd:<15} {Style.GRAY}→ {Style.WHITE}{desc:<47} {Style.PURPLE}║{Style.RESET}")

    print(f"{Style.PURPLE}╚══════════════════════════════════════════════════════════════════╝{Style.RESET}\n")

def main():
    banner_goster()
    while True:
        try:
            user = getpass.getuser()
            cwd = os.getcwd().replace(os.path.expanduser("~"), "~")

            # Ultra Modern Prompt
            prompt = f"{Style.PURPLE}┌──<{Style.CYAN}{user}@{socket.gethostname()}{Style.PURPLE}>─[{Style.GOLD}{cwd}{Style.PURPLE}]\n{Style.PURPLE}└─{Style.BLUE}❯{Style.RESET} "

            giris = input(prompt).strip()
            if not giris: continue

            if 'readline' in sys.modules:
                try: readline.write_history_file(HISTORY_PATH)
                except: pass

            p = giris.split()
            cmd = p[0].lower()
            args = " ".join(p[1:])

            # --- KOMUT MOTORU ---
            if cmd == "yardim":
                yardim_listele()

            elif cmd == "analiz":
                print(f" {Style.BLUE}● OS: {Style.WHITE}{platform.system()} {platform.release()}")
                print(f" {Style.BLUE}● İşlemci: {Style.WHITE}{platform.processor()}")
                print(f" {Style.BLUE}● Çekirdek: {Style.WHITE}{platform.machine()}")

            elif cmd == "saat":
                print(f" {Style.GOLD}⌚ Zaman: {datetime.datetime.now().strftime('%H:%M:%S')}{Style.RESET}")

            elif cmd == "temizle":
                banner_goster()

            elif cmd == "gezgin":
                print(f"{Style.GRAY}─ Dosya Listesi ───────────────{Style.RESET}")
                for item in sorted(os.listdir('.')):
                    color = Style.CYAN if os.path.isdir(item) else Style.WHITE
                    mark = "📁" if os.path.isdir(item) else "📄"
                    print(f" {mark} {color}{item}{Style.RESET}")

            elif cmd == "yd":
                try: os.chdir(args if args else os.path.expanduser("~"))
                except: print(f" {Style.RED}✘ Hata: Yol bulunamadı.{Style.RESET}")

            elif cmd == "oku":
                if not args: print(f" {Style.RED}✘ Hata: Dosya ismi belirtmediniz.{Style.RESET}")
                else:
                    try:
                        with open(args, 'r', encoding='utf-8') as f:
                            print(f"\n{Style.GRAY}--- {args} ---\n{Style.WHITE}{f.read()}\n{Style.GRAY}--- SON ---{Style.RESET}\n")
                    except: print(f" {Style.RED}✘ Hata: Dosya okunamadı.{Style.RESET}")

            elif cmd == "boyut":
                if os.path.exists(args):
                    s = os.path.getsize(args)
                    print(f" {Style.BLUE}⚖ Boyut: {round(s/1024, 2)} KB ({s} byte){Style.RESET}")
                else: print(f" {Style.RED}✘ Hata: Nesne bulunamadı.{Style.RESET}")

            elif cmd == "hava":
                os.system(f"curl -s wttr.in/{args if args else 'Istanbul'}?lang=tr")

            elif cmd == "hesapla":
                try: print(f" {Style.GREEN}Σ Sonuç: {eval(args)}{Style.RESET}")
                except: print(f" {Style.RED}✘ Hata: Geçersiz işlem.{Style.RESET}")

            elif cmd == "parola":
                chars = string.ascii_letters + string.digits + "!@#$%^&*"
                p_gen = ''.join(random.choice(chars) for _ in range(14))
                print(f" {Style.GOLD}🔑 Üretilen Parola: {Style.WHITE}{p_gen}{Style.RESET}")

            elif cmd == "ip_bul":
                print(f" {Style.CYAN}🌐 Yerel IP: {socket.gethostbyname(socket.gethostname())}{Style.RESET}")

            elif cmd == "web":
                print(f" {Style.CYAN}🌐 Tarayıcı açılıyor: {args}{Style.RESET}")
                webbrowser.open(args if args.startswith("http") else "https://" + args)

            elif cmd == "not-al":
                with open(NOTLAR_FILE, 'a', encoding='utf-8') as f:
                    f.write(f"[{datetime.datetime.now().strftime('%d/%m %H:%M')}] {args}\n")
                print(f" {Style.GREEN}✔ Not başarıyla kaydedildi.{Style.RESET}")

            elif cmd == "not-duzenle":
                editor = os.environ.get('EDITOR', 'nano' if os.name != 'nt' else 'notepad')
                subprocess.call([editor, NOTLAR_FILE])

            elif cmd in ["notlari-gor", "notları-gör"]:
                if os.path.exists(NOTLAR_FILE):
                    print(f"\n{Style.PURPLE}--- KAYITLI NOTLAR ---{Style.RESET}")
                    with open(NOTLAR_FILE, 'r', encoding='utf-8') as f:
                        print(f"{Style.WHITE}{f.read()}")
                else: print(f" {Style.RED}✘ Veri bulunamadı.{Style.RESET}")

            elif cmd in ["exit", "çıkış", "quit"]:
                print(f"\n {Style.RED}STerm kapatılıyor...{Style.RESET}"); break

            else:
                # Eğer STerm komutu değilse Bash'e gönder
                os.system(giris)

        except (KeyboardInterrupt, EOFError):
            print(f"\n {Style.RED}Bağlantı kesildi.{Style.RESET}"); break
        except Exception as e:
            print(f" {Style.RED}!! Hata: {e}{Style.RESET}")

if __name__ == "__main__":
    main()
