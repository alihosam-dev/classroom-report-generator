"""
Report generation orchestrator
"""
from services.classroom.classroom_client import ClassroomClient
from services.export.excel_generator import ExcelGenerator
from services.export.report_card_generator import ReportCardGenerator
import os

class ReportGenerator:
    def __init__(self):
        self.classroom_client = ClassroomClient()
        self.excel_generator = ExcelGenerator()
        self.report_card_generator = ReportCardGenerator()
        self.output_dir = os.getenv('OUTPUT_DIR', '../output/reports')
    
    def generate(self, course_id, coursework_ids, include_grades=True):
        """Generate all reports"""
        # Fetch data
        course = self.classroom_client.get_course(course_id)
        students = self.classroom_client.get_students(course_id)
        coursework = self.classroom_client.get_coursework(course_id)
        submissions = self.classroom_client.get_all_submissions(course_id, coursework_ids)
        
        # Filter coursework to selected only
        selected_coursework = [cw for cw in coursework if cw['id'] in coursework_ids]
        
        # Generate Excel file
        excel_filename = f"{course['name']}_report.xlsx"
        excel_path = self.excel_generator.generate(
            course=course,
            students=students,
            coursework=selected_coursework,
            submissions=submissions,
            output_path=os.path.join(self.output_dir, excel_filename),
            include_grades=include_grades
        )
        
        # Generate report cards
        report_cards = []
        if include_grades:
            report_cards = self.report_card_generator.generate_all(
                course=course,
                students=students,
                coursework=selected_coursework,
                submissions=submissions,
                output_dir=self.output_dir
            )
        
        return {
            'success': True,
            'excel_file': excel_filename,
            'report_cards': report_cards,
            'message': f'Generated reports for {len(students)} students'
        }
