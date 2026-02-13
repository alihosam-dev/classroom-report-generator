from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=['http://localhost:3000'])

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['OUTPUT_DIR'] = os.getenv('OUTPUT_DIR', '../output/reports')

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
    port = int(os.getenv('BACKEND_PORT', 5001))
    app.run(debug=True, port=port, host='127.0.0.1')
