"""
Report card image generator with modern, professional design
"""
from PIL import Image, ImageDraw, ImageFont
import logging
import os
from pathlib import Path

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
        self.font_dir = os.getenv(
            'REPORT_CARD_FONT_DIR',
            str(Path(__file__).resolve().parent.parent.parent / 'assets' / 'fonts')
        )
        self.force_bundled_fonts = os.getenv('REPORT_CARD_FORCE_BUNDLED_FONTS', 'false').lower() == 'true'
        self._font_cache = {}
        self._font_errors = {}
        self._font_debug = {}
        self.logger = logging.getLogger(__name__)

    def _load_font(self, filename, size):
        font_path = Path(self.font_dir) / filename
        cache_key = (filename, size)

        if cache_key in self._font_cache:
            return self._font_cache[cache_key]

        if not font_path.exists():
            self.logger.warning('Font %s not found at %s', filename, font_path)
            self._font_errors[cache_key] = 'missing'
            return None

        try:
            font = ImageFont.truetype(str(font_path), size)
            self._font_cache[cache_key] = font
            self._font_errors[cache_key] = None
            self.logger.info('Loaded font %s from %s', filename, font_path)
            return font
        except OSError as exc:
            # Pillow raises an OSError with "unknown file format" when the file
            # exists but cannot be parsed as a font (e.g., missing Git LFS pull).
            self._font_errors[cache_key] = f'parse_error: {exc}'
            self.logger.error('Failed to load font %s from %s: %s', filename, font_path, exc)
            return None
    
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
        
        self._font_errors = {}
        font_specs = {
            'title_font': ('SFPRODISPLAYBOLD.OTF', 56),
            'subtitle_font': ('SFPRODISPLAYMEDIUM.OTF', 36),
            'heading_font': ('SFPRODISPLAYSEMIBOLDITALIC.OTF', 32),
            'text_font': ('sf-pro-text-regular.otf', 28),
            'small_font': ('sf-pro-text-regular.otf', 24),
            'grade_font': ('SFPRODISPLAYBOLD.OTF', 36)
        }
        fonts = {key: self._load_font(*spec) for key, spec in font_specs.items()}
        missing_fonts = [key for key, font in fonts.items() if font is None]

        if missing_fonts:
            self.logger.warning('Bundled fonts missing or unreadable: %s', ', '.join(missing_fonts))
            if self.force_bundled_fonts:
                raise RuntimeError(
                    'Bundled report card fonts are required but missing. '
                    'Make sure git lfs assets are pulled on this environment.'
                )
            fallback_font = ImageFont.load_default()
            for key in missing_fonts:
                fonts[key] = fallback_font
            self.logger.info('Falling back to Pillow default font for: %s', ', '.join(missing_fonts))

        font_details = []
        font_dir_path = Path(self.font_dir)
        fallback_used = bool(missing_fonts and not self.force_bundled_fonts)
        for alias, (filename, size) in font_specs.items():
            font_path = font_dir_path / filename
            font_details.append({
                'alias': alias,
                'filename': filename,
                'size': size,
                'path': str(font_path),
                'exists': font_path.exists(),
                'load_error': self._font_errors.get((filename, size)),
                'using_fallback': alias in missing_fonts and not self.force_bundled_fonts
            })

        self._font_debug = {
            'font_dir': str(font_dir_path),
            'font_dir_exists': font_dir_path.exists(),
            'force_bundled_fonts': self.force_bundled_fonts,
            'missing_fonts': missing_fonts,
            'fallback_used': fallback_used,
            'fonts': font_details
        }

        title_font = fonts['title_font']
        subtitle_font = fonts['subtitle_font']
        heading_font = fonts['heading_font']
        text_font = fonts['text_font']
        small_font = fonts['small_font']
        grade_font = fonts['grade_font']
        
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

    def get_font_debug(self):
        """Expose last font loading status for API callers"""
        return self._font_debug

