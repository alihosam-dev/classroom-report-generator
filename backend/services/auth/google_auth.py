"""
Google OAuth2 authentication handler
"""
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
import json

# Disable HTTPS requirement for local development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

class GoogleAuth:
    SCOPES = [
        'https://www.googleapis.com/auth/classroom.courses.readonly',
        'https://www.googleapis.com/auth/classroom.coursework.students',
        'https://www.googleapis.com/auth/classroom.rosters.readonly',
        'https://www.googleapis.com/auth/classroom.profile.emails',
        'https://www.googleapis.com/auth/classroom.student-submissions.students.readonly',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email'
    ]
    
    def __init__(self):
        self.credentials_file = os.getenv('CREDENTIALS_FILE', 'credentials.json')
        self.token_file = os.getenv('TOKEN_FILE', 'token.json')
        self.redirect_uri = os.getenv('REDIRECT_URI', 'http://localhost:3000/auth/callback')
    
    def get_authorization_url(self):
        """Generate OAuth authorization URL"""
        flow = Flow.from_client_secrets_file(
            self.credentials_file,
            scopes=self.SCOPES,
            redirect_uri=self.redirect_uri
        )
        
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        return auth_url
    
    def exchange_code(self, code):
        """Exchange authorization code for credentials"""
        flow = Flow.from_client_secrets_file(
            self.credentials_file,
            scopes=self.SCOPES,
            redirect_uri=self.redirect_uri
        )
        
        # Allow scope changes - Google may not return all requested scopes
        flow.oauth2session.scope = None
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # Save credentials
        self._save_credentials(credentials)
        
        return self._credentials_to_dict(credentials)
    
    def get_credentials(self):
        """Get stored credentials or None"""
        if not os.path.exists(self.token_file):
            return None
        
        credentials = Credentials.from_authorized_user_file(
            self.token_file, 
            self.SCOPES
        )
        
        # Refresh if expired
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            self._save_credentials(credentials)
        
        return credentials
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        credentials = self.get_credentials()
        return credentials is not None and credentials.valid
    
    def logout(self):
        """Clear stored credentials"""
        if os.path.exists(self.token_file):
            os.remove(self.token_file)
    
    def get_user_info(self):
        """Get user profile information"""
        credentials = self.get_credentials()
        if not credentials:
            return None
        
        try:
            service = build('oauth2', 'v2', credentials=credentials)
            user_info = service.userinfo().get().execute()
            return {
                'email': user_info.get('email'),
                'name': user_info.get('name'),
                'picture': user_info.get('picture')
            }
        except Exception as e:
            print(f"Error fetching user info: {e}")
            return None
    
    def _save_credentials(self, credentials):
        """Save credentials to file"""
        with open(self.token_file, 'w') as token:
            token.write(credentials.to_json())
    
    def _credentials_to_dict(self, credentials):
        """Convert credentials to dictionary"""
        return {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
