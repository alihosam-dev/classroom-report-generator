"""
Report card image generator
"""
from PIL import Image, ImageDraw, ImageFont
import os

class ReportCardGenerator:
    def __init__(self):
        self.width = int(os.getenv('REPORT_CARD_WIDTH', 1200))
        self.height = int(os.getenv('REPORT_CARD_HEIGHT', 1600))
        self.bg_color = (255, 255, 255)
        self.text_color = (0, 0, 0)
        self.accent_color = (68, 114, 196)
    
    def generate_all(self, course, students, coursework, submissions, output_dir):
        """Generate report cards for all students"""
        report_cards = []
        
        os.makedirs(output_dir, exist_ok=True)
        
        for student in students:
            filename = self._generate_student_card(
                student, course, coursework, submissions, output_dir
            )
            report_cards.append(filename)
        
        return report_cards
    
    def _generate_student_card(self, student, course, coursework, submissions, output_dir):
        """Generate report card for one student"""
        # Create image
        img = Image.new('RGB', (self.width, self.height), self.bg_color)
        draw = ImageDraw.Draw(img)
        
        student_name = student.get('profile', {}).get('name', {}).get('fullName', 'Unknown')
        student_id = student.get('userId')
        course_name = course.get('name', 'Course')
        
        # Draw content (simplified - you can enhance this)
        try:
            title_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 48)
            text_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 32)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
        
        # Title
        draw.text((self.width // 2, 100), 'Student Report Card', 
                 font=title_font, fill=self.accent_color, anchor='mm')
        
        # Student name
        draw.text((self.width // 2, 200), student_name, 
                 font=title_font, fill=self.text_color, anchor='mm')
        
        # Course name
        draw.text((self.width // 2, 280), course_name, 
                 font=text_font, fill=self.text_color, anchor='mm')
        
        # Grades
        y_pos = 400
        total_grades = []
        
        for cw in coursework:
            cw_id = cw['id']
            cw_title = cw['title']
            cw_submissions = submissions.get(cw_id, [])
            
            # Find student's grade
            grade = None
            for sub in cw_submissions:
                if sub.get('userId') == student_id:
                    grade = sub.get('assignedGrade')
                    break
            
            grade_text = f"{cw_title}: {grade if grade is not None else 'N/A'}"
            draw.text((100, y_pos), grade_text, font=text_font, fill=self.text_color)
            
            if grade is not None:
                total_grades.append(grade)
            
            y_pos += 60
        
        # Average
        if total_grades:
            avg = sum(total_grades) / len(total_grades)
            draw.text((self.width // 2, self.height - 150), 
                     f'Average: {round(avg, 2)}', 
                     font=title_font, fill=self.accent_color, anchor='mm')
        
        # Save
        safe_filename = self._sanitize_filename(f"{student_name}_report.png")
        file_path = os.path.join(output_dir, safe_filename)
        img.save(file_path)
        
        return safe_filename
    
    def _sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename
