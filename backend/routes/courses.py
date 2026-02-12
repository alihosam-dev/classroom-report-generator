from flask import Blueprint, jsonify, request
from services.classroom.classroom_client import ClassroomClient

bp = Blueprint('courses', __name__, url_prefix='/api/courses')

classroom_client = ClassroomClient()

@bp.route('/', methods=['GET'])
def get_courses():
    """Get all courses for authenticated teacher"""
    try:
        courses = classroom_client.get_courses()
        return jsonify({'courses': courses})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<course_id>', methods=['GET'])
def get_course(course_id):
    """Get specific course details"""
    try:
        course = classroom_client.get_course(course_id)
        return jsonify({'course': course})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<course_id>/students', methods=['GET'])
def get_students(course_id):
    """Get students in a course"""
    try:
        students = classroom_client.get_students(course_id)
        return jsonify({'students': students})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<course_id>/coursework', methods=['GET'])
def get_coursework(course_id):
    """Get assignments for a course"""
    try:
        coursework = classroom_client.get_coursework(course_id)
        return jsonify({'coursework': coursework})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<course_id>/coursework/<coursework_id>/submissions', methods=['GET'])
def get_submissions(course_id, coursework_id):
    """Get submissions for an assignment"""
    try:
        submissions = classroom_client.get_submissions(course_id, coursework_id)
        return jsonify({'submissions': submissions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
