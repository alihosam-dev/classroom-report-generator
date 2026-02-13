from flask import Blueprint, jsonify, request, send_file
from services.export.report_generator import ReportGenerator
import os
import zipfile
from io import BytesIO

bp = Blueprint('reports', __name__, url_prefix='/api/reports')

report_generator = ReportGenerator()

@bp.route('/generate', methods=['POST'])
def generate_report():
    """Generate Excel and report card files"""
    try:
        data = request.json
        course_id = data.get('course_id')
        coursework_ids = data.get('coursework_ids', [])
        include_grades = data.get('include_grades', True)
        
        if not course_id or not coursework_ids:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Generate reports
        result = report_generator.generate(
            course_id=course_id,
            coursework_ids=coursework_ids,
            include_grades=include_grades
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download generated report file"""
    try:
        output_dir = os.getenv('OUTPUT_DIR', '../output/reports')
        file_path = os.path.join(output_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/list', methods=['GET'])
def list_reports():
    """List all generated reports"""
    try:
        output_dir = os.getenv('OUTPUT_DIR', '../output/reports')
        
        if not os.path.exists(output_dir):
            return jsonify({'files': []})
        
        files = [f for f in os.listdir(output_dir) 
                if os.path.isfile(os.path.join(output_dir, f))]
        
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/download-cards/<report_id>', methods=['GET'])
def download_report_cards(report_id):
    """Download all report card images as a zip file"""
    try:
        output_dir = os.getenv('OUTPUT_DIR', '../output/reports')
        cards_dir = os.path.join(output_dir, f'report_cards_{report_id}')
        
        if not os.path.exists(cards_dir):
            return jsonify({'error': 'Report cards not found'}), 404
        
        # Create zip file in memory
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for filename in os.listdir(cards_dir):
                if filename.endswith('.png'):
                    file_path = os.path.join(cards_dir, filename)
                    zf.write(file_path, filename)
        
        memory_file.seek(0)
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'report_cards_{report_id}.zip'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
