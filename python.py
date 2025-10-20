from flask import Flask, jsonify, session, request, render_template_string
import secrets
import hashlib
import base64
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your-super-secret-key-here'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Хранилище сессий (в продакшене используйте Redis или БД)
sessions = {}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>My TON dApp</title>
    <script src="https://unpkg.com/@tonconnect/ui@latest/dist/tonconnect-ui.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        button { background: #0088cc; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 16px; }
        button:hover { background: #0066aa; }
        .wallet-info { background: #f5f5f5; padding: 15px; border-radius: 8px; margin: 20px 0; }
        .transaction { background: #e8f4fd; padding: 15px; border-radius: 8px; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>🚀 My TON dApp</h1>
    
    <div id="connection-status">
        <button onclick="connectWallet()" id="connect-btn">Connect Wallet</button>
    </div>

    <script>
        let connector;
        let connectedWallet = null;

        function initTonConnect() {
            connector = new TonConnectUI({
                manifestUrl: '{{ manifest_url }}',
                buttonRootId: 'connection-status'
            });

            // Проверяем, есть ли уже подключенный кошелек
            connector.connectionRestored.then(() => {
                if (connector.connected) {
                    onWalletConnected(connector.wallet);
                }
            });
        }

        async function connectWallet() {
            try {
                const response = await fetch('/generate-payload');
                const data = await response.json();
                
                // Подключаем кошелек с полученным пейлоадом
                await connector.connect({
                    jsBridgeKey: data.js_bridge_key,
                    payload: data.payload
                });
            } catch (error) {
                console.error('Connection error:', error);
                alert('Connection failed: ' + error.message);
            }
        }

        function onWalletConnected(walletInfo) {
            connectedWallet = walletInfo;
            document.getElementById('connection-status').innerHTML = `
                <div class="wallet-info">
                    <h3>✅ Wallet Connected</h3>
                    <p><strong>Address:</strong> ${walletInfo.account.address}</p>
                    <p><strong>Chain:</strong> ${walletInfo.account.chain}</p>
                    <p><strong>Device:</strong> ${walletInfo.device.appName}</p>
                    <button onclick="disconnectWallet()">Disconnect</button>
                    <button onclick="sendTestTransaction()">Send Test Transaction</button>
                </div>
            `;
            
            // Сохраняем в бэкенд
            fetch('/verify-connection', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    address: walletInfo.account.address,
                    session_id: '{{ session_id }}'
                })
            });
        }

        function disconnectWallet() {
            if (connector) {
                connector.disconnect();
            }
            location.reload();
        }

        async function sendTestTransaction() {
            if (!connectedWallet) return;

            const transaction = {
                validUntil: Math.floor(Date.now() / 1000) + 600, // 10 minutes
                messages: [
                    {
                        address: connectedWallet.account.address, // Отправляем самому себе
                        amount: "1000000", // 0.001 TON
                        payload: "SGVsbG8gZnJvbSBNeSBUT04gZEFwcCE=" // "Hello from My TON dApp!" в base64
                    }
                ]
            };

            try {
                const result = await connector.sendTransaction(transaction);
                alert('Transaction sent! Hash: ' + result.boc);
            } catch (error) {
                console.error('Transaction error:', error);
                alert('Transaction failed: ' + error.message);
            }
        }

        // Инициализация при загрузке
        document.addEventListener('DOMContentLoaded', initTonConnect);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    session_id = session.get('session_id')
    if not session_id:
        session_id = secrets.token_hex(16)
        session['session_id'] = session_id
        sessions[session_id] = {
            'created_at': datetime.now(),
            'payload': None,
            'wallet_address': None
        }
    
    return render_template_string(HTML_TEMPLATE, 
                                manifest_url=request.url_root + 'tonconnect-manifest.json',
                                session_id=session_id)

@app.route('/tonconnect-manifest.json')
def manifest():
    manifest_data = {
        "url": request.url_root,
        "name": "My TON dApp",
        "iconUrl": request.url_root + "icon.png",
        "termsOfUseUrl": request.url_root + "terms",
        "privacyPolicyUrl": request.url_root + "privacy"
    }
    return jsonify(manifest_data)

@app.route('/generate-payload')
def generate_payload():
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'No session'}), 400
    
    # Генерируем уникальный пейлоад
    payload = secrets.token_hex(32)
    js_bridge_key = secrets.token_hex(16)
    
    # Сохраняем в сессию
    if session_id in sessions:
        sessions[session_id]['payload'] = payload
        sessions[session_id]['js_bridge_key'] = js_bridge_key
        sessions[session_id]['created_at'] = datetime.now()
    
    return jsonify({
        'payload': payload,
        'js_bridge_key': js_bridge_key
    })

@app.route('/verify-connection', methods=['POST'])
def verify_connection():
    data = request.get_json()
    wallet_address = data.get('address')
    session_id = data.get('session_id')
    
    if not session_id or session_id not in sessions:
        return jsonify({'error': 'Invalid session'}), 400
    
    # Сохраняем адрес кошелька в сессии
    sessions[session_id]['wallet_address'] = wallet_address
    sessions[session_id]['connected_at'] = datetime.now()
    
    print(f"✅ Wallet connected: {wallet_address}")
    
    return jsonify({
        'status': 'success',
        'message': 'Wallet connected successfully',
        'address': wallet_address
    })

@app.route('/wallet-info')
def wallet_info():
    session_id = session.get('session_id')
    if not session_id or session_id not in sessions:
        return jsonify({'error': 'No active session'}), 401
    
    wallet_data = sessions[session_id]
    return jsonify({
        'connected': wallet_data['wallet_address'] is not None,
        'address': wallet_data['wallet_address'],
        'connected_at': wallet_data.get('connected_at')
    })

# Заглушки для манифеста
@app.route('/icon.png')
def icon():
    return '', 404

@app.route('/terms')
def terms():
    return "Terms of Service", 200

@app.route('/privacy')
def privacy():
    return "Privacy Policy", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)