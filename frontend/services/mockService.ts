const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001';

export const mockService = {
  async getCourses() {
    const response = await fetch(`${API_URL}/api/mock/courses`, {
      credentials: 'include',
    });
    if (!response.ok) throw new Error('Failed to fetch mock courses');
    return response.json();
  },

  async getCoursework(courseId: string) {
    const response = await fetch(`${API_URL}/api/mock/courses/${courseId}/coursework`, {
      credentials: 'include',
    });
    if (!response.ok) throw new Error('Failed to fetch mock coursework');
    return response.json();
  },

  async generateReport(courseId: string, courseworkIds: string[], includeGrades: boolean = true) {
    const response = await fetch(`${API_URL}/api/mock/reports/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({
        courseId,
        courseworkIds,
        includeGrades,
      }),
    });
    if (!response.ok) throw new Error('Failed to generate mock report');
    return response.json();
  },
};
