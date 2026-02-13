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
        print(f"ERROR in callback: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@bp.route('/status', methods=['GET'])
def status():
    """Check authentication status and get user info"""
    try:
        is_authenticated = auth_service.is_authenticated()
        user_info = None
        if is_authenticated:
            user_info = auth_service.get_user_info()
        return jsonify({
            'authenticated': is_authenticated,
            'user': user_info
        })
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
