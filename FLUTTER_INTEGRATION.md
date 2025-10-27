# 🔒 Güvenli API Key Manager - Flutter Entegrasyonu

## ✅ Ne Değişti?

### Güvenlik İyileştirmeleri
1. **API Anahtarları Artık İstemciye Gönderilmiyor**
   - `GET /api/v1/keys/<name>` artık sadece önizleme (ilk 10 karakter) döndürür
   - `POST /api/v1/keys/<name>/use` endpoint'i devre dışı bırakıldı (403 döner)
   
2. **Yeni Güvenli Proxy Endpoint'ler**
   - `POST /api/v1/proxy/replicate` - Replicate prediction oluştur
   - `GET /api/v1/proxy/replicate/<prediction_id>` - Prediction durumu sorgula
   
3. **Git Güvenliği**
   - `.gitignore` dosyası eklendi
   - `api_keys.json` ve `initialize_api_keys.py` artık git'e gönderilmeyecek

## 🎯 Nasıl Çalışır?

### Eski Yöntem (GÜVENSİZ ❌)
```
Flutter App → /api/v1/keys/replicate_api → API Key alır → Replicate'e direkt istek
```
**Sorun:** API anahtarı istemciye açığa çıkar, decompile ile çalınabilir.

### Yeni Yöntem (GÜVENLİ ✅)
```
Flutter App → /api/v1/proxy/replicate → Sunucu Replicate'e istek → Sonuç Flutter'a döner
```
**Çözüm:** API anahtarı sadece sunucuda kalır, istemci hiç görmez.

---

## 📱 Flutter Entegrasyonu

### 1. Paketi Ekle
```yaml
# pubspec.yaml
dependencies:
  http: ^1.1.0
```

### 2. API Service Sınıfı

```dart
// lib/services/replicate_service.dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ReplicateService {
  // Sunucunuzun adresi (production'da değiştirin)
  static const String baseUrl = 'http://your-server-ip:8000';
  
  /// Replicate prediction oluştur
  /// 
  /// [modelVersion] - Replicate model version ID
  /// [input] - Model input parametreleri
  Future<Map<String, dynamic>> createPrediction({
    required String modelVersion,
    required Map<String, dynamic> input,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/v1/proxy/replicate'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'version': modelVersion,
          'input': input,
        }),
      );
      
      if (response.statusCode == 200 || response.statusCode == 201) {
        final data = jsonDecode(response.body);
        return data['data']; // Replicate API yanıtı
      } else {
        throw Exception('Prediction oluşturulamadı: ${response.body}');
      }
    } catch (e) {
      throw Exception('API hatası: $e');
    }
  }
  
  /// Prediction durumunu kontrol et
  /// 
  /// [predictionId] - Prediction ID (createPrediction'dan dönen)
  Future<Map<String, dynamic>> getPredictionStatus(String predictionId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/v1/proxy/replicate/$predictionId'),
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['data']; // Replicate API yanıtı
      } else {
        throw Exception('Durum sorgulanamadı: ${response.body}');
      }
    } catch (e) {
      throw Exception('API hatası: $e');
    }
  }
  
  /// Prediction tamamlanana kadar bekle (polling)
  /// 
  /// [predictionId] - Prediction ID
  /// [onUpdate] - Her kontrol sonrası çağrılır (opsiyonel)
  /// [maxAttempts] - Maksimum deneme sayısı (varsayılan: 60)
  /// [interval] - Kontrol aralığı saniye (varsayılan: 2)
  Future<Map<String, dynamic>> waitForPrediction(
    String predictionId, {
    Function(String status)? onUpdate,
    int maxAttempts = 60,
    int interval = 2,
  }) async {
    for (int i = 0; i < maxAttempts; i++) {
      final result = await getPredictionStatus(predictionId);
      final status = result['status'] as String;
      
      onUpdate?.call(status);
      
      if (status == 'succeeded') {
        return result;
      } else if (status == 'failed' || status == 'canceled') {
        throw Exception('Prediction başarısız: $status');
      }
      
      // Bekle ve tekrar dene
      await Future.delayed(Duration(seconds: interval));
    }
    
    throw Exception('Timeout: Prediction çok uzun sürdü');
  }
}
```

### 3. Kullanım Örneği

```dart
// lib/screens/image_generation_screen.dart
import 'package:flutter/material.dart';
import '../services/replicate_service.dart';

class ImageGenerationScreen extends StatefulWidget {
  @override
  _ImageGenerationScreenState createState() => _ImageGenerationScreenState();
}

class _ImageGenerationScreenState extends State<ImageGenerationScreen> {
  final _service = ReplicateService();
  final _promptController = TextEditingController();
  
  String _status = 'Hazır';
  String? _imageUrl;
  bool _isLoading = false;

  Future<void> _generateImage() async {
    if (_promptController.text.isEmpty) return;
    
    setState(() {
      _isLoading = true;
      _status = 'Prediction oluşturuluyor...';
      _imageUrl = null;
    });

    try {
      // 1. Prediction oluştur
      final prediction = await _service.createPrediction(
        modelVersion: 'stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b',
        input: {
          'prompt': _promptController.text,
          'num_outputs': 1,
        },
      );
      
      final predictionId = prediction['id'];
      setState(() => _status = 'İşleniyor... (ID: $predictionId)');
      
      // 2. Tamamlanana kadar bekle
      final result = await _service.waitForPrediction(
        predictionId,
        onUpdate: (status) {
          setState(() => _status = 'Durum: $status');
        },
      );
      
      // 3. Sonucu göster
      final output = result['output'];
      if (output is List && output.isNotEmpty) {
        setState(() {
          _imageUrl = output[0];
          _status = 'Tamamlandı!';
        });
      }
      
    } catch (e) {
      setState(() => _status = 'Hata: $e');
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('AI Görsel Üretici')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _promptController,
              decoration: InputDecoration(
                labelText: 'Prompt',
                hintText: 'Örn: a photo of a person',
              ),
            ),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: _isLoading ? null : _generateImage,
              child: Text(_isLoading ? 'İşleniyor...' : 'Görsel Üret'),
            ),
            SizedBox(height: 16),
            Text(_status, style: TextStyle(fontWeight: FontWeight.bold)),
            SizedBox(height: 16),
            if (_imageUrl != null)
              Expanded(
                child: Image.network(_imageUrl!, fit: BoxFit.contain),
              ),
          ],
        ),
      ),
    );
  }
}
```

---

## 🖥️ Sunucu Kurulumu

### 1. Sunucuyu Başlat
```bash
python api_key_manager.py
```

### 2. Yerel Test
```bash
python test_proxy.py
```

### 3. Production İçin
- HTTPS kullanın (Let's Encrypt veya cloud provider sertifikası)
- Firewall kuralları ekleyin (sadece gerekli portlar)
- Rate limiting ekleyin (örn: Flask-Limiter)
- Monitoring ve logging ekleyin

---

## 🔐 Güvenlik Notları

### ✅ YAPILDI
- ✅ API anahtarı istemciye gönderilmiyor
- ✅ Proxy pattern ile güvenli erişim
- ✅ `.gitignore` ile key dosyaları korunuyor
- ✅ Eski endpoint'ler devre dışı

### ⚠️ ÖNERİLER
1. **HTTPS Kullanın**
   - HTTP yerine HTTPS kullanarak tüm trafiği şifreleyin
   - Ücretsiz: Let's Encrypt sertifikası

2. **Kimlik Doğrulama Ekleyin**
   - JWT token veya API key ile Flutter app'i doğrulayın
   - Böylece sadece uygulamanız sunucuyu kullanabilir

3. **Rate Limiting**
   - Her kullanıcı/IP için istek limiti koyun
   - DDoS ve abuse koruması

4. **Monitoring**
   - Sunucu loglarını takip edin
   - Anormal kullanım tespit edin

5. **API Key Rotation**
   - Replicate API key'inizi düzenli aralıklarla değiştirin
   - Eski anahtarı iptal edin

6. **Environment Variables**
   - Production'da anahtarları environment variable'dan okuyun
   - `api_keys.json` yerine sistemin secret manager'ını kullanın

---

## 📊 Test Sonuçları

```
✅ Sunucu sağlık kontrolü - Başarılı
✅ Key endpoint güvenlik testi - Sadece preview döndürüyor
✅ Deprecated endpoint testi - Devre dışı (403)
✅ Proxy endpoint varlık kontrolü - Çalışıyor
✅ Gerçek Replicate API testi - Başarılı
```

---

## 🚀 Hızlı Başlangıç

1. **Sunucu çalışıyor mu kontrol et:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Flutter'da ReplicateService'i kullan:**
   ```dart
   final service = ReplicateService();
   final prediction = await service.createPrediction(
     modelVersion: 'your-model-version',
     input: {'prompt': 'test'},
   );
   ```

3. **Test scriptini çalıştır:**
   ```bash
   python test_proxy.py
   ```

---

## ❓ Sık Sorulan Sorular

**S: API anahtarım güvende mi?**  
C: Evet! Anahtar sadece sunucuda kalır, Flutter uygulamanız hiç görmez.

**S: Replicate limitleri nasıl yönetilir?**  
C: Sunucu tarafında rate limiting ekleyebilir veya Replicate dashboard'dan takip edebilirsiniz.

**S: Production'a nasıl deploy ederim?**  
C: Heroku, AWS, DigitalOcean, veya başka bir cloud provider kullanabilirsiniz. HTTPS şart!

**S: Flutter web ile çalışır mı?**  
C: Evet, aynı HTTP kütüphanesi çalışır. CORS zaten aktif.

---

## 📞 Destek

Sorunlarınız için:
1. `python test_proxy.py` çalıştırıp testleri kontrol edin
2. Sunucu loglarını inceleyin
3. Replicate API durumunu kontrol edin: https://replicate.com/status

**Başarılar! 🎉**
