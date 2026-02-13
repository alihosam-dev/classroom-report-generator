"""
Report generation orchestrator
"""
from services.classroom.classroom_client import ClassroomClient
from services.export.excel_generator import ExcelGenerator
from services.export.report_card_generator import ReportCardGenerator
import os
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.classroom_client = ClassroomClient()
        self.excel_generator = ExcelGenerator()
        self.report_card_generator = ReportCardGenerator()
        default_output = '/tmp/reports' if os.getenv('VERCEL') else '../output/reports'
        self.output_dir = os.getenv('OUTPUT_DIR', default_output)
    
    def _prepare_report_data(self, students, coursework, submissions):
        """Prepare report data for frontend display"""
        student_data = []
        
        for student in students:
            student_name = student.get('profile', {}).get('name', {}).get('fullName', 'Unknown')
            student_id = student.get('userId')
            student_email = student.get('profile', {}).get('emailAddress', '')
            
            grades = []
            total_earned = 0
            total_possible = 0
            
            for cw in coursework:
                cw_id = cw['id']
                cw_title = cw['title']
                max_pts = cw.get('maxPoints', 100)
                cw_submissions = submissions.get(cw_id, [])
                
                # Find student's submission
                grade = None
                submission_state = None
                for sub in cw_submissions:
                    if sub.get('userId') == student_id:
                        grade = sub.get('assignedGrade')
                        submission_state = sub.get('state')
                        break
                
                if grade is not None:
                    grades.append({
                        'assignment': cw_title,
                        'grade': grade,
                        'max_points': max_pts,
                        'display': f"{grade}/{max_pts}"
                    })
                    total_earned += grade
                    total_possible += max_pts
                elif submission_state == 'TURNED_IN' or submission_state == 'RETURNED':
                    # Submitted but not graded yet
                    grades.append({
                        'assignment': cw_title,
                        'grade': None,
                        'max_points': max_pts,
                        'display': 'Not Graded Yet'
                    })
                else:
                    # Not submitted
                    grades.append({
                        'assignment': cw_title,
                        'grade': None,
                        'max_points': max_pts,
                        'display': 'Not Submitted'
                    })
            
            # Calculate average percentage
            avg_pct = (total_earned / total_possible * 100) if total_possible > 0 else 0
            
            student_data.append({
                'name': student_name,
                'email': student_email,
                'grades': grades,
                'average': f"{round(avg_pct, 1)}%"
            })
        
        return student_data
    
    def _generate_analysis(self, students, coursework, submissions):
        """Generate detailed analysis and insights"""
        analysis = {
            'assignments': [],
            'class_stats': {},
            'insights': []
        }
        
        # Per-assignment statistics
        for cw in coursework:
            cw_id = cw['id']
            cw_title = cw['title']
            max_pts = cw.get('maxPoints', 100)
            cw_submissions = submissions.get(cw_id, [])
            
            grades = [sub.get('assignedGrade') for sub in cw_submissions 
                     if sub.get('assignedGrade') is not None]
            
            if grades:
                avg = sum(grades) / len(grades)
                avg_pct = (avg / max_pts * 100) if max_pts > 0 else 0
                
                analysis['assignments'].append({
                    'title': cw_title,
                    'average': f"{round(avg_pct, 1)}%",
                    'highest': f"{max(grades)}/{max_pts}",
                    'lowest': f"{min(grades)}/{max_pts}",
                    'submissions': len(cw_submissions),
                    'graded': len(grades),
                    'max_points': max_pts
                })
        
        # Overall class statistics
        all_percentages = []
        students_with_grades = 0
        
        for student in students:
            student_id = student.get('userId')
            total_earned = 0
            total_possible = 0
            
            for cw in coursework:
                cw_id = cw['id']
                max_pts = cw.get('maxPoints', 100)
                cw_submissions = submissions.get(cw_id, [])
                
                for sub in cw_submissions:
                    if sub.get('userId') == student_id:
                        grade = sub.get('assignedGrade')
                        if grade is not None:
                            total_earned += grade
                            total_possible += max_pts
                        break
            
            if total_possible > 0:
                student_pct = (total_earned / total_possible * 100)
                all_percentages.append(student_pct)
                students_with_grades += 1
        
        # Calculate class statistics
        if all_percentages:
            class_avg = sum(all_percentages) / len(all_percentages)
            analysis['class_stats'] = {
                'average': f"{round(class_avg, 1)}%",
                'highest': f"{round(max(all_percentages), 1)}%",
                'lowest': f"{round(min(all_percentages), 1)}%",
                'total_students': len(students)
            }
            
            # Generate insights
            if class_avg >= 90:
                analysis['insights'].append({'key': 'excellentPerformance', 'value': None})
            elif class_avg >= 80:
                analysis['insights'].append({'key': 'strongPerformance', 'value': None})
            elif class_avg < 70:
                analysis['insights'].append({'key': 'belowAverage', 'value': None})
            
            # Check for struggling students
            struggling = sum(1 for p in all_percentages if p < 60)
            if struggling > 0:
                analysis['insights'].append({'key': 'strugglingStudents', 'value': struggling})
            
            # Check for high performers
            high_performers = sum(1 for p in all_percentages if p >= 95)
            if high_performers > 0:
                analysis['insights'].append({'key': 'highPerformers', 'value': high_performers})
            
            # Check grade distribution
            spread = max(all_percentages) - min(all_percentages)
            if spread > 50:
                analysis['insights'].append({'key': 'wideDistribution', 'value': round(spread, 1)})
        
        return analysis
    
    def generate(self, course_id, coursework_ids, include_grades=True):
        """Generate all reports"""
        # Generate unique report ID
        now = datetime.now()
        report_id = now.strftime('%Y%m%d_%H%M%S')
        readable_date = now.strftime('%b %d, %Y')
        
        # Fetch data
        course = self.classroom_client.get_course(course_id)
        students = self.classroom_client.get_students(course_id)
        coursework = self.classroom_client.get_coursework(course_id)
        submissions = self.classroom_client.get_all_submissions(course_id, coursework_ids)
        
        # Filter coursework to selected only
        selected_coursework = [cw for cw in coursework if cw['id'] in coursework_ids]
        
        # Generate Excel file
        excel_filename = f"{course['name']} - {readable_date}.xlsx"
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
            cards_dir = os.path.join(self.output_dir, f'report_cards_{report_id}')
            os.makedirs(cards_dir, exist_ok=True)
            report_cards = self.report_card_generator.generate_all(
                course=course,
                students=students,
                coursework=selected_coursework,
                submissions=submissions,
                output_dir=cards_dir
            )
        
        # Prepare report data for display
        report_data = self._prepare_report_data(students, selected_coursework, submissions)
        analysis = self._generate_analysis(students, selected_coursework, submissions)
        
        return {
            'success': True,
            'excel_file': excel_filename,
            'report_cards': report_cards,
            'report_id': report_id,
            'report_data': report_data,
            'analysis': analysis,
            'message': f'Generated reports for {len(students)} students'
        }
