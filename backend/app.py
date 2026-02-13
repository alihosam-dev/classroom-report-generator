from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Configure CORS for production
if os.getenv('FLASK_ENV') == 'production':
    allowed_origins = os.getenv('ALLOWED_ORIGINS', '').split(',')
    CORS(app, supports_credentials=True, origins=allowed_origins)
else:
    CORS(app, supports_credentials=True, origins=['http://localhost:3000'])

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
default_output_dir = '/tmp/reports' if os.getenv('VERCEL') else '../output/reports'
app.config['OUTPUT_DIR'] = os.getenv('OUTPUT_DIR', default_output_dir)
# Session cookies must be cross-site when frontend + backend use different domains
if os.getenv('FLASK_ENV') == 'production':
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_NAME'] = os.getenv('SESSION_COOKIE_NAME', 'crg_session')

# Import routes
from routes import auth, courses, reports
from routes.mock import mock_bp

app.register_blueprint(auth.bp)
app.register_blueprint(courses.bp)
app.register_blueprint(reports.bp)
app.register_blueprint(mock_bp)

@app.route('/')
def home():
    return jsonify({
        'message': 'Classroom Report Generator API',
        'version': '1.0.0',
        'status': 'running'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', os.getenv('BACKEND_PORT', 5001)))
    debug = os.getenv('FLASK_ENV') != 'production'
    host = '0.0.0.0' if os.getenv('FLASK_ENV') == 'production' else '127.0.0.1'
    app.run(debug=debug, port=port, host=host)
