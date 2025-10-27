# 🚀 Movie Face AI - Sıfırdan Kurulum

## 📍 Proje Konumu

```
C:\api_panel
```

## 🎯 Adım Adım Kurulum

### ADIM 1: Klasör Oluştur

```bash
cd C:\
mkdir api_panel
cd api_panel
```

### ADIM 2: Dosyaları Oluştur

Tüm dosyaları `C:\api_panel` klasörüne kopyala:
- `api_key_manager.py`
- `requirements.txt`
- `initialize_api_keys.py`
- `start_server.bat`
- `README.md`

### ADIM 3: Key'i Ekle

`initialize_api_keys.py` dosyasında key zaten var:
```python
REPLICATE_API_KEY = "r8_8bPWQwE9O66KH2fpKwyKAPEwNMdT7sw3a3mk0"
```

### ADIM 4: Python Paketlerini Yükle

```bash
pip install flask flask-cors requests
```

Veya:
```bash
pip install -r requirements.txt
```

### ADIM 5: Key Dosyasını Oluştur

```bash
python initialize_api_keys.py
```

Çıktı:
```
✅ API Key dosyası oluşturuldu: api_keys.json
📝 Key adı: replicate_api
📡 Platform: Replicate
```

### ADIM 6: Server'ı Başlat

```bash
python api_key_manager.py
```

Çıktı:
```
============================================================
🔐 Movie Face AI - API Key Manager
============================================================
📡 Server: http://0.0.0.0:8000
✅ Server başlatıldı! Backend çalışıyor.
```

### ADIM 7: Test Et

Yeni terminal aç:
```bash
curl http://localhost:8000/health
```

Cevap:
```json
{"status":"ok","service":"API Key Manager","version":"1.0.0"}
```

## 📱 Flutter App'te Kullan

Flutter app'te key'i kullan:

```dart
import 'package:movie_face_ai/services/api_key_service.dart';

// Key'i al
final apiKey = await ApiKeyService.getApiKey('replicate_api');

// Kullan
if (apiKey != null) {
  print('Key alındı: $apiKey');
} else {
  print('Key bulunamadı');
}
```

## ✅ Kontrol Listesi

- [ ] Klasör oluşturuldu (C:\api_panel)
- [ ] Dosyalar kopyalandı
- [ ] Python paketleri yüklendi
- [ ] `python initialize_api_keys.py` çalıştırıldı
- [ ] `api_keys.json` oluşturuldu
- [ ] `python api_key_manager.py` çalıştırıldı
- [ ] Server 8000 portunda çalışıyor
- [ ] Health check başarılı
- [ ] Flutter app key'i alabiliyor

## 🆘 Sorun Giderme

### "Module not found"

```bash
pip install flask flask-cors requests
```

### "Port already in use"

Windows:
```bash
netstat -ano | findstr :8000
taskkill /F /PID <PID>
```

### "API Key Manager çalışmıyor"

1. Server çalışıyor mu? → `python api_key_manager.py`
2. Port açık mı? → `netstat -ano | findstr :8000`
3. Firewall ayarları

## 📂 Dosya Yapısı (C:\api_panel)

```
C:\api_panel\
├── api_key_manager.py        # Flask server
├── api_keys.json             # Key'ler (oluşturulacak)
├── initialize_api_keys.py    # Key hazırlama
├── requirements.txt          # Python paketleri
├── start_server.bat          # Tek tıkla başlat
└── README.md                 # Dokümantasyon
```

## 🚀 Tek Komutla Başlat (Gelecekte)

```bash
start_server.bat
```

## 📝 Notlar

- Server localhost:8000'de çalışır
- Key'ler `api_keys.json` dosyasında saklanır
- Flutter app `http://localhost:8000/api/v1` kullanır
- Key hiçbir zaman Flutter app'ine kod olarak girilmez

