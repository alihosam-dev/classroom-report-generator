"""
Report card image generator with modern, professional design
"""
from PIL import Image, ImageDraw, ImageFont
import os

class ReportCardGenerator:
    def __init__(self):
        self.width = int(os.getenv('REPORT_CARD_WIDTH', 1200))
        self.height = int(os.getenv('REPORT_CARD_HEIGHT', 1600))
        self.bg_color = (255, 255, 255)
        self.primary_color = (41, 98, 255)  # Modern blue
        self.secondary_color = (99, 102, 241)  # Indigo
        self.accent_color = (16, 185, 129)  # Green
        self.text_dark = (31, 41, 55)  # Dark gray
        self.text_light = (107, 114, 128)  # Medium gray
        self.bg_light = (249, 250, 251)  # Light background
    
    def _get_letter_grade(self, percentage):
        """Convert percentage to letter grade"""
        if percentage >= 90:
            return 'A*'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B'
        elif percentage >= 60:
            return 'C'
        elif percentage >= 50:
            return 'D'
        elif percentage >= 40:
            return 'E'
        elif percentage >= 30:
            return 'F'
        elif percentage >= 20:
            return 'G'
        else:
            return 'U'
    
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
        """Generate modern report card for one student"""
        # Create image
        img = Image.new('RGB', (self.width, self.height), self.bg_color)
        draw = ImageDraw.Draw(img)
        
        student_name = student.get('profile', {}).get('name', {}).get('fullName', 'Unknown')
        student_id = student.get('userId')
        course_name = course.get('name', 'Course')
        
        # Load fonts - Try SF Pro (macOS system font), then fallback to others
        try:
            # Try SF Pro Display (modern macOS font)
            title_font = ImageFont.truetype('/System/Library/Fonts/SF-Pro-Display-Bold.otf', 56)
            subtitle_font = ImageFont.truetype('/System/Library/Fonts/SF-Pro-Display-Medium.otf', 36)
            heading_font = ImageFont.truetype('/System/Library/Fonts/SF-Pro-Display-Semibold.otf', 32)
            text_font = ImageFont.truetype('/System/Library/Fonts/SF-Pro-Text-Regular.otf', 28)
            small_font = ImageFont.truetype('/System/Library/Fonts/SF-Pro-Text-Regular.otf', 24)
            grade_font = ImageFont.truetype('/System/Library/Fonts/SF-Pro-Display-Bold.otf', 36)
        except:
            try:
                # Fallback to Avenir (also on macOS)
                title_font = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 56)
                subtitle_font = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 36)
                heading_font = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 32)
                text_font = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 28)
                small_font = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 24)
                grade_font = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 36)
            except:
                # Final fallback
                title_font = subtitle_font = heading_font = text_font = small_font = grade_font = ImageFont.load_default()
        
        # Header with gradient effect (simulated with rectangles)
        header_height = 280
        draw.rectangle([0, 0, self.width, header_height], fill=self.primary_color)
        draw.rectangle([0, header_height-10, self.width, header_height], fill=self.secondary_color)
        
        # Title
        draw.text((self.width // 2, 80), 'STUDENT REPORT CARD', 
                 font=heading_font, fill=(255, 255, 255), anchor='mm')
        
        # Student name (larger and bold)
        draw.text((self.width // 2, 160), student_name, 
                 font=title_font, fill=(255, 255, 255), anchor='mm')
        
        # Course name
        draw.text((self.width // 2, 230), course_name, 
                 font=subtitle_font, fill=(255, 255, 255, 200), anchor='mm')
        
        # Content area with padding
        content_start_y = 340
        margin_x = 80
        
        # Section: Grades
        current_y = content_start_y
        
        # "Grades Overview" section header
        draw.rectangle([margin_x, current_y, self.width - margin_x, current_y + 60], 
                      fill=self.bg_light)
        draw.text((margin_x + 20, current_y + 30), 'GRADES OVERVIEW', 
                 font=heading_font, fill=self.text_dark, anchor='lm')
        
        current_y += 90
        
        # Draw grades in a structured table-like format
        total_earned = []
        total_possible = []
        
        for idx, cw in enumerate(coursework):
            cw_id = cw['id']
            cw_title = cw['title']
            cw_submissions = submissions.get(cw_id, [])
            max_pts = cw.get('maxPoints', 100)
            
            # Find student's submission
            grade = None
            submission_state = None
            for sub in cw_submissions:
                if sub.get('userId') == student_id:
                    grade = sub.get('assignedGrade')
                    submission_state = sub.get('state')
                    break
            
            # Alternating row backgrounds
            if idx % 2 == 0:
                draw.rectangle([margin_x, current_y - 10, self.width - margin_x, current_y + 50],
                              fill=self.bg_light)
            
            # Assignment title
            draw.text((margin_x + 20, current_y + 20), cw_title[:50], 
                     font=text_font, fill=self.text_dark, anchor='lm')
            
            # Grade or status
            if grade is not None:
                percentage = (grade / max_pts * 100) if max_pts > 0 else 0
                letter_grade = self._get_letter_grade(percentage)
                grade_text = f"{grade}/{max_pts} ({letter_grade})"
                
                # Color code based on percentage
                if percentage >= 90:
                    grade_color = self.accent_color
                elif percentage >= 80:
                    grade_color = self.primary_color
                elif percentage >= 70:
                    grade_color = (251, 146, 60)  # Orange
                else:
                    grade_color = (239, 68, 68)  # Red
                
                # Draw grade with letter in brackets
                draw.text((self.width - margin_x - 20, current_y + 20), grade_text, 
                         font=heading_font, fill=grade_color, anchor='rm')
                
                total_earned.append(grade)
                total_possible.append(max_pts)
            elif submission_state == 'TURNED_IN' or submission_state == 'RETURNED':
                draw.text((self.width - margin_x - 20, current_y + 20), "Not Graded", 
                         font=text_font, fill=(251, 146, 60), anchor='rm')  # Orange
            else:
                draw.text((self.width - margin_x - 20, current_y + 20), "Not Submitted", 
                         font=text_font, fill=(239, 68, 68), anchor='rm')  # Red
            
            current_y += 70
        
        # Summary section at bottom
        if total_earned and sum(total_possible) > 0:
            avg_pct = (sum(total_earned) / sum(total_possible) * 100)
            avg_letter = self._get_letter_grade(avg_pct)
            
            # Summary box
            summary_y = self.height - 220
            draw.rectangle([margin_x, summary_y, self.width - margin_x, summary_y + 160],
                          fill=self.primary_color, outline=self.secondary_color, width=3)
            
            # Overall average label
            draw.text((self.width // 2, summary_y + 40), 'OVERALL AVERAGE', 
                     font=heading_font, fill=(255, 255, 255), anchor='mm')
            
            # Percentage with letter grade
            draw.text((self.width // 2, summary_y + 110), f'{round(avg_pct, 1)}% ({avg_letter})', 
                     font=title_font, fill=(255, 255, 255), anchor='mm')
        
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

