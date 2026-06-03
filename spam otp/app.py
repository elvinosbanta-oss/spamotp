from flask import Flask, render_template, request, jsonify
import time
from datetime import datetime
from utils.spam_sender import SpamSender
import config

app = Flask(__name__)
app.secret_key = 'spam-tools-for-own-number-only'

# History sederhana
spam_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/send-spam', methods=['POST'])
def send_spam():
    data = request.get_json()
    phone = data.get('phone', '').strip()
    
    # Validasi nomor
    if not phone:
        return jsonify({'success': False, 'message': 'Nomor telepon wajib diisi'}), 400
    
    # Clean phone number
    phone = phone.replace('+', '').replace(' ', '').replace('-', '')
    
    # Validasi format (harus angka)
    if not phone.isdigit():
        return jsonify({'success': False, 'message': 'Nomor telepon hanya boleh berisi angka'}), 400
    
    # Validasi panjang
    if len(phone) < 9 or len(phone) > 15:
        return jsonify({'success': False, 'message': 'Panjang nomor telepon 9-15 digit'}), 400
    
    # Kirim spam
    try:
        sender = SpamSender(phone)
        results = sender.send_all()
        
        success_count = sum(1 for r in results if r.get('success', False))
        
        # Simpan ke history
        history_entry = {
            'phone': phone,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'success_count': success_count,
            'total': len(results)
        }
        spam_history.insert(0, history_entry)
        if len(spam_history) > 10:
            spam_history.pop()
        
        return jsonify({
            'success': True,
            'message': f'Pengiriman selesai: {success_count}/{len(results)} berhasil',
            'results': results,
            'phone': phone,
            'success_count': success_count,
            'total': len(results),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500

@app.route('/api/history')
def get_history():
    return jsonify({'history': spam_history})

if __name__ == '__main__':
    print("=" * 60)
    print("⚠️  PERINGATAN ⚠️")
    print("=" * 60)
    print("Tools ini HANYA untuk nomor ANDA sendiri!")
    print(f"Mode: {'DEBUG (Simulasi)' if config.DEBUG_MODE else 'LIVE (Mengirim Real)'}")
    print("=" * 60)
    print(f"\n🌐 Web: http://localhost:5000")
    print("📱 Gunakan hanya untuk nomor sendiri!")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)