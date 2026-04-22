#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------
# Proje: STerm - Terminal Ekosistemi (Evrensel & Gelişmiş)
# Ekip: Kapsül Serix Takımı
# Versiyon: 2.0 (ULTRA ADVANCED - ALL-IN-ONE)
# Geliştirici: Kemal & Kefe3
# Yayın Tarihi: Nisan 2026
# ------------------------------------------------------------------

import os
import sys
import getpass
import socket
import shutil
import platform
import datetime
import webbrowser
import subprocess
import string
import random
import json
import time

# --- BAĞIMLILIKLARI KONTROL ET ---
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# --- YAPILANDIRMA VE SABITLER ---
SURUM = "2.0"
SURUM_ADI = "ULTRA ADVANCED - ALL-IN-ONE"
GUNCELLEME_URL = "https://raw.githubusercontent.com/kefe3/sterm/refs/heads/main/sterm_guncelleme.py"
CONFIG_FILE = "sterm_config.json"
HISTORY_FILE = "sterm_history.txt"
NOTLAR_FILE = "sterm_notlar.txt"

# --- RENKLER VE STİLLER ---
class Renkler:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# --- KONFIGÜRASYON YÖNETIMI ---
def yukle_config():
    """Konfigürasyonu dosyadan yükle."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return varsayilan_config()
    return varsayilan_config()

def varsayilan_config():
    """Varsayılan konfigürasyon döndür."""
    return {
        "tema": "dark",
        "dil": "tr",
        "hava_sehri": "Konya",
        "otomatik_guncelle": False,
        "sesin_aç": True,
        "tarih_formatı": "%d/%m/%Y %H:%M:%S"
    }

def kaydet_config(config):
    """Konfigürasyonu dosyaya kaydet."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

# --- DOSYA VE TARİH YÖNETİMİ ---
def tarih_saat():
    """Şu anki tarih ve saati döndür."""
    config = yukle_config()
    return datetime.datetime.now().strftime(config["tarih_formatı"])

def gecmis_ekle(komut):
    """Komutu geçmişe ekle."""
    with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{tarih_saat()}] {komut}\n")

def gecmis_goster(satir_sayisi=50):
    """Geçmiş komutları göster."""
    if not os.path.exists(HISTORY_FILE):
        print("❌ Henüz geçmiş kaydı yok.")
        return
    
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        satirlar = f.readlines()
    
    print(f"\n📜 Son {min(satir_sayisi, len(satirlar))} komut:")
    for satir in satirlar[-satir_sayisi:]:
        print(satir.rstrip())

# --- SİSTEM KONTROL FONKSİYONLARI ---
def ekrani_temizle():
    """Ekranı temizle."""
    os.system('cls' if os.name == 'nt' else 'clear')

def banner_goster():
    """Başlık bannerını göster."""
    ekrani_temizle()
    sistem = platform.system().upper()
    
    # Sistem tespiti
    if sistem == "WINDOWS":
        sistem_kisaltma = "WIN"
        emoji = "🪟"
    elif sistem == "DARWIN":
        sistem_kisaltma = "MAC"
        emoji = "🍎"
    else:
        sistem_kisaltma = "LNX"
        emoji = "🐧"
    
    print("\033[1;36m" + "█"*80)
    print(f"  ⚡ STerm v{SURUM} {SURUM_ADI} ⚡")
    print(f"  {emoji} SİSTEM: {sistem_kisaltma} | CİHAZ: {socket.gethostname()} | GELİŞTİRİCİ: KEMAL & KEFE3")
    print("  " + "█"*80 + "\033[0m\n")

def yardim_goster():
    """Kapsamlı yardım menüsünü göster."""
    print("\n" + "█"*85)
    print("  " + Renkler.BOLD + "🎯 SERIX v2.0 - KOMUT MERKEZİ" + Renkler.ENDC)
    print("█"*85)
    
    # SİSTEM KOMUTLARI
    print("\n" + Renkler.OKBLUE + Renkler.BOLD + "[1] SİSTEM & GÜNCELLEME" + Renkler.ENDC)
    print("  guncelle           : Yazılımı İnternetten Güncelle")
    print("  surum              : Versiyon Detaylarını Göster")
    print("  analiz             : Derin Sistem Raporu")
    print("  bilgisayar         : Bilgisayar Bilgilerini Göster")
    print("  saat               : Güncel Tarih ve Saati Göster")
    print("  temizle            : Ekranı ve Logoyu Tazele")
    
    # DOSYA VE DİZİN YÖNETİMİ
    print("\n" + Renkler.OKGREEN + Renkler.BOLD + "[2] DOSYA & DİZİN YÖNETİMİ" + Renkler.ENDC)
    print("  yd [dizin]         : Dizin Değiştir (cd)")
    print("  yarat [isim]       : Yeni Klasör Oluştur")
    print("  sil [isim]         : Dosya/Klasör Sil")
    print("  gezgin             : Dosyaları Renkli Listele")
    print("  ara [isim]         : Dosya/Klasör Ara")
    print("  boyut [isim]       : Dosya Boyutunu Göster (KB)")
    print("  oku [dosya]        : Dosya İçeriğini Oku")
    print("  kopyala [kaynak]   : Dosya Kopyala (cp -r)")
    print("  tası [hedef]       : Dosya Taşı (mv)")
    
    # AKILLI ARAÇLAR
    print("\n" + Renkler.WARNING + Renkler.BOLD + "[3] AKILLI ARAÇLAR" + Renkler.ENDC)
    print("  hava [sehir]       : Hava Durumunu Göster")
    print("  hesapla [işlem]    : Matematiksel İşlem Çöz (ör: 2+2*5)")
    print("  parola-uret [n]    : n uzunluğunda Güvenli Şifre (def: 12)")
    print("  indir [url] [ad]   : İnternetten Dosya İndir")
    print("  web [url]          : Tarayıcıda Site Aç")
    print("  ip_bul             : Yerel IP Adresi")
    print("  ping [host]        : Bağlantı Test Et")
    print("  disk               : Disk Kullanımı Göster")
    print("  not-al [metin]     : Hızlı Not Kaydet")
    print("  notları-gör        : Kaydedilen Notları Gör")
    
    # PAKETİ VE YÖNETİM
    print("\n" + Renkler.FAIL + Renkler.BOLD + "[4] PAKET & YÖNETİM" + Renkler.ENDC)
    print("  serix-get [paket]  : Paket Yükleyici (Apt/Pacman/Brew/Winget)")
    print("  serix-kök          : Yönetici/Root Erişimi")
    print("  kapat              : Bilgisayarı Kapat")
    print("  yeniden            : Yeniden Başlat")
    print("  kilitle            : Ekranı Kilitle")
    
    # GEÇMİŞ VE AYARLAR
    print("\n" + Renkler.OKGREEN + Renkler.BOLD + "[5] GEÇMİŞ & AYARLAR" + Renkler.ENDC)
    print("  gecmis [n]         : Son n komutun Geçmişi Göster")
    print("  ayar [anahtar]     : Ayarları Yönet")
    print("  config             : Konfigürasyonu Göster")
    
    # ÇIKIŞş
    print("\n" + Renkler.BOLD + "[6] ÇIKIŞ" + Renkler.ENDC)
    print("  yardim / yardım    : Bu Menüyü Tekrar Göster")
    print("  çıkış              : STerm'den Ayrıl\n")
    
    print("█"*85 + "\n")

# --- GÜNCELLEME FONKSİYONU ---
def guncelleme_denetle():
    """GitHub'dan güncellemeyi kontrol et ve uygula."""
    if not HAS_REQUESTS:
        print("⚠️  Güncelleme için 'requests' kütüphanesi gereklidir.")
        print("   Kurulum: pip install requests")
        return
    
    print("🔄 Serix Bulut Sunucularına Bağlanılıyor...")
    try:
        # Cache sorununu önlemek için timestamp ekle
        taze_url = f"{GUNCELLEME_URL}?t={int(time.time())}"
        yanit = requests.get(taze_url, timeout=10)
        
        if yanit.status_code == 200:
            yeni_kod = yanit.text
            
            # Sürüm kontrol
            if f'SURUM = "{SURUM}"' in yeni_kod:
                print(f"✅ Zaten en güncel sürümü (v{SURUM}) kullanıyorsunuz!")
            else:
                # Yedek dosya oluştur
                if os.path.exists(__file__):
                    shutil.copy(__file__, f"{__file__}.bak")
                
                with open(__file__, "w", encoding="utf-8") as f:
                    f.write(yeni_kod)
                print("✅ STerm Başarıyla Güncellendi!")
                print("⚠️  Lütfen programı yeniden başlatın: python3 sterm_v2.0.py")
                sys.exit(0)
        else:
            print(f"❌ Güncelleme sunucusuna ulaşılamadı. HTTP {yanit.status_code}")
    except requests.ConnectionError:
        print("❌ İnternet bağlantısı yok!")
    except Exception as e:
        print(f"❌ Hata: {e}")

# --- ARAÇ FONKSİYONLARI ---
def hava_durumu(sehir=None):
    """Hava durumunu göster."""
    config = yukle_config()
    sehir = sehir if sehir else config["hava_sehri"]
    
    is_windows = os.name == 'nt'
    try:
        if is_windows:
            os.system(f"curl -s wttr.in/{sehir}?lang=tr")
        else:
            os.system(f"curl -s wttr.in/{sehir}?lang=tr")
    except:
        print(f"❌ '{sehir}' için hava durumu alınamadı.")

def hesapla(ifade):
    """Matematiksel işlemi hesapla."""
    try:
        # Güvenlik: sadece izin verilen karakterler
        izin_verilen = set('0123456789+-*/(). ')
        if not all(c in izin_verilen for c in ifade):
            print("❌ Geçersiz karakter!")
            return
        
        sonuc = eval(ifade)
        print(f"🔢 Sonuç: {sonuc}")
    except:
        print("❌ Hatalı matematiksel işlem!")

def parola_uret(uzunluk=12):
    """Güvenli şifre üret."""
    try:
        uzunluk = int(uzunluk)
        if uzunluk < 4:
            print("⚠️  Minimum 4 karakter olmalı!")
            return
        
        karakterler = string.ascii_letters + string.digits + string.punctuation
        sifre = ''.join(random.choice(karakterler) for _ in range(uzunluk))
        print(f"🔐 Oluşturulan Şifre ({uzunluk} karakter): {sifre}")
    except:
        print("❌ Geçersiz uzunluk!")

def dosya_indir(url, dosya_adi):
    """İnternetten dosya indir."""
    if not HAS_REQUESTS:
        print("⚠️  İndirme için 'requests' kütüphanesi gereklidir.")
        return
    
    try:
        print(f"📥 {dosya_adi} indiriliyor...")
        yanit = requests.get(url, stream=True)
        
        if yanit.status_code == 200:
            toplam = int(yanit.headers.get('content-length', 0))
            indirildi = 0
            
            with open(dosya_adi, 'wb') as f:
                for chunk in yanit.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        indirildi += len(chunk)
                        if toplam > 0:
                            yuzde = (indirildi / toplam) * 100
                            print(f"  [{yuzde:.1f}%] {indirildi}/{toplam} bytes", end='\r')
            
            print(f"\n✅ {dosya_adi} başarıyla indirildi!")
        else:
            print(f"❌ İndirme başarısız (HTTP {yanit.status_code})")
    except Exception as e:
        print(f"❌ Hata: {e}")

def not_al(metin):
    """Not kaydet."""
    try:
        with open(NOTLAR_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{tarih_saat()}] {metin}\n")
        print("📝 Not kaydedildi!")
    except:
        print("❌ Not kaydedilemedi!")

def notlari_goster():
    """Kaydedilen notları göster."""
    if not os.path.exists(NOTLAR_FILE):
        print("❌ Henüz not kaydı yok.")
        return
    
    try:
        with open(NOTLAR_FILE, 'r', encoding='utf-8') as f:
            notlar = f.readlines()
        
        print(f"\n📚 Kaydedilen Notlar ({len(notlar)} toplam):\n")
        for i, not_satiri in enumerate(notlar, 1):
            print(f"{i}. {not_satiri.rstrip()}")
        print()
    except:
        print("❌ Notlar okunamadı!")

def disk_bilgisi():
    """Disk kullanımını göster."""
    try:
        toplam, kullanilan, bos = shutil.disk_usage("/")
        
        toplam_gb = toplam // (2**30)
        kullanilan_gb = kullanilan // (2**30)
        bos_gb = bos // (2**30)
        yuzde = (kullanilan / toplam) * 100
        
        print(f"\n💾 DİSK KULLANIMI:")
        print(f"  Toplam      : {toplam_gb:>6} GB")
        print(f"  Kullanılan  : {kullanilan_gb:>6} GB ({yuzde:.1f}%)")
        print(f"  Boş         : {bos_gb:>6} GB\n")
    except:
        print("❌ Disk bilgisi alınamadı!")

def ip_bulma():
    """Yerel IP adresini bul."""
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        print(f"🌐 Yerel IP Adresi: {ip}")
    except:
        print("❌ IP adresi bulunamadı!")

# --- DOSYA YÖNETİMİ FONKSİYONLARI ---
def klasor_olustur(isim):
    """Klasör oluştur."""
    try:
        os.makedirs(isim, exist_ok=True)
        print(f"✅ '{isim}' klasörü oluşturuldu!")
    except Exception as e:
        print(f"❌ Hata: {e}")

def dosya_sil(yol):
    """Dosya veya klasörü sil."""
    try:
        if os.path.isdir(yol):
            shutil.rmtree(yol)
            print(f"✅ '{yol}' klasörü silindi!")
        else:
            os.remove(yol)
            print(f"✅ '{yol}' dosyası silindi!")
    except Exception as e:
        print(f"❌ Hata: {e}")

def dosya_ara(isim):
    """Dosya veya klasör ara."""
    try:
        bulunanlar = []
        for dosya in os.listdir('.'):
            if isim.lower() in dosya.lower():
                durum = "📁" if os.path.isdir(dosya) else "📄"
                bulunanlar.append(f"{durum} {dosya}")
        
        if bulunanlar:
            print(f"\n🔍 '{isim}' aranırken bulunanlar ({len(bulunanlar)}):")
            for bulundu in bulunanlar:
                print(f"  {bulundu}")
            print()
        else:
            print(f"❌ '{isim}' ile eşleşen dosya bulunamadı.")
    except Exception as e:
        print(f"❌ Hata: {e}")

def dosya_boyutu(yol):
    """Dosya veya klasör boyutunu göster."""
    try:
        if os.path.isfile(yol):
            boyut_kb = os.path.getsize(yol) / 1024
            boyut_mb = boyut_kb / 1024
            if boyut_mb > 1:
                print(f"⚖️  '{yol}' boyutu: {boyut_mb:.2f} MB")
            else:
                print(f"⚖️  '{yol}' boyutu: {boyut_kb:.2f} KB")
        elif os.path.isdir(yol):
            toplam = 0
            for dirpath, dirnames, filenames in os.walk(yol):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    toplam += os.path.getsize(filepath)
            boyut_mb = toplam / (1024*1024)
            print(f"⚖️  '{yol}' klasörü: {boyut_mb:.2f} MB")
        else:
            print(f"❌ '{yol}' bulunamadı!")
    except Exception as e:
        print(f"❌ Hata: {e}")

def dosya_oku(yol):
    """Dosya içeriğini oku ve göster."""
    try:
        if not os.path.exists(yol):
            print(f"❌ '{yol}' bulunamadı!")
            return
        
        with open(yol, 'r', encoding='utf-8') as f:
            icerik = f.read()
        
        print(f"\n📄 '{yol}' İçeriği:")
        print("="*70)
        print(icerik)
        print("="*70 + "\n")
    except:
        print(f"❌ '{yol}' okunamadı!")

def dosya_listele():
    """Dosyaları renkli listele."""
    try:
        dosyalar = os.listdir('.')
        
        if not dosyalar:
            print("📂 Klasör boş.")
            return
        
        print(f"\n📂 Dosyalar ({len(dosyalar)} toplam):\n")
        
        # Sıralama
        klasorler = [d for d in dosyalar if os.path.isdir(d)]
        dosyalar_listesi = [d for d in dosyalar if os.path.isfile(d)]
        
        # Klasörleri göster
        for klasor in sorted(klasorler):
            print(f"  📁 {Renkler.OKBLUE}{klasor}{Renkler.ENDC}/")
        
        # Dosyaları göster
        for dosya in sorted(dosyalar_listesi):
            uzanti = os.path.splitext(dosya)[1]
            if uzanti in ['.py', '.sh', '.js', '.ts']:
                renk = Renkler.WARNING
            elif uzanti in ['.txt', '.md', '.json']:
                renk = Renkler.OKGREEN
            else:
                renk = Renkler.ENDC
            
            print(f"  📄 {renk}{dosya}{Renkler.ENDC}")
        print()
    except Exception as e:
        print(f"❌ Hata: {e}")

# --- SİSTEM BİLGİSİ ---
def sistem_analizi():
    """Derin sistem analizi yap."""
    print("\n" + Renkler.BOLD + "💻 SİSTEM ANALİZİ" + Renkler.ENDC)
    print("="*70)
    
    try:
        print(f"İşletim Sistemi  : {platform.system()} {platform.release()}")
        print(f"Platform         : {platform.platform()}")
        print(f"İşlemci          : {platform.processor()}")
        print(f"Mimari           : {platform.machine()}")
        print(f"Python Sürümü    : {platform.python_version()}")
        print(f"Bilgisayar Adı   : {socket.gethostname()}")
        print(f"Kullanıcı        : {getpass.getuser()}")
        print(f"Çalışma Dizini   : {os.getcwd()}")
    except:
        pass
    
    print("="*70 + "\n")

def surum_bilgisi():
    """Versiyon bilgilerini göster."""
    print(f"\n{Renkler.BOLD}📦 STerm SÜRÜMü{Renkler.ENDC}")
    print("="*70)
    print(f"Sürüm            : {SURUM}")
    print(f"Kod Adı          : {SURUM_ADI}")
    print(f"Takım            : Kapsül Serix Takımı")
    print(f"Geliştirici      : Kemal & Kefe3")
    print(f"Yayın Tarihi     : Nisan 2026")
    print(f"Python Sürümü    : {platform.python_version()}")
    print(f"Sistem           : {platform.system()}")
    print("="*70 + "\n")

# --- ANA LOOP ---
def main():
    """Ana program döngüsü."""
    banner_goster()
    yardim_goster()
    
    config = yukle_config()
    
    while True:
        try:
            dizin = os.getcwd().replace(os.path.expanduser("~"), "~")
            kullanici = getpass.getuser()
            sistem = platform.system()
            is_windows = sistem == "WINDOWS"
            is_mac = sistem == "Darwin"
            
            # Dinamik Prompt
            if is_windows:
                prompt = f"🪟 {Renkler.WARNING}[SERIX-WIN]{Renkler.ENDC} {Renkler.OKGREEN}{kullanici}{Renkler.ENDC}:{Renkler.OKBLUE}{dizin}{Renkler.ENDC}> "
            elif is_mac:
                prompt = f"🍎 {Renkler.WARNING}[SERIX-MAC]{Renkler.ENDC} {Renkler.OKGREEN}{kullanici}{Renkler.ENDC}:{Renkler.OKBLUE}{dizin}{Renkler.ENDC}$ "
            else:
                yetki = "[KÖK-SERIX]" if os.getuid() == 0 else "[SERIX-TITAN]"
                prompt = f"🐧 {Renkler.WARNING}{yetki}{Renkler.ENDC} {Renkler.OKGREEN}{kullanici}{Renkler.ENDC}:{Renkler.OKBLUE}{dizin}{Renkler.ENDC}$ "
            
            giris = input(prompt).strip()
            if not giris:
                continue
            
            # Geçmişe ekle
            gecmis_ekle(giris)
            
            # Komutu parçala
            parcalar = giris.split()
            komut = parcalar[0].lower()
            arguman = " ".join(parcalar[1:])
            
            # --- SİSTEM KOMUTLARI ---
            if komut == "guncelle":
                guncelleme_denetle()
            
            elif komut == "surum":
                surum_bilgisi()
            
            elif komut == "analiz":
                sistem_analizi()
            
            elif komut == "bilgisayar":
                print(f"\n📌 Bilgisayar: {socket.gethostname()}")
                print(f"💻 Sistem: {platform.system()} {platform.release()}")
                print(f"🧠 İşlemci: {platform.processor()}")
                print(f"🏗️  Mimari: {platform.machine()}\n")
            
            elif komut == "saat":
                print(f"⏰ {tarih_saat()}")
            
            elif komut == "temizle":
                banner_goster()
            
            elif komut == "yardim" or komut == "yardım":
                yardim_goster()
            
            # --- DOSYA VE DİZİN YÖNETİMİ ---
            elif komut == "yd":
                hedef = arguman if arguman else os.path.expanduser("~")
                try:
                    os.chdir(hedef)
                    print(f"✅ {hedef} dizinine geçildi.")
                except:
                    print(f"❌ Dizin bulunamadı: {hedef}")
            
            elif komut == "yarat":
                if arguman:
                    klasor_olustur(arguman)
                else:
                    print("⚠️  Kullanım: yarat [klasör_adı]")
            
            elif komut == "sil":
                if arguman:
                    dosya_sil(arguman)
                else:
                    print("⚠️  Kullanım: sil [dosya/klasör]")
            
            elif komut == "gezgin":
                dosya_listele()
            
            elif komut == "ara":
                if arguman:
                    dosya_ara(arguman)
                else:
                    print("⚠️  Kullanım: ara [dosya_adı]")
            
            elif komut == "boyut":
                if arguman:
                    dosya_boyutu(arguman)
                else:
                    print("⚠️  Kullanım: boyut [dosya/klasör]")
            
            elif komut == "oku":
                if arguman:
                    dosya_oku(arguman)
                else:
                    print("⚠️  Kullanım: oku [dosya]")
            
            elif komut == "kopyala":
                if arguman:
                    os.system(f"copy {arguman}" if is_windows else f"cp -r {arguman}")
                else:
                    print("⚠️  Kullanım: kopyala [kaynak] [hedef]")
            
            elif komut == "tası":
                if arguman:
                    os.system(f"move {arguman}" if is_windows else f"mv {arguman}")
                else:
                    print("⚠️  Kullanım: tası [kaynak] [hedef]")
            
            # --- AKILLI ARAÇLAR ---
            elif komut == "hava":
                sehir = arguman if arguman else config["hava_sehri"]
                hava_durumu(sehir)
            
            elif komut == "hesapla":
                if arguman:
                    hesapla(arguman)
                else:
                    print("⚠️  Kullanım: hesapla [işlem] (ör: 2+2*5)")
            
            elif komut == "parola-uret":
                uzunluk = arguman if arguman else "12"
                parola_uret(uzunluk)
            
            elif komut == "indir":
                if arguman and len(parcalar) >= 3:
                    url = parcalar[1]
                    dosya_adi = parcalar[2]
                    dosya_indir(url, dosya_adi)
                else:
                    print("⚠️  Kullanım: indir [url] [dosya_adı]")
            
            elif komut == "web":
                if arguman:
                    url = arguman if arguman.startswith("http") else f"https://{arguman}"
                    webbrowser.open(url)
                    print(f"🌐 {url} tarayıcıda açılıyor...")
                else:
                    print("⚠️  Kullanım: web [url]")
            
            elif komut == "ip_bul":
                ip_bulma()
            
            elif komut == "ping":
                if arguman:
                    os.system(f"ping -n 4 {arguman}" if is_windows else f"ping -c 4 {arguman}")
                else:
                    print("⚠️  Kullanım: ping [host]")
            
            elif komut == "disk":
                disk_bilgisi()
            
            elif komut == "not-al":
                if arguman:
                    not_al(arguman)
                else:
                    print("⚠️  Kullanım: not-al [metin]")
            
            elif komut == "notları-gör":
                notlari_goster()
            
            # --- PAKET VE YÖNETİM ---
            elif komut == "serix-get":
                if arguman:
                    print(f"📦 '{arguman}' kurulmaya çalışılıyor...")
                    if is_windows:
                        os.system(f"winget install {arguman}")
                    elif is_mac:
                        os.system(f"brew install {arguman}")
                    else:
                        if os.path.exists("/usr/bin/pacman"):
                            os.system(f"sudo pacman -S --noconfirm {arguman}")
                        elif os.path.exists("/usr/bin/apt"):
                            os.system(f"sudo apt update && sudo apt install -y {arguman}")
                        else:
                            print("❌ Paket yöneticisi tanınmadı!")
                else:
                    print("⚠️  Kullanım: serix-get [paket_adı]")
            
            elif komut == "serix-kök":
                if is_windows:
                    print("🔑 Windows'ta yönetici olarak yeni terminal açılıyor...")
                    os.system("powershell Start-Process python -Verb runAs")
                elif is_mac:
                    print("🔑 Root erişimi isteniyor...")
                    os.system("sudo -s")
                else:
                    print("🔑 Root erişimi isteniyor...")
                    os.system("sudo -s")
            
            elif komut == "kapat":
                if is_windows:
                    os.system("shutdown /s /t 1")
                elif is_mac:
                    os.system("osascript -e 'tell app \"System Events\" to shut down'")
                else:
                    os.system("sudo shutdown -h now")
            
            elif komut == "yeniden":
                if is_windows:
                    os.system("shutdown /r /t 1")
                elif is_mac:
                    os.system("osascript -e 'tell app \"System Events\" to restart'")
                else:
                    os.system("sudo reboot")
            
            elif komut == "kilitle":
                if is_windows:
                    os.system("rundll32.exe user32.dll,LockWorkStation")
                elif is_mac:
                    os.system("pmset displaysleepnow")
                else:
                    os.system("xdg-screensaver lock")
            
            # --- GEÇMİŞ VE AYARLAR ---
            elif komut == "gecmis":
                satir_sayisi = int(arguman) if arguman else 50
                gecmis_goster(satir_sayisi)
            
            elif komut == "config":
                print(f"\n⚙️  Mevcut Konfigürasyon:")
                for anahtar, deger in config.items():
                    print(f"  {anahtar}: {deger}")
                print()
            
            elif komut == "ayar":
                if arguman and "=" in arguman:
                    anahtar, deger = arguman.split("=", 1)
                    config[anahtar.strip()] = deger.strip()
                    kaydet_config(config)
                    print(f"✅ Ayar kaydedildi: {anahtar} = {deger}")
                else:
                    print("⚠️  Kullanım: ayar [anahtar]=[değer]")
            
            # --- ÇIKIŞ ---
            elif komut == "çıkış" or komut == "exit":
                print("👋 STerm'den ayrılıyorsunuz. Hoşça kalın!")
                break
            
            # --- BİLİNMEYEN KOMUTLAR ---
            else:
                print(f"❓ '{komut}' komutu tanınmadı.")
                print("   Yardım için 'yardim' yazın.")
                # Sisteme komut gönder
                if not komut.startswith("/"):
                    try:
                        os.system(giris)
                    except:
                        pass
        
        except KeyboardInterrupt:
            print("\n⚠️  Çıkmak için 'çıkış' yazın.")
        except Exception as e:
            print(f"❌ Hata: {e}")

# --- PROGRAM BAŞLANGICI ---
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 STerm sonlandırılıyor...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Kritik Hata: {e}")
        sys.exit(1)
