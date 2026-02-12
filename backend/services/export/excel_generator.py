"""
Excel report generator
"""
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, Reference
import os

class ExcelGenerator:
    def generate(self, course, students, coursework, submissions, output_path, include_grades=True):
        """Generate Excel file with raw grades and analysis"""
        
        # Create workbook
        wb = Workbook()
        
        # Remove default sheet
        if 'Sheet' in wb.sheetnames:
            wb.remove(wb['Sheet'])
        
        # Create raw grades sheet
        self._create_raw_grades_sheet(wb, students, coursework, submissions, include_grades)
        
        # Create analysis sheet
        if include_grades:
            self._create_analysis_sheet(wb, students, coursework, submissions)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save workbook
        wb.save(output_path)
        
        return output_path
    
    def _create_raw_grades_sheet(self, wb, students, coursework, submissions, include_grades):
        """Create sheet with raw grades"""
        ws = wb.create_sheet('Raw Grades')
        
        # Headers
        headers = ['Student Name', 'Email'] + [cw['title'] for cw in coursework]
        if include_grades:
            headers.append('Average')
        
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col)
            cell.value = header
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
            cell.alignment = Alignment(horizontal='center')
        
        # Data rows
        for row_idx, student in enumerate(students, 2):
            student_name = student.get('profile', {}).get('name', {}).get('fullName', 'Unknown')
            student_email = student.get('profile', {}).get('emailAddress', '')
            student_id = student.get('userId')
            
            ws.cell(row=row_idx, column=1, value=student_name)
            ws.cell(row=row_idx, column=2, value=student_email)
            
            grades = []
            for col_idx, cw in enumerate(coursework, 3):
                cw_id = cw['id']
                cw_submissions = submissions.get(cw_id, [])
                
                # Find this student's submission
                grade = None
                for sub in cw_submissions:
                    if sub.get('userId') == student_id:
                        grade = sub.get('assignedGrade')
                        break
                
                if include_grades and grade is not None:
                    ws.cell(row=row_idx, column=col_idx, value=grade)
                    grades.append(grade)
                else:
                    ws.cell(row=row_idx, column=col_idx, value='-')
            
            # Calculate average
            if include_grades and grades:
                avg = sum(grades) / len(grades)
                ws.cell(row=row_idx, column=len(coursework) + 3, value=round(avg, 2))
        
        # Auto-size columns
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column_letter].width = adjusted_width
    
    def _create_analysis_sheet(self, wb, students, coursework, submissions):
        """Create sheet with statistical analysis"""
        ws = wb.create_sheet('Analysis')
        
        # Title
        ws['A1'] = 'Grade Analysis'
        ws['A1'].font = Font(size=16, bold=True)
        
        # Statistics table
        ws['A3'] = 'Assignment'
        ws['B3'] = 'Average'
        ws['C3'] = 'Highest'
        ws['D3'] = 'Lowest'
        ws['E3'] = 'Submissions'
        
        for col in range(1, 6):
            cell = ws.cell(row=3, column=col)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
        
        row = 4
        for cw in coursework:
            cw_id = cw['id']
            cw_submissions = submissions.get(cw_id, [])
            
            grades = [sub.get('assignedGrade') for sub in cw_submissions 
                     if sub.get('assignedGrade') is not None]
            
            ws.cell(row=row, column=1, value=cw['title'])
            
            if grades:
                ws.cell(row=row, column=2, value=round(sum(grades) / len(grades), 2))
                ws.cell(row=row, column=3, value=max(grades))
                ws.cell(row=row, column=4, value=min(grades))
            
            ws.cell(row=row, column=5, value=len(cw_submissions))
            row += 1
        
        # Auto-size columns
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column_letter].width = adjusted_width
