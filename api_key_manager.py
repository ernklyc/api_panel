"""
Movie Face AI - API Key Manager
Güvenli API key yönetimi için Flask API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
import requests

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max
CORS(app)

API_KEY_FILE = 'api_keys.json'

def load_api_keys():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_api_keys(keys):
    with open(API_KEY_FILE, 'w', encoding='utf-8') as f:
        json.dump(keys, f, indent=2, ensure_ascii=False)

@app.route('/api/v1/keys', methods=['GET'])
def get_keys():
    keys = load_api_keys()
    safe_keys = {
        name: {
            'platform': info.get('platform', 'Unknown'),
            'created': info.get('created', 'Unknown'),
            'last_used': info.get('last_used', 'Never'),
            'key_preview': info['key'][:10] + '...' if 'key' in info else 'N/A'
        }
        for name, info in keys.items()
    }
    return jsonify({'success': True, 'keys': safe_keys, 'count': len(keys)})

@app.route('/api/v1/keys/<key_name>', methods=['GET'])
def get_key(key_name):
    """
    ⚠️ GÜVENLİK: Bu endpoint artık tam anahtarı döndürmez.
    Sadece meta bilgi döndürür. Anahtarı kullanmak için /api/v1/proxy/* endpoint'lerini kullanın.
    """
    keys = load_api_keys()
    if key_name not in keys:
        return jsonify({'success': False, 'error': 'Key not found'}), 404
    
    info = keys[key_name]
    return jsonify({
        'success': True,
        'key_preview': info['key'][:10] + '...' if 'key' in info else 'N/A',
        'platform': info.get('platform', 'Unknown'),
        'created': info.get('created', 'Unknown'),
        'last_used': info.get('last_used', 'Never'),
        'note': 'Use /api/v1/proxy/replicate to make requests securely'
    })

@app.route('/api/v1/keys', methods=['POST'])
def add_key():
    data = request.json
    key_name = data.get('name')
    key_value = data.get('key')
    platform = data.get('platform', 'Unknown')
    
    if not key_name or not key_value:
        return jsonify({'success': False, 'error': 'Name and key are required'}), 400
    
    keys = load_api_keys()
    
    if key_name in keys:
        return jsonify({'success': False, 'error': 'Key name already exists'}), 400
    
    keys[key_name] = {
        'key': key_value,
        'platform': platform,
        'created': datetime.now().isoformat(),
        'last_used': 'Never'
    }
    
    save_api_keys(keys)
    
    return jsonify({
        'success': True,
        'message': 'Key added successfully',
        'key_name': key_name
    })

@app.route('/api/v1/keys/<key_name>', methods=['PUT'])
def update_key(key_name):
    data = request.json
    keys = load_api_keys()
    
    if key_name not in keys:
        return jsonify({'success': False, 'error': 'Key not found'}), 404
    
    if 'key' in data:
        keys[key_name]['key'] = data['key']
    if 'platform' in data:
        keys[key_name]['platform'] = data['platform']
    
    save_api_keys(keys)
    
    return jsonify({'success': True, 'message': 'Key updated successfully'})

@app.route('/api/v1/keys/<key_name>', methods=['DELETE'])
def delete_key(key_name):
    keys = load_api_keys()
    
    if key_name not in keys:
        return jsonify({'success': False, 'error': 'Key not found'}), 404
    
    del keys[key_name]
    save_api_keys(keys)
    
    return jsonify({'success': True, 'message': 'Key deleted successfully'})

@app.route('/api/v1/keys/<key_name>/use', methods=['POST'])
def use_key(key_name):
    """
    ⚠️ DEPRECATED: Bu endpoint artık anahtarı döndürmez.
    Anahtarı kullanmak için /api/v1/proxy/* endpoint'lerini kullanın.
    """
    keys = load_api_keys()
    
    if key_name not in keys:
        return jsonify({'success': False, 'error': 'Key not found'}), 404
    
    keys[key_name]['last_used'] = datetime.now().isoformat()
    save_api_keys(keys)
    
    return jsonify({
        'success': False,
        'error': 'This endpoint is deprecated for security reasons',
        'message': 'Use /api/v1/proxy/replicate instead'
    }), 403

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'service': 'API Key Manager',
        'version': '1.0.0'
    })

@app.route('/api/v1/proxy/replicate/<path:model_name>', methods=['POST'])
@app.route('/api/v1/proxy/replicate', methods=['POST'])
def proxy_replicate(model_name=None):
    """
    🔒 GÜVENLİ PROXY ENDPOINT
    Flutter uygulaması bu endpoint'e istek atar.
    Sunucu Replicate'e çağrı yapar ve sonucu döndürür.
    API key hiçbir zaman istemciye gönderilmez.
    
    URL'de model adı varsa kullan: /api/v1/proxy/replicate/google/nano-banana
    Body: { "input": { "prompt": "..." } }
    
    Veya eski format: Body: { "version": "...", "input": {...} }
    """
    try:
        print(f"\n🔔 Proxy isteği geldi: {request.method} {request.path}")
        print(f"📦 Model adı: {model_name or 'yok (version kullanılıyor)'}")
        
        # API anahtarını yükle
        keys = load_api_keys()
        if 'replicate_api' not in keys:
            print("❌ Replicate API key bulunamadı!")
            return jsonify({
                'success': False,
                'error': 'Replicate API key not configured'
            }), 500
        
        api_key = keys['replicate_api']['key']
        print(f"✅ API key bulundu: {api_key[:10]}...")
        
        # İstek verisini al
        data = request.json
        if not data:
            print("❌ Request body boş!")
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        print(f"📝 Request data keys: {list(data.keys())}")
        
        # Replicate API'ye istek yap
        headers = {
            'Authorization': f'Token {api_key}',
            'Content-Type': 'application/json'
        }
        
        # URL'de model adı varsa (lib2 formatı)
        if model_name:
            print(f"📤 Model adı URL'de: {model_name}")
            # Replicate Predictions API - Model URL formatı
            replicate_url = f'https://api.replicate.com/v1/models/{model_name}/predictions'
            response = requests.post(replicate_url, json=data, headers=headers, timeout=30)
        else:
            # Eski format: version field ile
            print(f"📤 Version field ile gönderiliyor: {data.get('version')}")
            replicate_url = 'https://api.replicate.com/v1/predictions'
            response = requests.post(replicate_url, json=data, headers=headers, timeout=30)
        
        print(f"📥 Replicate'den yanıt: {response.status_code}")
        
        if response.status_code == 201:
            response_data = response.json()
            print(f"✅ Prediction oluşturuldu: {response_data.get('id')}")
        else:
            print(f"❌ Replicate hatası: {response.text}")
        
        # Son kullanım zamanını güncelle
        keys['replicate_api']['last_used'] = datetime.now().isoformat()
        save_api_keys(keys)
        
        # Yanıtı döndür
        return jsonify({
            'success': True,
            'data': response.json(),
            'status_code': response.status_code
        }), response.status_code
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Replicate API hatası: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Replicate API error: {str(e)}'
        }), 500
    except Exception as e:
        print(f"❌ Server hatası: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/v1/proxy/replicate/prediction/<prediction_id>', methods=['GET'])
def get_replicate_prediction(prediction_id):
    """
    🔒 GÜVENLİ PROXY ENDPOINT - Prediction durumu sorgulama
    Flutter uygulaması bu endpoint'le Replicate prediction'ın durumunu kontrol eder.
    
    Örnek Flutter isteği:
    GET http://your-server:8000/api/v1/proxy/replicate/xxxxxx-prediction-id
    """
    try:
        # API anahtarını yükle
        keys = load_api_keys()
        if 'replicate_api' not in keys:
            return jsonify({
                'success': False,
                'error': 'Replicate API key not configured'
            }), 500
        
        api_key = keys['replicate_api']['key']
        
        # Replicate API'den prediction durumunu al
        headers = {
            'Authorization': f'Token {api_key}',
            'Content-Type': 'application/json'
        }
        
        replicate_url = f'https://api.replicate.com/v1/predictions/{prediction_id}'
        response = requests.get(replicate_url, headers=headers, timeout=30)
        
        # Yanıtı döndür
        return jsonify({
            'success': True,
            'data': response.json(),
            'status_code': response.status_code
        }), response.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'Replicate API error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🔐 Movie Face AI - API Key Manager")
    print("=" * 60)
    print("📡 Server: http://0.0.0.0:8000")
    print("📚 Endpoints:")
    print("   GET    /api/v1/keys           - List all keys (preview only)")
    print("   GET    /api/v1/keys/<name>    - Get key info (preview only)")
    print("   POST   /api/v1/keys            - Add new key")
    print("   PUT    /api/v1/keys/<name>     - Update key")
    print("   DELETE /api/v1/keys/<name>     - Delete key")
    print("   GET    /health                 - Health check")
    print("")
    print("🔒 GÜVENLI PROXY ENDPOINTS (Flutter için):")
    print("   POST   /api/v1/proxy/replicate              - Replicate prediction oluştur")
    print("   GET    /api/v1/proxy/replicate/<pred_id>    - Prediction durumu sorgula")
    print("=" * 60)
    print("✅ Server başlatıldı! Backend çalışıyor.")
    print("⚠️  Ctrl+C ile durdurun")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=8000, debug=False)
