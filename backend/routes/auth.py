from flask import Blueprint, request, jsonify, session
from services.auth.google_auth import GoogleAuth

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

auth_service = GoogleAuth()

@bp.route('/login', methods=['GET'])
def login():
    """Initiate Google OAuth flow"""
    try:
        auth_url = auth_service.get_authorization_url()
        return jsonify({'auth_url': auth_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/callback', methods=['POST'])
def callback():
    """Handle OAuth callback"""
    try:
        code = request.json.get('code')
        if not code:
            return jsonify({'error': 'Authorization code required'}), 400
        
        credentials = auth_service.exchange_code(code)
        session['credentials'] = credentials
        
        return jsonify({'message': 'Authentication successful'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/status', methods=['GET'])
def status():
    """Check authentication status"""
    try:
        is_authenticated = auth_service.is_authenticated()
        return jsonify({'authenticated': is_authenticated})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/logout', methods=['POST'])
def logout():
    """Logout and clear session"""
    try:
        auth_service.logout()
        session.clear()
        return jsonify({'message': 'Logged out successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
