# 🚀 RENDER'A DEPLOYMENT REHBERİ

Bu projeyi ücretsiz olarak Render'a deploy etmek için adım adım talimatlar.

## ✅ Ön Hazırlık (TAMAMLANDI)

Aşağıdaki değişiklikler zaten yapıldı:

1. ✅ `requirements.txt` dosyasına `gunicorn` eklendi
2. ✅ `api_key_manager.py` dosyası environment variable kullanacak şekilde güncellendi
3. ✅ `Procfile` dosyası oluşturuldu
4. ✅ `render.yaml` dosyası oluşturuldu
5. ✅ `.gitignore` dosyası zaten mevcut ve doğru yapılandırılmış

## 📦 Adım 1: GitHub'a Yükleme

### 1.1 Git Initialize (Eğer henüz yapmadıysanız)

```powershell
git init
git add .
git commit -m "Initial commit - Ready for Render deployment"
```

### 1.2 GitHub Repository Oluşturma

1. [GitHub](https://github.com) üzerinde oturum açın
2. Sağ üst köşeden **"+"** → **"New repository"** seçin
3. Repository ayarları:
   - **Repository name**: `api-panel` (veya istediğiniz isim)
   - **Visibility**: **Private** ⚠️ (GÜVENLİK ZORUNLU!)
   - **Initialize this repository with**: Hiçbir şey seçmeyin
   - **Create repository** butonuna tıklayın

### 1.3 GitHub'a Push

GitHub'ın gösterdiği komutları kullanın (örnek):

```powershell
git remote add origin https://github.com/KULLANICI_ADINIZ/api-panel.git
git branch -M main
git push -u origin main
```

**⚠️ ÖNEMLİ KONTROL**: Push'tan önce mutlaka `api_keys.json` ve `initialize_api_keys.py` dosyalarının GitHub'a GİTMEDİĞİNDEN emin olun!

```powershell
git status
```

Bu dosyalar listede görünmemeli.

---

## 🌐 Adım 2: Render'a Deployment

### 2.1 Render Hesabı

1. [Render](https://render.com) adresine gidin
2. **"Get Started for Free"** veya **"Sign Up"** butonuna tıklayın
3. GitHub hesabınızla giriş yapın (önerilen)

### 2.2 Web Service Oluşturma

1. Render Dashboard'da **"New +"** butonuna tıklayın
2. **"Web Service"** seçin
3. **"Build and deploy from a Git repository"** → **"Next"**
4. GitHub repository'nizi seçin:
   - Eğer görünmüyorsa **"Configure account"** ile erişim verin
   - Private repository'nizi listeden seçin

### 2.3 Service Ayarları

Aşağıdaki ayarları yapın:

| Alan | Değer |
|------|-------|
| **Name** | `api-key-manager` (veya istediğiniz isim) |
| **Region** | `Frankfurt (EU Central)` (veya size yakın olan) |
| **Branch** | `main` |
| **Root Directory** | (boş bırakın) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn api_key_manager:app` |
| **Instance Type** | `Free` ✅ |

### 2.4 Environment Variables (EN ÖNEMLİ ADIM! 🔐)

**"Environment"** bölümünde:

1. **"Add Environment Variable"** butonuna tıklayın
2. Aşağıdaki değişkeni ekleyin:

```
Key: REPLICATE_API_KEY
Value: r8_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

⚠️ **Value** kısmına GERÇEK Replicate API anahtarınızı yapıştırın!

Replicate API anahtarınızı [https://replicate.com/account/api-tokens](https://replicate.com/account/api-tokens) adresinden alabilirsiniz.

### 2.5 Deploy

1. **"Create Web Service"** butonuna tıklayın
2. Render otomatik olarak deploy işlemine başlayacak
3. Build loglarını izleyin (2-3 dakika sürer)

### 2.6 Deploy Tamamlandı ✅

Deploy başarılı olduğunda:

1. URL'nizi görürsünüz (örnek): `https://api-key-manager-xxxx.onrender.com`
2. **"Logs"** sekmesinden sunucunun çalıştığını doğrulayın
3. Tarayıcıda test edin:

```
https://your-app-name.onrender.com/health
```

Şu yanıtı görmelisiniz:

```json
{
  "status": "ok",
  "service": "API Key Manager",
  "version": "1.0.0"
}
```

---

## 🧪 Adım 3: Test Etme

### 3.1 Health Check Test

```bash
curl https://your-app-name.onrender.com/health
```

### 3.2 Replicate Proxy Test (Postman veya cURL)

```bash
curl -X POST https://your-app-name.onrender.com/api/v1/proxy/replicate \
  -H "Content-Type: application/json" \
  -d '{
    "version": "xxxxx-model-version-id",
    "input": {
      "prompt": "a beautiful sunset"
    }
  }'
```

---

## 📱 Adım 4: Flutter Uygulamasını Güncelleme

Flutter uygulamanızdaki API base URL'i değiştirin:

### ESKİ KOD:
```dart
const String apiBaseUrl = 'http://localhost:8000';
```

### YENİ KOD:
```dart
const String apiBaseUrl = 'https://your-app-name.onrender.com';
```

**DİKKAT**: `http` değil, `https` kullanın!

---

## ⚙️ Adım 5: Render Ayarları ve İpuçları

### Otomatik Deploy (Önerilen)

Render, varsayılan olarak GitHub'daki her push'ta otomatik deploy yapar. Bunu kapatmak için:

1. Render Dashboard → Service Settings
2. **"Auto-Deploy"** → **"No"** seçin

### Free Plan Sınırlamaları

Render Free Plan:

- ✅ 750 saat/ay ücretsiz (tek service için yeterli)
- ⚠️ 15 dakika işlem yapılmazsa "sleep" moduna girer
- ⚠️ İlk istekte 30-60 saniye gecikme olabilir (cold start)
- ✅ HTTPS otomatik aktif
- ✅ Otomatik SSL sertifikası

### Sleep Mode Sorunu Çözümü (Opsiyonel)

Eğer uygulamanızın 7/24 aktif kalmasını istiyorsanız:

**Seçenek 1**: Paid plan'e geçin ($7/ay)

**Seçenek 2**: Cron-job ile 10 dakikada bir ping atın:
- [cron-job.org](https://cron-job.org) veya [UptimeRobot](https://uptimerobot.com) kullanın
- Her 10 dakikada bir `/health` endpoint'ine istek attırın

---

## 🔐 Güvenlik Kontrol Listesi

Deployment'tan önce kontrol edin:

- [ ] `api_keys.json` dosyası `.gitignore` içinde ve GitHub'da YOK
- [ ] `initialize_api_keys.py` dosyası `.gitignore` içinde ve GitHub'da YOK
- [ ] GitHub repository **PRIVATE** olarak ayarlandı
- [ ] Render'da `REPLICATE_API_KEY` environment variable doğru ayarlandı
- [ ] Flutter uygulaması HTTPS kullanıyor
- [ ] Local bilgisayarınızdaki `api_keys.json` dosyası güvende (yedeğini alın)

---

## 🐛 Sorun Giderme

### "Application Error" hatası alıyorum

**Çözüm**: Render Dashboard → Logs sekmesinden hata detaylarını kontrol edin.

Muhtemel nedenler:
1. `REPLICATE_API_KEY` environment variable eksik veya yanlış
2. `requirements.txt` dosyasında eksik paket
3. Port ayarı sorunu (Render otomatik PORT atar, değiştirmeyin)

### "API key not configured on server" hatası

**Çözüm**:
1. Render Dashboard → Environment sekmesindehttp://localhost:8000 `REPLICATE_API_KEY` ekli mi kontrol edin
2. Environment variable ekledikten sonra **"Manual Deploy" → "Clear build cache & deploy"** yapın

### Replicate API'den "Invalid Token" hatası

**Çözüm**:
1. [Replicate API Tokens](https://replicate.com/account/api-tokens) sayfasından yeni token oluşturun
2. Render'da environment variable'ı güncelleyin
3. Manual deploy yapın

### Cold Start çok yavaş

**Normal**: Render Free Plan'da ilk istek 30-60 saniye sürebilir.

**Çözümler**:
- Paid plan kullanın
- Cron-job ile düzenli ping atın (yukarıda açıklandı)

---

## 📞 Destek

Sorun yaşarsanız:

1. Render Logs'u kontrol edin
2. `FLUTTER_INTEGRATION.md` dosyasını tekrar okuyun
3. [Render Documentation](https://render.com/docs) bakın

---

## ✅ Sonuç

Başarıyla deploy ettiyseniz:

✅ Projeniz ücretsiz ve güvenli bir şekilde yayında  
✅ API anahtarınız sunucuda gizli  
✅ Flutter uygulamanız https://your-app-name.onrender.com adresine istek atabilir  
✅ GitHub repository'niz private ve güvenli

**Tebrikler! 🎉**
