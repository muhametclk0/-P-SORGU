import socket
import requests
import platform
import ipaddress
import psutil
import shutil
import uuid
import subprocess
import time
import datetime
import hashlib
import os

def banner(): 
    print(""" 
    ╔══════════════════════════════╗ 
           ip sorgu    
           
              isnta - muhametclk0   
 
    ╚══════════════════════════════╝ 
    """)

def ip_bilgisi_al(ip):
    bilgi = {}
    
   
    bilgi['🌍 IP Adresi'] = ip
    bilgi['🔒 Özel IP mi?'] = ipaddress.ip_address(ip).is_private
    bilgi['🖥️ Host Adı'] = socket.getfqdn(ip)
    bilgi['🔢 IP Versiyonu'] = 'IPv4' if '.' in ip else 'IPv6'

   
    yanit = {}
    try:
        yanit = requests.get(f'https://ipinfo.io/{ip}/json', timeout=5).json()
    except requests.RequestException as e:
        print(f"API isteği sırasında hata oluştu: {e}")
    
    bilgi['🏙️ Şehir'] = yanit.get('city', 'Bilinmiyor')
    bilgi['📍 Bölge'] = yanit.get('region', 'Bilinmiyor')
    bilgi['🇨🇦 Ülke'] = yanit.get('country', 'Bilinmiyor')
    bilgi['🏢 İnternet Sağlayıcısı'] = yanit.get('org', 'Bilinmiyor')
    bilgi['📮 Posta Kodu'] = yanit.get('postal', 'Bilinmiyor')
    bilgi['🕰️ Zaman Dilimi'] = yanit.get('timezone', 'Bilinmiyor')
    bilgi['🌍 Koordinatlar'] = yanit.get('loc', 'Bilinmiyor')

    
    bilgi['📅 Sorgu Zamanı'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bilgi['💻 İşletim Sistemi'] = platform.system()
    bilgi['🔢 İşletim Sistemi Sürümü'] = platform.version()
    bilgi['⚙️ İşlemci'] = platform.processor()
    bilgi['🔢 Çekirdek Sayısı'] = psutil.cpu_count(logical=False) if hasattr(psutil, 'cpu_count') else 'Bilinmiyor'
    
    try:
        bilgi['⏳ Sistem Uptime'] = time.strftime("%H saat, %M dakika, %S saniye", time.gmtime(time.time() - psutil.boot_time()))
    except (PermissionError, AttributeError):
        bilgi['⏳ Sistem Uptime'] = 'Bilinmiyor'
    
    bilgi['👤 Kullanıcı Adı'] = platform.node()
    
    try:
        bilgi['🛑 Toplam RAM'] = f"{psutil.virtual_memory().total / (1024**3):.2f} GB"
        bilgi['💾 Kullanılan RAM'] = f"{psutil.virtual_memory().used / (1024**3):.2f} GB"
        bilgi['📊 RAM Kullanımı (%)'] = psutil.virtual_memory().percent
    except (PermissionError, AttributeError):
        bilgi['🛑 Toplam RAM'] = 'Bilinmiyor'
        bilgi['💾 Kullanılan RAM'] = 'Bilinmiyor'
        bilgi['📊 RAM Kullanımı (%)'] = 'Bilinmiyor'
    
    try:
        bilgi['💽 Toplam Depolama'] = f"{shutil.disk_usage('/').total / (1024**3):.2f} GB"
        bilgi['📂 Kullanılan Depolama'] = f"{shutil.disk_usage('/').used / (1024**3):.2f} GB"
        bilgi['📀 Disk Kullanımı (%)'] = shutil.disk_usage('/').used / shutil.disk_usage('/').total * 100
    except (PermissionError, AttributeError):
        bilgi['💽 Toplam Depolama'] = 'Bilinmiyor'
        bilgi['📂 Kullanılan Depolama'] = 'Bilinmiyor'
        bilgi['📀 Disk Kullanımı (%)'] = 'Bilinmiyor'
    
    bilgi['🔑 IP Hash (SHA-256)'] = hashlib.sha256(ip.encode()).hexdigest()
    bilgi['🌐 Yerel IP Adresi'] = socket.gethostbyname(socket.gethostname())
    bilgi['💻 Sistem Mimarisi'] = platform.architecture()[0]
    
    try:
        bilgi['⚡ CPU Kullanımı (%)'] = psutil.cpu_percent()
    except (PermissionError, AttributeError):
        bilgi['⚡ CPU Kullanımı (%)'] = 'Bilinmiyor'
    
    try:
        bilgi['🔍 Açık Portlar'] = [conn.laddr.port for conn in psutil.net_connections() if conn.status == 'LISTEN']
    except (PermissionError, AttributeError):
        bilgi['🔍 Açık Portlar'] = 'Bilinmiyor'
    
    try:
        bilgi['📑 Çalışan Süreç Sayısı'] = len(psutil.pids())
    except (PermissionError, AttributeError):
        bilgi['📑 Çalışan Süreç Sayısı'] = 'Bilinmiyor'
    
    try:
        bilgi['🔗 TCP Bağlantı Sayısı'] = len([conn for conn in psutil.net_connections() if conn.type == socket.SOCK_STREAM])
        bilgi['🔗 UDP Bağlantı Sayısı'] = len([conn for conn in psutil.net_connections() if conn.type == socket.SOCK_DGRAM])
    except (PermissionError, AttributeError):
        bilgi['🔗 TCP Bağlantı Sayısı'] = 'Bilinmiyor'
        bilgi['🔗 UDP Bağlantı Sayısı'] = 'Bilinmiyor'
    
    try:
        battery = psutil.sensors_battery()
        bilgi['🔋 Pil Durumu (%)'] = battery.percent if battery else 'Yok'
        bilgi['🔌 Şarj Durumu'] = 'Takılı' if battery and battery.power_plugged else 'Takılı Değil'
    except (PermissionError, AttributeError):
        bilgi['🔋 Pil Durumu (%)'] = 'Yok'
        bilgi['🔌 Şarj Durumu'] = 'Takılı Değil'

    
    if platform.system() == 'Linux':
        try:
            bilgi['🖥️ Ekran Çözünürlüğü'] = subprocess.run(['xdpyinfo | grep dimensions'], shell=True, capture_output=True, text=True).stdout.strip()
            bilgi['📶 Wi-Fi Sinyal Gücü'] = subprocess.run(['iwconfig 2>/dev/null | grep -i --color quality'], shell=True, capture_output=True, text=True).stdout.strip()
        except subprocess.SubprocessError as e:
            print(f"Platforma özgü bilgi toplama sırasında hata oluştu: {e}")
    else:
        bilgi['🖥️ Ekran Çözünürlüğü'] = 'Bilinmiyor'
        bilgi['📶 Wi-Fi Sinyal Gücü'] = 'Bilinmiyor'

    
    bilgi['📂 Sistem Yolu'] = os.getcwd()
    bilgi['🔒 Anonim Sistem Bilgisi'] = uuid.uuid4()
    bilgi['⚙️ CPU Model'] = platform.processor()
    bilgi['🔋 Pil Sağlığı'] = 'Bilinmiyor'
    bilgi['🕹️ Sistem Performansı'] = 'Bilinmiyor'
    bilgi['🗂️ Dosya Sistemi Kullanımı'] = 'Bilinmiyor'
    bilgi['🖥️ GPU Kullanımı'] = "Bilinmiyor"
    bilgi['🌍 IP Bilgisi (Geolokasyon)'] = yanit.get('loc', 'Bilinmiyor')
    bilgi['🛠️ Donanım Durumu'] = "Bilinmiyor"
    bilgi['🌐 Internet Durumu'] = 'Bağlı' if psutil.net_if_addrs() else 'Bağlantı Yok'
    bilgi['📞 Ağ Bağlantı Durumu'] = 'Bilinmiyor'
    bilgi['🎮 Sistem Belleği'] = 'Bilinmiyor'
    bilgi['📉 Sistem CPU Yükü'] = 'Bilinmiyor'
    bilgi['🌌 Bellek Durumu'] = 'Bilinmiyor'
    bilgi['⏱️ Zaman Ayarı'] = datetime.datetime.now()
    bilgi['🔎 Sistem Adı'] = platform.node()
    bilgi['📲 Sistem Bilgisi'] = platform.platform()
    bilgi['🔗 Ethernet Durumu'] = 'Bilinmiyor'

    return bilgi


def main():
    banner()
    while True:
        ip = input("𝗜𝗣 𝗚𝗜𝗥: ").strip()
        if ip.lower() == 'q':
            print("Programdan çıkılıyor...")
            break
        try:
           
            ipaddress.ip_address(ip)
            bilgi = ip_bilgisi_al(ip)
            for key, value in bilgi.items():
                print(f"{key}: {value}")
        except ValueError:
            print("Geçersiz IP adresi! Lütfen doğru bir IP adresi girin.")

if __name__ == "__main__":
    main()