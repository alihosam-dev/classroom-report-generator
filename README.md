# 📚 Classroom Report Generator

A web application for generating comprehensive grade reports from Google Classroom. Create Excel spreadsheets with statistical analysis and visual report cards for each student.

## ✨ Features

- 🎓 **Course Selection**: Browse and select from your Google Classroom courses
- 📝 **Assignment Selection**: Choose specific assignments to include in reports  
- 📊 **Excel Reports**: Generate spreadsheets with raw grades and statistical analysis
- 🎨 **Student Report Cards**: Create visual report cards as images for each student
- 🔒 **Secure**: OAuth 2.0 authentication via Google
- 🌐 **Web-based**: Access from any device with a browser

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.8+
- Google account with Google Classroom access (teacher account)
- Google Cloud project with Classroom API enabled

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ClassroomReportGenerator.git
   cd ClassroomReportGenerator
   ```

2. **Install backend dependencies**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Set up Google Cloud credentials** (See Setup Guide below)

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

### Running the Application

**Start the backend server:**
```bash
cd backend
source venv/bin/activate
python app.py
```

**Start the frontend development server:**
```bash
cd frontend
npm run dev
```

Visit `http://localhost:3000` in your browser.

## 📖 Setup Guide

### 1. Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select an existing one
3. Enable the **Google Classroom API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Classroom API"
   - Click "Enable"

### 2. OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop app" as application type
4. Download the JSON file
5. Rename it to `credentials.json`
6. Place it in the project root directory

### 3. OAuth Consent Screen

Configure the consent screen with these scopes:
- `https://www.googleapis.com/auth/classroom.courses.readonly`
- `https://www.googleapis.com/auth/classroom.coursework.students.readonly`
- `https://www.googleapis.com/auth/classroom.rosters.readonly`
- `https://www.googleapis.com/auth/classroom.profile.emails`
- `https://www.googleapis.com/auth/classroom.student-submissions.students.readonly`

### 4. First Run

On first run, the app will:
1. Open your browser for Google authentication
2. Request permission to access your Classroom data
3. Save a token locally for future use

## 📂 Project Structure

```
ClassroomReportGenerator/
├── frontend/          # React application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API service layer
│   │   ├── hooks/         # Custom React hooks
│   │   └── utils/         # Utility functions
│   └── public/
├── backend/           # Python Flask API
│   ├── app.py         # Main application
│   ├── routes/        # API endpoints
│   ├── services/      # Business logic
│   │   ├── auth/      # Google OAuth
│   │   ├── classroom/ # Classroom API client
│   │   └── export/    # Report generation
│   └── utils/         # Helper functions
└── output/            # Generated reports (not in git)
```

## 🛠️ Development

### Running Tests

**Backend tests:**
```bash
cd backend
pytest tests/
```

**Frontend tests:**
```bash
cd frontend
npm test
```

### Code Style

**Backend:** PEP 8
```bash
black backend/
flake8 backend/
```

**Frontend:** ESLint + Prettier
```bash
cd frontend
npm run lint
```

## 📊 Output Examples

### Excel File Structure

**Sheet 1: Raw Grades**
| Student Name | Assignment 1 | Assignment 2 | Assignment 3 | Average |
|--------------|-------------|-------------|-------------|---------|
| John Doe     | 95          | 87          | 92          | 91.33   |
| Jane Smith   | 88          | 95          | 90          | 91.00   |

**Sheet 2: Analysis**
- Class statistics per assignment
- Grade distribution charts
- Performance trends
- Summary statistics

### Report Cards
Each student gets a PNG image with:
- Student name and course information
- List of assignments and grades
- Visual grade chart
- Overall average

## 🔒 Security & Privacy

- **Never commit** `credentials.json` or `token.json`
- Student data is only stored temporarily during processing
- All API communication uses HTTPS
- OAuth tokens are stored securely locally

## 🐛 Troubleshooting

### "Invalid credentials" error
- Regenerate `credentials.json` from Google Cloud Console
- Ensure the OAuth client ID is for "Desktop app"

### "Access denied" error
- Verify all required scopes are added to OAuth consent screen
- Delete `token.json` and re-authenticate

### No courses showing
- Ensure you're logged in as a teacher
- Check that courses are active (not archived)

### Rate limit errors
- The app includes automatic retry logic
- For large courses, requests are batched

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Follow coding standards
4. Add tests for new features
5. Submit a pull request

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section above

## 🛠️ Built With

**Frontend:**
- React
- Tailwind CSS
- Axios

**Backend:**
- Flask
- Google Classroom API
- pandas
- openpyxl
- Pillow

---

**Note**: This project is not affiliated with or endorsed by Google LLC.
