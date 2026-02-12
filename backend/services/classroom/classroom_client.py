"""
Google Classroom API client
"""
from googleapiclient.discovery import build
from services.auth.google_auth import GoogleAuth

class ClassroomClient:
    def __init__(self):
        self.auth = GoogleAuth()
        self.service = None
    
    def _get_service(self):
        """Get or create Classroom service"""
        if not self.service:
            credentials = self.auth.get_credentials()
            if not credentials:
                raise Exception('Not authenticated')
            
            self.service = build('classroom', 'v1', credentials=credentials)
        
        return self.service
    
    def get_courses(self):
        """Fetch all courses for teacher"""
        service = self._get_service()
        
        courses = []
        page_token = None
        
        while True:
            results = service.courses().list(
                teacherId='me',
                courseStates=['ACTIVE'],
                pageSize=100,
                pageToken=page_token
            ).execute()
            
            courses.extend(results.get('courses', []))
            page_token = results.get('nextPageToken')
            
            if not page_token:
                break
        
        return courses
    
    def get_course(self, course_id):
        """Get specific course"""
        service = self._get_service()
        return service.courses().get(id=course_id).execute()
    
    def get_students(self, course_id):
        """Get students in a course"""
        service = self._get_service()
        
        students = []
        page_token = None
        
        while True:
            results = service.courses().students().list(
                courseId=course_id,
                pageSize=100,
                pageToken=page_token
            ).execute()
            
            students.extend(results.get('students', []))
            page_token = results.get('nextPageToken')
            
            if not page_token:
                break
        
        return students
    
    def get_coursework(self, course_id):
        """Get assignments for a course"""
        service = self._get_service()
        
        coursework = []
        page_token = None
        
        while True:
            results = service.courses().courseWork().list(
                courseId=course_id,
                courseWorkStates=['PUBLISHED'],
                pageSize=100,
                pageToken=page_token
            ).execute()
            
            coursework.extend(results.get('courseWork', []))
            page_token = results.get('nextPageToken')
            
            if not page_token:
                break
        
        return coursework
    
    def get_submissions(self, course_id, coursework_id):
        """Get submissions for an assignment"""
        service = self._get_service()
        
        submissions = []
        page_token = None
        
        while True:
            results = service.courses().courseWork().studentSubmissions().list(
                courseId=course_id,
                courseWorkId=coursework_id,
                pageSize=100,
                pageToken=page_token
            ).execute()
            
            submissions.extend(results.get('studentSubmissions', []))
            page_token = results.get('nextPageToken')
            
            if not page_token:
                break
        
        return submissions
    
    def get_all_submissions(self, course_id, coursework_ids):
        """Get submissions for multiple assignments"""
        all_submissions = {}
        
        for coursework_id in coursework_ids:
            submissions = self.get_submissions(course_id, coursework_id)
            all_submissions[coursework_id] = submissions
        
        return all_submissions
