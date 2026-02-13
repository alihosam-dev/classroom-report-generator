"""
Mock data generator for testing without Google Classroom API
"""
import random
from datetime import datetime

class MockDataGenerator:
    def __init__(self):
        self.student_names = [
            "Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Prince",
            "Ethan Hunt", "Fiona Gallagher", "George Wilson", "Hannah Baker",
            "Isaac Newton", "Julia Roberts", "Kevin Hart", "Laura Palmer",
            "Michael Scott", "Nina Simone", "Oliver Twist", "Patricia King"
        ]
        
        self.course_names = [
            "Mathematics IGCSE", "English as a Second Language IGCSE", "Edexcel Physics Unit 4",
            "Computer Science IGCSE",  "Cambridge Chemistry AS"
        ]
        
        self.assignment_titles = [
            "Quiz 1", "Homework Assignment 1", "Midterm Exam",
            "Project Presentation", "Lab Report", "Final Essay",
            "Weekly Quiz 2", "Group Project", "Research Paper",
            "Class Participation", "Final Exam", "Book Review"
        ]
    
    def generate_courses(self):
        """Generate mock courses"""
        courses = []
        for i, name in enumerate(self.course_names):
            courses.append({
                'id': f'mock_course_{i+1}',
                'name': name,
                'section': f'Section {chr(65+i)}',
                'descriptionHeading': f'{name} - Mock Course',
                'room': f'Room {100+i*10}',
                'ownerId': 'mock_teacher_1',
                'courseState': 'ACTIVE'
            })
        return courses
    
    def generate_students(self, course_id, num_students=16):
        """Generate mock students"""
        students = []
        for i in range(num_students):
            name = self.student_names[i] if i < len(self.student_names) else f"Student {i+1}"
            students.append({
                'courseId': course_id,
                'userId': f'mock_student_{i+1}',
                'profile': {
                    'id': f'mock_student_{i+1}',
                    'name': {
                        'givenName': name.split()[0],
                        'familyName': name.split()[1],
                        'fullName': name
                    },
                    'emailAddress': f'{name.lower().replace(" ", ".")}@student.school.com',
                    'photoUrl': None
                }
            })
        return students
    
    def generate_coursework(self, course_id, num_assignments=8):
        """Generate mock coursework/assignments"""
        coursework = []
        for i in range(num_assignments):
            title = self.assignment_titles[i] if i < len(self.assignment_titles) else f"Assignment {i+1}"
            coursework.append({
                'courseId': course_id,
                'id': f'mock_cw_{i+1}',
                'title': title,
                'description': f'Description for {title}',
                'state': 'PUBLISHED',
                'alternateLink': f'https://classroom.google.com/mock/{i+1}',
                'creationTime': datetime.now().isoformat(),
                'updateTime': datetime.now().isoformat(),
                'maxPoints': random.choice([50, 75, 100, 100, 100]),  # Mostly 100
                'workType': 'ASSIGNMENT',
                'assigneeMode': 'ALL_STUDENTS'
            })
        return coursework
    
    def generate_submissions(self, course_id, coursework_ids, student_ids):
        """Generate mock submissions with realistic grades"""
        submissions = {}
        
        for cw_id in coursework_ids:
            cw_submissions = []
            # Find the coursework to get max points
            max_points = 100  # default
            
            for student_id in student_ids:
                # 70% chance student has submitted and been graded
                # 20% chance submitted but not graded yet
                # 10% chance not submitted
                rand = random.random()
                
                if rand < 0.70:  # Graded
                    # Generate realistic grade distribution
                    grade_range = random.random()
                    if grade_range < 0.15:  # 15% excellent (90-100%)
                        grade = random.randint(90, 100)
                    elif grade_range < 0.40:  # 25% good (80-89%)
                        grade = random.randint(80, 89)
                    elif grade_range < 0.70:  # 30% average (70-79%)
                        grade = random.randint(70, 79)
                    elif grade_range < 0.90:  # 20% below average (60-69%)
                        grade = random.randint(60, 69)
                    else:  # 10% poor (below 60%)
                        grade = random.randint(40, 59)
                    
                    cw_submissions.append({
                        'courseId': course_id,
                        'courseWorkId': cw_id,
                        'id': f'mock_sub_{cw_id}_{student_id}',
                        'userId': student_id,
                        'state': 'RETURNED',
                        'assignedGrade': grade,
                        'draftGrade': grade
                    })
                elif rand < 0.90:  # Submitted but not graded
                    cw_submissions.append({
                        'courseId': course_id,
                        'courseWorkId': cw_id,
                        'id': f'mock_sub_{cw_id}_{student_id}',
                        'userId': student_id,
                        'state': 'TURNED_IN',
                        'assignedGrade': None,
                        'draftGrade': None
                    })
                else:  # Not submitted
                    cw_submissions.append({
                        'courseId': course_id,
                        'courseWorkId': cw_id,
                        'id': f'mock_sub_{cw_id}_{student_id}',
                        'userId': student_id,
                        'state': 'NEW',
                        'assignedGrade': None,
                        'draftGrade': None
                    })
            
            submissions[cw_id] = cw_submissions
        
        return submissions

# Singleton instance
mock_generator = MockDataGenerator()
