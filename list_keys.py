"""
Key Listesi Görüntüleme
"""
import requests
import json

try:
    response = requests.get('http://localhost:8000/api/v1/keys')
    
    if response.status_code == 200:
        data = response.json()
        keys = data['keys']
        
        print("=" * 60)
        print("📋 Kayıtlı API Key'ler")
        print("=" * 60)
        
        if not keys:
            print("   Henüz key eklenmemiş.")
            print("   Ekle: python add_key.py")
        else:
            for name, info in keys.items():
                print(f"\n🔑 {name}")
                print(f"   Platform: {info['platform']}")
                print(f"   Key: {info['key_preview']}")
                print(f"   Son kullanım: {info['last_used']}")
        
        print("=" * 60)
    else:
        print("❌ Key listesi alınamadı")
        
except requests.exceptions.ConnectionError:
    print("❌ API Key Manager çalışmıyor!")
    print("   Başlat: python api_key_manager.py")
except Exception as e:
    print(f"❌ Hata: {e}")

