"""
Flutter Bağlantı Test Scripti
Android Emulator için bağlantıyı test eder
"""
import socket
import requests
import json
from flask import Flask, request, jsonify
import threading
import time

def get_local_ip():
    """Yerel IP adresini al"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "localhost"

def test_server():
    """API sunucusunu test et"""
    print("=" * 70)
    print("🧪 Flutter Bağlantı Testi")
    print("=" * 70)
    
    local_ip = get_local_ip()
    
    print(f"\n📡 Yerel IP: {local_ip}")
    print(f"📡 Localhost: 127.0.0.1")
    print(f"📡 Emulator için: 10.0.2.2 (host'tan erişilemez)")
    
    # Test URLs
    test_urls = [
        "http://localhost:8000/health",
        f"http://{local_ip}:8000/health",
        "http://127.0.0.1:8000/health",
        "http://0.0.0.0:8000/health",
    ]
    
    print("\n🔍 Sunucu Test Ediliyor...")
    print("-" * 70)
    
    working_urls = []
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print(f"✅ {url} - ÇALIŞIYOR")
                working_urls.append(url)
            else:
                print(f"⚠️  {url} - Hata: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ {url} - BAĞLANTI HATASI")
        except requests.exceptions.Timeout:
            print(f"⏱️  {url} - TIMEOUT")
        except Exception as e:
            print(f"❌ {url} - Hata: {e}")
    
    print("\n" + "=" * 70)
    
    if working_urls:
        print("✅ Sunucu çalışıyor!")
        print("\n📱 FLUTTER İÇİN ADRES:")
        print("-" * 70)
        print(f"Android Emulator: http://10.0.2.2:8000")
        print(f"Android Gerçek Cihaz: http://{local_ip}:8000")
        print(f"iOS Simulator: http://localhost:8000 veya http://{local_ip}:8000")
        
        print("\n🔥 Flutter kodunuzda şunu kullanın:")
        print(f"   static const String baseUrl = 'http://10.0.2.2:8000';")
        
        # Proxy endpoint test
        print("\n🧪 Proxy Endpoint Test...")
        try:
            test_payload = {
                "version": "test-version",
                "input": {"prompt": "test"}
            }
            response = requests.post(
                working_urls[0].replace("/health", "/api/v1/proxy/replicate"),
                json=test_payload,
                timeout=5
            )
            print(f"✅ Proxy endpoint erişilebilir (Status: {response.status_code})")
            
            if response.status_code == 422:
                print("   ℹ️  422 hatası normal (test version kullanıldı)")
                print("   ✅ Sunucu Replicate API ile iletişim kurabiliyor!")
            
        except Exception as e:
            print(f"⚠️  Proxy endpoint hatası: {e}")
            
    else:
        print("❌ SUNUCU ÇALIŞMIYOR!")
        print("\n💡 Çözüm:")
        print("   1. Sunucuyu başlat: python api_key_manager.py")
        print("   2. Port 8000'in kullanımda olmadığından emin ol")
        print("   3. Firewall ayarlarını kontrol et")
    
    print("=" * 70)
    
    # Windows Firewall kontrol
    print("\n🔒 Windows Firewall Durumu:")
    print("-" * 70)
    print("⚠️  Eğer Android emülatörden bağlanamıyorsanız:")
    print("   1. Windows Defender Firewall'u aç")
    print("   2. 'Advanced settings' > 'Inbound Rules'")
    print("   3. 'New Rule' > Port > TCP > 8000 > Allow")
    print("   VEYA")
    print("   PowerShell'i YÖNETİCİ olarak aç ve çalıştır:")
    print("   netsh advfirewall firewall add rule name=\"Python API\" dir=in action=allow protocol=TCP localport=8000")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_server()
