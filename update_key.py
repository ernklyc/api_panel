"""
API Key Güncelleme Scripti
"""
import requests

print("=" * 60)
print("✏️ API Key Güncelleme")
print("=" * 60)

# Yeni key al
print("\nYeni Replicate API Key'i girin:")
print("URL: https://replicate.com/account/api-tokens\n")

new_key = input("Yeni API Key: ").strip()

if not new_key.startswith('r8_'):
    print("⚠️ Geçersiz key formatı! r8_ ile başlamalı.")
    exit()

# Key'i güncelle
try:
    response = requests.put('http://localhost:8000/api/v1/keys/replicate_api', json={
        'key': new_key
    })
    
    if response.status_code == 200:
        print("\n✅ API Key başarıyla güncellendi!")
    else:
        print(f"❌ Hata: {response.json()}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ API Key Manager çalışmıyor!")
    print("   Önce şunu çalıştır: python api_key_manager.py")
except Exception as e:
    print(f"\n❌ Hata: {e}")

print("=" * 60)

