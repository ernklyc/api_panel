"""
API Key Ekleme Scripti
"""
import requests

print("=" * 60)
print("🔑 API Key Ekleme")
print("=" * 60)

# Replicate API Key al
print("\nReplicate API Key URL'den al:")
print("https://replicate.com/account/api-tokens")
print("\nKey formatı: r8_xxxxxxxxxxxxx\n")

api_key = input("API Key'i yapıştır: ").strip()

if not api_key.startswith('r8_'):
    print("⚠️ Geçersiz key formatı! r8_ ile başlamalı.")
    exit()

# Server'a ekle
try:
    response = requests.post('http://localhost:8000/api/v1/keys', json={
        'name': 'replicate_api',
        'key': api_key,
        'platform': 'Replicate'
    })
    
    if response.status_code == 200:
        print("\n✅ API Key başarıyla eklendi!")
        print(f"📋 Key adı: replicate_api")
        print(f"📡 Platform: Replicate")
        
        # Key listesini göster
        print("\n📊 Şu anda kayıtlı key'ler:")
        list_response = requests.get('http://localhost:8000/api/v1/keys')
        if list_response.status_code == 200:
            data = list_response.json()
            for name, info in data['keys'].items():
                print(f"   • {name} - {info['platform']}")
    else:
        error = response.json()
        if 'already exists' in error.get('error', ''):
            print(f"\n⚠️ Bu key zaten var! Güncellemek için:")
            print(f"   python update_key.py")
        else:
            print(f"❌ Hata: {error}")
            
except requests.exceptions.ConnectionError:
    print("\n❌ API Key Manager çalışmıyor!")
    print("   Önce şunu çalıştır: python api_key_manager.py")
except Exception as e:
    print(f"\n❌ Hata: {e}")

print("=" * 60)
