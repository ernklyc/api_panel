# 🔐 API Key Manager & Secure Proxy Server

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Deploy to Render](https://img.shields.io/badge/deploy-render-purple.svg)](https://render.com)

> 🚀 **Production-ready API Proxy Server** - Secure API key management and proxy service for Flutter/mobile applications. Deployed on Render with zero-config deployment.

**Live Demo:** [https://api-panel-5c1o.onrender.com](https://api-panel-5c1o.onrender.com)

---

## � İçindekiler

- [Proje Hakkında](#-proje-hakkında)
- [Özellikler](#-özellikler)
- [Teknolojiler](#-teknolojiler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [API Endpoints](#-api-endpoints)
- [Deployment](#-deployment)
- [Güvenlik](#-güvenlik)
- [Dokümantasyon](#-dokümantasyon)

---

## 🎯 Proje Hakkında

Bu proje, **Flutter/mobil uygulamalar için güvenli API proxy servisi** sağlar. Ana amacı:

- 🔒 **API anahtarlarını client'tan gizlemek**
- 🌐 **Replicate API için güvenli proxy sağlamak**
- ☁️ **Ücretsiz cloud deployment** (Render.com)
- 📱 **Flutter uygulamaları ile kolay entegrasyon**

### Senaryo

Bir Flutter uygulamanız var ve Replicate API kullanıyorsunuz. API anahtarınızı **uygulamaya gömdüğünüzde**:
- ❌ Herkes APK'yı decompile edip anahtarı çalabilir
- ❌ API anahtarı public domain'e düşer
- ❌ Güvenlik riski oluşur

### Çözüm

Bu API Proxy Server:
- ✅ API anahtarını **sunucuda** saklar
- ✅ Flutter uygulamanız **proxy üzerinden** istek atar
- ✅ Anahtar **asla client'a iletilmez**
- ✅ **Ücretsiz Render.com** ile deploy edilir

---

## ✨ Özellikler

### 🔐 Güvenlik
- **Environment Variable** desteği (production için)
- **Fallback to local JSON** (development için)
- **CORS** yapılandırması (Flutter için)
- **API key hiçbir zaman client'a gönderilmez**
- **Deprecated endpoint'ler** devre dışı

### 🚀 Deployment
- **Render.com** otomatik deployment
- **Zero-config** deployment (Procfile + render.yaml)
- **Free tier** support
- **Auto-deploy** on git push

### 📱 Flutter/Mobile Integration
- **RESTful API** endpoints
- **JSON** responses
- **Polling** desteği (prediction status)
- **Error handling**

### 🛠️ Development
- **Local development** için `api_keys.json`
- **Test script'leri** dahil
- **Health check** endpoint
- **Detailed logging**

---

## 🔧 Teknolojiler

### Backend
- **Python 3.8+**
- **Flask 3.0.0** - Web framework
- **Flask-CORS 4.0.0** - CORS support
- **Requests 2.32.5** - HTTP client

### Production
- **Gunicorn 23.0.0** - WSGI HTTP Server
- **Render.com** - Cloud platform (PaaS)

### API Integration
- **Replicate API** - AI model hosting platform

### DevOps
- **Git** - Version control
- **GitHub** - Repository hosting
- **Render** - Automatic deployment
- **Cron-job.org** - Keep-alive service (optional)

---

## 📦 Kurulum

### 1️⃣ Repository'yi Clone Edin

```bash
git clone https://github.com/ernklyc/api_panel.git
cd api_panel
```

### 2️⃣ Virtual Environment Oluşturun (Opsiyonel)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3️⃣ Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 4️⃣ API Key'i Ayarlayın

```bash
python initialize_api_keys.py
```

Replicate API key'inizi girin (ücretsiz: [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens))

### 5️⃣ Sunucuyu Başlatın

```bash
# Windows
start_server.bat

# Linux/Mac
python api_key_manager.py
```

✅ Server: `http://localhost:8000`

---

## 🎮 Kullanım

### Health Check

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "ok",
  "service": "API Key Manager",
  "version": "1.0.0"
}
```

### Replicate Proxy - Flutter Örneği

```dart
const String apiBaseUrl = 'http://localhost:8000'; // or your production URL

Future<String> generateImage(String prompt) async {
  // 1. Prediction oluştur
  final response = await http.post(
    Uri.parse('$apiBaseUrl/api/v1/proxy/replicate/google/nano-banana'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'input': {'prompt': prompt}
    }),
  );

  if (response.statusCode == 201) {
    final data = jsonDecode(response.body);
    final predictionId = data['data']['id'];
    
    // 2. Polling ile sonucu bekle
    while (true) {
      await Future.delayed(Duration(seconds: 2));
      
      final statusResponse = await http.get(
        Uri.parse('$apiBaseUrl/api/v1/proxy/replicate/prediction/$predictionId'),
      );
      
      final statusData = jsonDecode(statusResponse.body);
      final status = statusData['data']['status'];
      
      if (status == 'succeeded') {
        return statusData['data']['output'][0]; // Image URL
      } else if (status == 'failed') {
        throw Exception('Generation failed');
      }
    }
  }
  
  throw Exception('Failed to create prediction');
}
```

---

## 📡 API Endpoints

### Public Endpoints

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| `GET` | `/` | API bilgileri ve endpoint listesi |
| `GET` | `/health` | Health check |
| `GET` | `/api/v1/keys` | API keys listesi (preview only) |

### 🔒 Secure Proxy Endpoints (Flutter için)

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| `POST` | `/api/v1/proxy/replicate` | Replicate prediction oluştur (version ile) |
| `POST` | `/api/v1/proxy/replicate/<model_name>` | Replicate prediction oluştur (model ile) |
| `GET` | `/api/v1/proxy/replicate/prediction/<id>` | Prediction durumu sorgula |

#### POST /api/v1/proxy/replicate/<model_name>

**Request:**
```json
{
  "input": {
    "prompt": "a beautiful sunset",
    "aspect_ratio": "1:1"
  }
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "xxxxx-prediction-id",
    "status": "starting",
    "urls": {
      "get": "https://api.replicate.com/v1/predictions/xxxxx",
      "cancel": "https://api.replicate.com/v1/predictions/xxxxx/cancel"
    }
  }
}
```

#### GET /api/v1/proxy/replicate/prediction/<id>

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "xxxxx-prediction-id",
    "status": "succeeded",
    "output": ["https://replicate.delivery/xxxxx.png"]
  }
}
```

---

## 🚀 Deployment (Render.com)

### Otomatik Deployment

1. **GitHub'a Push Edin:**
   ```bash
   git push origin main
   ```

2. **Render Dashboard:**
   - [render.com](https://render.com) → Sign Up
   - **New + → Web Service**
   - Repository'nizi seçin (`ernklyc/api_panel`)

3. **Ayarlar** (otomatik doldurulur):
   - **Name:** `api-panel`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn api_key_manager:app`

4. **Environment Variables:**
   ```
   REPLICATE_API_KEY = your_replicate_api_token_here
   ```

5. **Deploy!**
   - 2-3 dakika içinde hazır
   - URL: `https://your-app.onrender.com`

### Keep-Alive (Sleep Mode Önleme)

Render Free Tier, 15 dakika inaktivite sonrası sleep mode'a girer. Bunu önlemek için:

**[cron-job.org](https://cron-job.org) ile:**
- **URL:** `https://your-app.onrender.com/health`
- **Schedule:** Her 10 dakika (`*/10 * * * *`)
- ✅ Ücretsiz ve basit

**Detaylı rehber:** [`RENDER_DEPLOYMENT.md`](RENDER_DEPLOYMENT.md)

---

## 🔐 Güvenlik

### ✅ Best Practices

1. **API keys asla Git'e commit edilmez:**
   - `.gitignore` ile `api_keys.json` korunur
   - Production'da environment variable kullanılır

2. **Hybrid API Key Loading:**
   ```python
   # Production: Environment variable
   api_key = os.environ.get('REPLICATE_API_KEY')
   
   # Development: Local JSON (fallback)
   if not api_key:
       keys = load_api_keys()
       api_key = keys['replicate_api']['key']
   ```

3. **CORS Configuration:**
   - Flutter/mobile apps için yapılandırılmış
   - Production'da domain restriction eklenebilir

4. **API Key Exposure:**
   - ❌ Keys **asla** client'a gönderilmez
   - ✅ Deprecated endpoint'ler devre dışı
   - ✅ Sadece proxy üzerinden erişim

### 🔍 Security Checklist

- [x] `api_keys.json` → `.gitignore`
- [x] Environment variables for production
- [x] No hardcoded secrets in code
- [x] CORS configured
- [x] HTTPS in production (Render otomatik)
- [x] API key never sent to client

---

## 📚 Dokümantasyon

| Dosya | Açıklama |
|-------|----------|
| [`RENDER_DEPLOYMENT.md`](RENDER_DEPLOYMENT.md) | 🚀 Detaylı Render deployment rehberi |
| [`FLUTTER_INTEGRATION.md`](FLUTTER_INTEGRATION.md) | 📱 Flutter entegrasyon kılavuzu |
| [`SECURITY_UPDATE.md`](SECURITY_UPDATE.md) | 🔒 Güvenlik güncellemeleri |
| [`QUICK_START.md`](QUICK_START.md) | ⚡ Hızlı başlangıç rehberi |
| [`DEPLOYMENT_READY.md`](DEPLOYMENT_READY.md) | ✅ Deployment kontrol listesi |

---

## 🧪 Test

### Otomatik Test

```bash
python test_proxy.py
```

### Manuel Test

```bash
# Health check
curl http://localhost:8000/health

# Proxy test
curl -X POST http://localhost:8000/api/v1/proxy/replicate/google/nano-banana \
  -H "Content-Type: application/json" \
  -d '{"input": {"prompt": "test"}}'
```

---

## 🌟 Özellikler ve Avantajlar

| Özellik | Local Development | Production (Render) |
|---------|-------------------|---------------------|
| **API Key Storage** | `api_keys.json` | Environment Variable |
| **Server** | Flask Development | Gunicorn |
| **Port** | 8000 | Dynamic (Render assigns) |
| **HTTPS** | ❌ HTTP | ✅ HTTPS (otomatik) |
| **Auto Deploy** | ❌ Manual | ✅ Git push triggers |
| **Cost** | Free | Free (750 hrs/month) |
| **Uptime** | Manual | 24/7 (with cron-job) |

---

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

---

## 📝 License

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [`LICENSE`](LICENSE) dosyasına bakın.

---

## 👤 Yazar

**ernklyc**

- GitHub: [@ernklyc](https://github.com/ernklyc)
- Repository: [api_panel](https://github.com/ernklyc/api_panel)

---

## 🙏 Teşekkürler

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Replicate](https://replicate.com/) - AI model hosting
- [Render](https://render.com/) - Cloud platform
- [cron-job.org](https://cron-job.org/) - Free cron service

---

## 📞 Destek

Sorularınız için:
- 🐛 **Issues:** [GitHub Issues](https://github.com/ernklyc/api_panel/issues)
- 📖 **Docs:** Yukarıdaki dokümantasyon dosyalarına bakın
- 💬 **Discussions:** [GitHub Discussions](https://github.com/ernklyc/api_panel/discussions)

---

<div align="center">

**⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! ⭐**

Made with ❤️ by [ernklyc](https://github.com/ernklyc)

</div>

```bash
# Windows
start_server.bat

# Linux/Mac
python api_key_manager.py
```

✅ Server: `http://localhost:8000`

---

## 🎮 Kullanım

### Health Check

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "ok",
  "service": "API Key Manager",
  "version": "1.0.0"
}
```

### Replicate Proxy (Flutter için)

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

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
