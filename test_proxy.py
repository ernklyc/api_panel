"""
Proxy Endpoint Test Scripti
Sunucunun güvenli olduğunu ve proxy endpoint'in çalıştığını doğrular
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("🧪 API Key Manager - Güvenlik ve Proxy Test")
print("=" * 70)

# Test 1: Sunucu sağlık kontrolü
print("\n1️⃣ Sunucu sağlık kontrolü...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        print("   ✅ Sunucu çalışıyor")
        print(f"   📊 {response.json()}")
    else:
        print("   ❌ Sunucu yanıt vermiyor")
        exit(1)
except Exception as e:
    print(f"   ❌ HATA: Sunucu çalışmıyor! {e}")
    print("   💡 Önce sunucuyu başlat: python api_key_manager.py")
    exit(1)

# Test 2: Key endpoint güvenlik testi (tam key döndürmemeli)
print("\n2️⃣ Güvenlik Testi: Key endpoint anahtarı açığa çıkarmamalı...")
try:
    response = requests.get(f"{BASE_URL}/api/v1/keys/replicate_api", timeout=5)
    data = response.json()
    
    if 'key' in data and len(data['key']) > 15:
        print("   ❌ GÜVENLİK SORUNU: Endpoint tam anahtarı döndürüyor!")
        print(f"   🔑 Dönen: {data['key'][:10]}...")
    elif 'key_preview' in data:
        print("   ✅ Güvenli: Sadece önizleme döndürüyor")
        print(f"   🔒 Preview: {data['key_preview']}")
        print(f"   📝 Not: {data.get('note', 'N/A')}")
    else:
        print(f"   ℹ️  Yanıt: {json.dumps(data, indent=2)}")
except Exception as e:
    print(f"   ❌ Test başarısız: {e}")

# Test 3: Deprecated /use endpoint testi
print("\n3️⃣ Deprecated Endpoint Testi: /use endpoint devre dışı olmalı...")
try:
    response = requests.post(f"{BASE_URL}/api/v1/keys/replicate_api/use", timeout=5)
    data = response.json()
    
    if response.status_code == 403:
        print("   ✅ Güvenli: Endpoint devre dışı bırakıldı")
        print(f"   📝 Mesaj: {data.get('message', 'N/A')}")
    else:
        print(f"   ⚠️  Beklenmeyen yanıt: {data}")
except Exception as e:
    print(f"   ❌ Test başarısız: {e}")

# Test 4: Proxy endpoint varlık kontrolü (gerçek Replicate çağrısı yapmadan)
print("\n4️⃣ Proxy Endpoint Varlık Kontrolü...")
try:
    # Boş body ile POST deneyelim (hata dönmeli ama endpoint var olduğunu gösterir)
    response = requests.post(f"{BASE_URL}/api/v1/proxy/replicate", 
                            json={}, 
                            timeout=5)
    data = response.json()
    
    # 400 (bad request) veya 500 bekliyoruz - endpoint var demektir
    if response.status_code in [400, 500]:
        print("   ✅ Proxy endpoint mevcut ve çalışıyor")
        print(f"   📝 Yanıt: {data.get('error', 'N/A')}")
    else:
        print(f"   ℹ️  Beklenmeyen yanıt: {response.status_code}")
        print(f"   📊 {json.dumps(data, indent=2)}")
except Exception as e:
    print(f"   ❌ Endpoint bulunamadı: {e}")

# Test 5: Gerçek Replicate API testi (opsiyonel - sadece endpoint yapısını kontrol eder)
print("\n5️⃣ Replicate API Yapı Testi (basit prediction)...")
print("   ℹ️  Bu test gerçek bir Replicate model çağrısı yapar.")
print("   ⏳ Test ediliyor...")

test_payload = {
    "version": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
    "input": {
        "prompt": "a simple test image",
        "num_outputs": 1
    }
}

try:
    response = requests.post(f"{BASE_URL}/api/v1/proxy/replicate", 
                            json=test_payload,
                            timeout=30)
    data = response.json()
    
    if response.status_code in [200, 201]:
        print("   ✅ Proxy başarıyla Replicate API'yi çağırdı!")
        if 'data' in data and 'id' in data.get('data', {}):
            pred_id = data['data']['id']
            print(f"   🎯 Prediction ID: {pred_id}")
            print(f"   📊 Status: {data['data'].get('status', 'unknown')}")
            
            # Prediction durumu kontrolü
            print(f"\n   🔄 Prediction durumu sorgulanıyor...")
            time.sleep(2)
            status_response = requests.get(f"{BASE_URL}/api/v1/proxy/replicate/{pred_id}", timeout=10)
            status_data = status_response.json()
            
            if status_response.status_code == 200:
                print(f"   ✅ Durum endpoint'i çalışıyor")
                print(f"   📊 Status: {status_data.get('data', {}).get('status', 'unknown')}")
            else:
                print(f"   ⚠️  Durum sorgulanamadı: {status_data.get('error', 'N/A')}")
        else:
            print(f"   ℹ️  Yanıt: {json.dumps(data, indent=2)[:200]}...")
    else:
        print(f"   ⚠️  API çağrısı başarısız: {response.status_code}")
        print(f"   📝 Hata: {data.get('error', 'N/A')}")
except requests.exceptions.Timeout:
    print("   ⏱️  Timeout: Replicate API yanıt vermedi (normal olabilir)")
except Exception as e:
    print(f"   ❌ Test hatası: {e}")

print("\n" + "=" * 70)
print("✅ Test tamamlandı!")
print("=" * 70)
print("\n📚 Flutter için kullanım örnekleri:")
print("""
// Dart/Flutter HTTP isteği örneği:

import 'package:http/http.dart' as http;
import 'dart:convert';

// 1. Prediction oluştur
final response = await http.post(
  Uri.parse('http://your-server:8000/api/v1/proxy/replicate'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'version': 'model_version_id',
    'input': {
      'prompt': 'a photo of a person',
      // diğer parametreler...
    }
  }),
);

final data = jsonDecode(response.body);
final predictionId = data['data']['id'];

// 2. Prediction durumunu kontrol et
final statusResponse = await http.get(
  Uri.parse('http://your-server:8000/api/v1/proxy/replicate/$predictionId'),
);

final statusData = jsonDecode(statusResponse.body);
print('Status: ${statusData['data']['status']}');
print('Output: ${statusData['data']['output']}');
""")
print("=" * 70)
