# 🚀 API Key Manager - Hızlı Başlangıç

## 1️⃣ Server'ı Başlat

```bash
cd admin_panel
python api_key_manager.py
```

Terminal'de şunu göreceksin:
```
✅ Server başlatıldı! Backend çalışıyor.
```

## 2️⃣ API Key Ekle

**Seçenek A: Python Script (Kolay)**

Yeni bir terminal aç:
```bash
cd admin_panel
python add_key.py
```

Key'i yaz. Başarı mesajını göreceksin.

**Seçenek B: Curl**

```bash
curl -X POST http://localhost:8000/api/v1/keys -H "Content-Type: application/json" -d "{\"name\":\"replicate_api\",\"key\":\"r8_KEY_BURAYA\",\"platform\":\"Replicate\"}"
```

## 3️⃣ Flutter App'de Kullan

```dart
import 'package:movie_face_ai/services/api_key_service.dart';

// Key'i al
final apiKey = await ApiKeyService.getApiKey('replicate_api');

// Key'i kullan
await ReplicateService.generate(apiKey: apiKey);
```

## ✅ Hazır!

Artık API key'lerini güvenli bir şekilde kullanabilirsin.

## 🧪 Test

```bash
# Key listesi
curl http://localhost:8000/api/v1/keys

# Key al
curl http://localhost:8000/api/v1/keys/replicate_api

# Key'i kullan
curl -X POST http://localhost:8000/api/v1/keys/replicate_api/use
```

## 📱 Production

Server'da çalıştır:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 api_key_manager:app
```

Flutter app'inde URL'i değiştir:
```dart
static const String baseUrl = 'https://your-server.com/api/v1';
```

