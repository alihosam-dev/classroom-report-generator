"""
Mock data routes for testing without Google Classroom
"""
from flask import Blueprint, jsonify, request
from services.mock_data import mock_generator
from services.export.report_generator import ReportGenerator
import os

mock_bp = Blueprint('mock', __name__)
report_generator = ReportGenerator()

@mock_bp.route('/api/mock/courses', methods=['GET'])
def get_mock_courses():
    """Get mock courses"""
    courses = mock_generator.generate_courses()
    return jsonify(courses)

@mock_bp.route('/api/mock/courses/<course_id>/coursework', methods=['GET'])
def get_mock_coursework(course_id):
    """Get mock coursework for a course"""
    coursework = mock_generator.generate_coursework(course_id, num_assignments=8)
    return jsonify(coursework)

@mock_bp.route('/api/mock/reports/generate', methods=['POST'])
def generate_mock_report():
    """Generate a report using mock data"""
    try:
        data = request.get_json()
        course_id = data.get('courseId')
        coursework_ids = data.get('courseworkIds', [])
        include_grades = data.get('includeGrades', True)
        
        # Generate mock data
        course = next((c for c in mock_generator.generate_courses() if c['id'] == course_id), None)
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        students = mock_generator.generate_students(course_id)
        coursework = mock_generator.generate_coursework(course_id)
        
        # Filter to selected coursework
        selected_coursework = [cw for cw in coursework if cw['id'] in coursework_ids]
        
        # Generate submissions
        student_ids = [s['userId'] for s in students]
        submissions = mock_generator.generate_submissions(course_id, coursework_ids, student_ids)
        
        # Prepare report data (same as real report generator)
        report_data = report_generator._prepare_report_data(students, selected_coursework, submissions)
        analysis = report_generator._generate_analysis(students, selected_coursework, submissions)
        
        # Generate files
        from datetime import datetime
        now = datetime.now()
        report_id = now.strftime('%Y%m%d_%H%M%S')
        readable_date = now.strftime('%b %d, %Y')
        output_dir = os.getenv('OUTPUT_DIR', '../output/reports')
        
        # Generate Excel
        from services.export.excel_generator import ExcelGenerator
        excel_gen = ExcelGenerator()
        excel_filename = f"{course['name']} - {readable_date}.xlsx"
        excel_path = excel_gen.generate(
            course=course,
            students=students,
            coursework=selected_coursework,
            submissions=submissions,
            output_path=os.path.join(output_dir, excel_filename),
            include_grades=include_grades
        )
        
        # Generate report cards
        from services.export.report_card_generator import ReportCardGenerator
        card_gen = ReportCardGenerator()
        cards_dir = os.path.join(output_dir, f'report_cards_{report_id}')
        report_cards = card_gen.generate_all(course, students, selected_coursework, submissions, cards_dir)
        
        return jsonify({
            'success': True,
            'reportId': report_id,
            'excelFile': excel_filename,
            'reportCards': report_cards,
            'reportData': report_data,
            'analysis': analysis
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
