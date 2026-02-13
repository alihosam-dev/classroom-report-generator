import api from '@/lib/api';

export const authService = {
  async getAuthUrl() {
    const response = await api.get('/api/auth/login');
    return response.data.auth_url;
  },

  async handleCallback(code: string) {
    const response = await api.post('/api/auth/callback', { code });
    return response.data;
  },

  async checkStatus() {
    const response = await api.get('/api/auth/status');
    return response.data;
  },

  async logout() {
    const response = await api.post('/api/auth/logout');
    return response.data;
  },
};

export const courseService = {
  async getCourses() {
    const response = await api.get('/api/courses/');
    return response.data.courses;
  },

  async getCourse(courseId: string) {
    const response = await api.get(`/api/courses/${courseId}`);
    return response.data.course;
  },

  async getStudents(courseId: string) {
    const response = await api.get(`/api/courses/${courseId}/students`);
    return response.data.students;
  },

  async getCoursework(courseId: string) {
    const response = await api.get(`/api/courses/${courseId}/coursework`);
    return response.data.coursework;
  },
};

export const reportService = {
  async generateReport(data: {
    course_id: string;
    coursework_ids: string[];
    include_grades: boolean;
  }) {
    const response = await api.post('/api/reports/generate', data);
    return response.data;
  },

  async downloadFile(filename: string) {
    const response = await api.get(`/api/reports/download/${filename}`, {
      responseType: 'blob',
    });
    return response.data;
  },

  async listReports() {
    const response = await api.get('/api/reports/list');
    return response.data.files;
  },
};
