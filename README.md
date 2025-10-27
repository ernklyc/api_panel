# 🔐 API Key Manager - GÜVENLİ VERSİYON

> ⚠️ **ÖNEMLİ GÜVENLİK GÜNCELLEMESİ**: Bu versiyon artık API anahtarlarını istemciye göndermez!
> Flutter uygulamanız için güvenli proxy endpoint'ler eklendi.

## 🚀 Hızlı Başlangıç

### 1. Sunucuyu Başlat
```bash
python api_key_manager.py
```

### 2. Test Et
```bash
python test_proxy.py
```

✅ Tüm testler başarılı olmalı!

## 🔒 Güvenlik Özellikleri

- ✅ **API anahtarları istemciye gönderilmez**
- ✅ **Güvenli proxy pattern** - Sunucu Replicate'i çağırır
- ✅ **Git koruması** - `.gitignore` ile key dosyaları saklanır
- ✅ **Deprecated endpoint'ler** - Güvensiz endpoint'ler devre dışı

## 📱 Flutter Entegrasyonu

**Detaylı dokümantasyon:** [`FLUTTER_INTEGRATION.md`](FLUTTER_INTEGRATION.md)

### Hızlı Örnek

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

// Prediction oluştur
final response = await http.post(
  Uri.parse('http://your-server:8000/api/v1/proxy/replicate'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'version': 'model-version-id',
    'input': {'prompt': 'a photo of a person'},
  }),
);

final data = jsonDecode(response.body);
final predictionId = data['data']['id'];

// Durumu kontrol et
final status = await http.get(
  Uri.parse('http://your-server:8000/api/v1/proxy/replicate/$predictionId'),
);
```

## 🛠️ API Endpoint'leri

### Yönetim Endpoint'leri (Key yönetimi için)
- `GET /api/v1/keys` - Tüm key'leri listele (sadece önizleme)
- `POST /api/v1/keys` - Yeni key ekle
- `PUT /api/v1/keys/<name>` - Key güncelle
- `DELETE /api/v1/keys/<name>` - Key sil

### 🔒 Güvenli Proxy Endpoint'leri (Flutter için)
- `POST /api/v1/proxy/replicate` - Replicate prediction oluştur
- `GET /api/v1/proxy/replicate/<id>` - Prediction durumu sorgula

## 📝 Manuel Key Ekleme

### 1. Yöntem: Script ile

```bash
python initialize_api_keys.py
```

### 2. Yöntem: Sunucu çalışırken API ile
```bash
python add_key.py
```

### 3. Yöntem: Key güncelleme
```bash
python update_key.py
```

### 4. Sunucuyu Başlat

```bash
python api_key_manager.py
```

Server çalışıyor! ✅

## 🧪 Test ve Doğrulama

### Güvenlik testleri:
```bash
python test_proxy.py
```

### Manuel test:
```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/keys
```

## 📁 Dosyalar

- `api_key_manager.py` - Ana sunucu (proxy endpoint'ler ile)
- `test_proxy.py` - Güvenlik ve proxy testleri
- `initialize_api_keys.py` - Key hazırla
- `add_key.py` - Sunucuya key ekle
- `update_key.py` - Key güncelle
- `list_keys.py` - Key'leri listele
- `.gitignore` - Key dosyalarını korur
- `FLUTTER_INTEGRATION.md` - Detaylı Flutter dokümantasyonu
- `requirements.txt` - Python paketleri

## 🆘 Sorun Giderme

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"Port already in use"**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /F /PID <PID>

# Linux
sudo lsof -i :8000
sudo kill -9 <PID>
```

## ✅ Her Şey Hazır!

1. Key'in dosyada
2. Server çalışıyor
3. Flutter app key'i alabilir
