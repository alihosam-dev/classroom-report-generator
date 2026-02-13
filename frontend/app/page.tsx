'use client';

import { useState, useEffect } from 'react';
import { authService, courseService, reportService } from '@/lib/services';
import { mockService } from '@/services/mockService';
import { useLocale } from './LocaleProvider';
import LanguageSwitcher from './LanguageSwitcher';
import Avatar from './Avatar';

// Set this to true to use mock data, false for real Google Classroom data
const USE_MOCK_DATA = false;

export default function Home() {
  const { messages: t, isRTL } = useLocale();
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<any>(null);
  const [courses, setCourses] = useState<any[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<string | null>(null);
  const [coursework, setCoursework] = useState<any[]>([]);
  const [selectedCoursework, setSelectedCoursework] = useState<string[]>([]);
  const [includeGrades, setIncludeGrades] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [showAllAssignments, setShowAllAssignments] = useState(false);
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const [showCourseDropdown, setShowCourseDropdown] = useState(false);

  useEffect(() => {
    if (USE_MOCK_DATA) {
      // Skip auth check in mock mode
      setAuthenticated(true);
      setUser({ name: 'Mock User', email: 'mock@test.com', picture: null });
      setLoading(false);
      loadCourses();
    } else {
      checkAuth();
    }
  }, []);

  const checkAuth = async () => {
    try {
      const response = await authService.checkStatus();
      setAuthenticated(response.authenticated);
      setUser(response.user);
      if (response.authenticated) {
        loadCourses();
      }
    } catch (error) {
      console.error('Auth check failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async () => {
    try {
      const authUrl = await authService.getAuthUrl();
      window.location.href = authUrl;
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  const handleLogout = async () => {
    try {
      await authService.logout();
      setAuthenticated(false);
      setUser(null);
      setCourses([]);
      setSelectedCourse(null);
      setCoursework([]);
      setSelectedCoursework([]);
      setResult(null);
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const loadCourses = async () => {
    try {
      const data = USE_MOCK_DATA ? await mockService.getCourses() : await courseService.getCourses();
      setCourses(data);
    } catch (error) {
      console.error('Failed to load courses:', error);
    }
  };

  const handleCourseSelect = async (courseId: string) => {
    setSelectedCourse(courseId);
    setSelectedCoursework([]);
    setResult(null);
    setShowCourseDropdown(false);
    try {
      const data = USE_MOCK_DATA 
        ? await mockService.getCoursework(courseId)
        : await courseService.getCoursework(courseId);
      setCoursework(data);
    } catch (error) {
      console.error('Failed to load coursework:', error);
    }
  };

  const toggleCoursework = (id: string) => {
    setSelectedCoursework(prev =>
      prev.includes(id) ? prev.filter(cw => cw !== id) : [...prev, id]
    );
  };

  const handleGenerate = async () => {
    if (!selectedCourse || selectedCoursework.length === 0) return;

    setGenerating(true);
    try {
      const data = USE_MOCK_DATA
        ? await mockService.generateReport(selectedCourse, selectedCoursework, includeGrades)
        : await reportService.generateReport({
            course_id: selectedCourse,
            coursework_ids: selectedCoursework,
            include_grades: includeGrades,
          });
      setResult(data);
    } catch (error) {
      console.error('Report generation failed:', error);
      alert('Failed to generate report');
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">{t.status?.loading || 'Loading...'}</div>
      </div>
    );
  }

  if (!authenticated || !t.app) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 px-4 py-6">
        <div className="absolute top-4 right-4">
          <LanguageSwitcher />
        </div>
        <div className="bg-white p-6 sm:p-12 rounded-2xl shadow-2xl max-w-2xl w-full" style={{ fontFamily: '-apple-system, "SF Pro Display", "Avenir Next", Avenir, system-ui, sans-serif' }}>
          <div className="text-center mb-6 sm:mb-8">
            <div className="mb-3 sm:mb-4 flex justify-center">
              <svg className="w-12 h-12 sm:w-16 sm:h-16" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="8" y="12" width="48" height="44" rx="2" fill="#2E5090"/>
                <rect x="12" y="8" width="48" height="44" rx="2" fill="#4472C4"/>
                <rect x="16" y="4" width="48" height="44" rx="2" fill="#5B9BD5"/>
                <path d="M20 16 L24 16 L24 40 L20 40 Z" fill="white" opacity="0.9"/>
                <path d="M28 20 L56 20 L56 22 L28 22 Z" fill="white" opacity="0.9"/>
                <path d="M28 26 L52 26 L52 28 L28 28 Z" fill="white" opacity="0.9"/>
                <path d="M28 32 L48 32 L48 34 L28 34 Z" fill="white" opacity="0.9"/>
              </svg>
            </div>
            <h1 className="text-2xl sm:text-4xl font-bold text-gray-800 mb-3 sm:mb-4" style={{ fontFamily: '-apple-system, "SF Pro Display", "Avenir Next", Avenir, system-ui, sans-serif' }}>
              {t.app?.title}
            </h1>
            <p className="text-base sm:text-lg text-gray-600 mb-4 sm:mb-6" style={{ fontFamily: '-apple-system, "SF Pro Display", "Avenir Next", Avenir, system-ui, sans-serif' }}>
              {t.app?.subtitle}
            </p>
          </div>
          
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-4 sm:p-6 mb-6 sm:mb-8">
            <h2 className="text-base sm:text-xl font-semibold text-gray-800 mb-3 sm:mb-4 flex items-center gap-2" style={{ fontFamily: '-apple-system, "SF Pro Display", "Avenir Next", Avenir, system-ui, sans-serif' }}>
              <svg className="w-4 h-4 sm:w-5 sm:h-5 flex-shrink-0" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" fill="#5B9BD5" stroke="#4472C4" strokeWidth="2" strokeLinejoin="round"/>
              </svg>
              {t.splash?.whatItDoes}
            </h2>
            <ul className="space-y-2 sm:space-y-3 text-gray-700 text-sm sm:text-base" style={{ fontFamily: '-apple-system, "SF Pro Display", "Avenir Next", Avenir, system-ui, sans-serif' }}>
              <li className="flex items-start">
                <svg className="w-4 h-4 sm:w-5 sm:h-5 text-green-600 mr-2 sm:mr-3 mt-0.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                <span>{t.splash?.features?.connect}</span>
              </li>
              <li className="flex items-start">
                <svg className="w-4 h-4 sm:w-5 sm:h-5 text-green-600 mr-2 sm:mr-3 mt-0.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                <span>{t.splash?.features?.select}</span>
              </li>
              <li className="flex items-start">
                <svg className="w-4 h-4 sm:w-5 sm:h-5 text-green-600 mr-2 sm:mr-3 mt-0.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                <span>{t.splash?.features?.excel}</span>
              </li>
              <li className="flex items-start">
                <svg className="w-4 h-4 sm:w-5 sm:h-5 text-green-600 mr-2 sm:mr-3 mt-0.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                <span>{t.splash?.features?.reportCards}</span>
              </li>
              <li className="flex items-start">
                <svg className="w-4 h-4 sm:w-5 sm:h-5 text-green-600 mr-2 sm:mr-3 mt-0.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                <span>{t.splash?.features?.view}</span>
              </li>
            </ul>
          </div>

          <button
            onClick={handleLogin}
            className="w-full bg-blue-600 text-white py-4 px-6 rounded-xl font-semibold text-lg hover:bg-blue-700 transition shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 flex items-center justify-center gap-3"
            style={{ fontFamily: '-apple-system, "SF Pro Display", "Avenir Next", Avenir, system-ui, sans-serif' }}
          >
            <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            {t.splash?.signIn}
          </button>
          
          <p className="text-center text-sm text-gray-500 mt-6" style={{ fontFamily: '-apple-system, "SF Pro Display", "Avenir Next", Avenir, system-ui, sans-serif' }}>
            {t.splash?.privacyNote}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header with Profile */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-3 sm:px-4 py-2 flex items-center justify-between">
          <div className="flex-1 min-w-0">
            <h1 className="text-sm sm:text-xl font-bold text-gray-800 truncate">
              <span className="sm:hidden">Report Generator</span>
              <span className="hidden sm:inline">{t.app?.title}</span>
            </h1>
            <p className="text-xs text-gray-600 hidden sm:block">{t.app?.tagline}</p>
          </div>
          
          <div className="flex items-center gap-2 sm:gap-3 flex-shrink-0">
            <LanguageSwitcher />
            
            {/* Profile Menu */}
            {user && (
              <div className="relative">
                <button
                  onClick={() => setShowProfileMenu(!showProfileMenu)}
                  className="flex items-center gap-1 sm:gap-2 hover:bg-gray-50 rounded-lg px-1 sm:px-2 py-1 transition"
                >
                  <div className={`text-${isRTL ? 'left' : 'right'} hidden sm:block`}>
                    <div className="text-xs font-medium text-gray-900">{user.name}</div>
                    <div className="text-[10px] text-gray-500">{user.email}</div>
                  </div>
                  <Avatar name={user.name} picture={user.picture} size="sm" />
                </button>
                
                {showProfileMenu && (
                  <div className={`absolute ${isRTL ? 'left-0' : 'right-0'} mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1`}>
                    <button
                      onClick={handleLogout}
                      className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center gap-2"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                      </svg>
                      {t.header?.signOut}
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-3 sm:px-4 py-3 sm:py-4">

        {/* Course Selection */}
        <div className="bg-white rounded-lg shadow p-3 sm:p-4 mb-3 sm:mb-4">
          <h2 className="text-base sm:text-lg font-semibold mb-2 sm:mb-3 text-gray-900">{t.courses?.step} {t.courses?.title}</h2>
          <div className="relative">
            <button
              onClick={() => setShowCourseDropdown(!showCourseDropdown)}
              className="w-full p-3 rounded-lg border-2 border-gray-300 hover:border-blue-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition text-sm text-gray-900 bg-white flex items-center justify-between"
              style={{ fontFamily: '-apple-system, "SF Pro Display", "Avenir Next", Avenir, system-ui, sans-serif' }}
            >
              <span className={selectedCourse ? 'text-gray-900' : 'text-gray-500'}>
                {selectedCourse 
                  ? (() => {
                      const course = courses.find(c => c.id === selectedCourse);
                      return course ? `${course.name}${course.section ? ' - ' + course.section : ''}` : 'Select a course...';
                    })()
                  : 'Select a course...'}
              </span>
              <svg 
                className={`w-5 h-5 text-gray-600 transition-transform ${showCourseDropdown ? 'rotate-180' : ''}`} 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            
            {showCourseDropdown && (
              <>
                {/* Backdrop */}
                <div 
                  className="fixed inset-0 z-10" 
                  onClick={() => setShowCourseDropdown(false)}
                />
                
                {/* Dropdown menu */}
                <div className="absolute z-20 w-full mt-2 bg-white rounded-lg shadow-lg border border-gray-200 max-h-64 overflow-y-auto">
                  {courses.map(course => (
                    <button
                      key={course.id}
                      onClick={() => handleCourseSelect(course.id)}
                      className={`w-full text-left px-4 py-3 hover:bg-blue-50 transition flex items-center justify-between border-b border-gray-100 last:border-b-0 ${
                        selectedCourse === course.id ? 'bg-blue-50' : ''
                      }`}
                      style={{ fontFamily: '-apple-system, "SF Pro Display", "Avenir Next", Avenir, system-ui, sans-serif' }}
                    >
                      <div>
                        <div className="font-semibold text-sm text-gray-900">{course.name}</div>
                        <div className="text-xs text-gray-600">{course.section}</div>
                      </div>
                      {selectedCourse === course.id && (
                        <svg className="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      )}
                    </button>
                  ))}
                </div>
              </>
            )}
          </div>
        </div>

        {/* Assignment Selection */}
        {selectedCourse && coursework.length > 0 && (
          <div className="bg-white rounded-lg shadow p-3 sm:p-4 mb-3 sm:mb-4">
            <div className="flex items-center justify-between mb-2 sm:mb-3">
              <h2 className="text-base sm:text-lg font-semibold text-gray-900">{t.assignments?.step} {t.assignments?.title}</h2>
              <span className="text-xs text-gray-600">
                {selectedCoursework.length} {t.assignments?.selected?.replace('{total}', coursework.length.toString())}
              </span>
            </div>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {(showAllAssignments ? coursework : coursework.slice(0, 5)).map(cw => (
                <label 
                  key={cw.id} 
                  className="flex items-center p-2 hover:bg-gray-50 rounded-lg border border-gray-200 cursor-pointer transition group"
                >
                  <input
                    type="checkbox"
                    checked={selectedCoursework.includes(cw.id)}
                    onChange={() => toggleCoursework(cw.id)}
                    className={`${isRTL ? 'ml-3' : 'mr-3'} w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500`}
                  />
                  <div className="flex-1">
                    <span className="text-sm font-medium text-gray-800 group-hover:text-blue-600 transition">
                      {cw.title}
                    </span>
                  </div>
                  {cw.maxPoints && (
                    <span className={`${isRTL ? 'mr-3' : 'ml-3'} px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-xs font-medium`}>
                      {cw.maxPoints} {t.assignments?.points}
                    </span>
                  )}
                </label>
              ))}
            </div>
            {coursework.length > 5 && (
              <button
                onClick={() => setShowAllAssignments(!showAllAssignments)}
                className="mt-3 w-full py-1.5 text-blue-600 hover:text-blue-700 font-medium text-xs transition"
              >
                {showAllAssignments ? `▲ ${t.assignments?.showLess}` : `▼ ${t.assignments?.showAll?.replace('{count}', (coursework.length - 5).toString())}`}
              </button>
            )}
          </div>
        )}

        {/* Options & Generate */}
        {selectedCoursework.length > 0 && (
          <div className="bg-white rounded-lg shadow p-3 sm:p-4">
            <h2 className="text-base sm:text-lg font-semibold mb-2 sm:mb-3 text-gray-900">{t.generate?.step} {t.generate?.title}</h2>
            <label className="flex items-center mb-3 sm:mb-4 cursor-pointer">
              <input
                type="checkbox"
                checked={includeGrades}
                onChange={e => setIncludeGrades(e.target.checked)}
                className={`${isRTL ? 'ml-2' : 'mr-2'} w-4 h-4`}
              />
              <span className="text-sm text-gray-900">{t.generate?.includeGrades}</span>
            </label>
            <button
              onClick={handleGenerate}
              disabled={generating}
              className="w-full sm:w-auto bg-blue-600 text-white py-2 px-6 rounded-lg text-sm font-semibold hover:bg-blue-700 transition disabled:bg-gray-400"
            >
              {generating ? t.generate?.generating : t.generate?.button}
            </button>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="space-y-3 sm:space-y-4 mt-3 sm:mt-4">
            {/* Report Data Table */}
            {result.report_data && result.report_data.length > 0 && (
              <div className="bg-white rounded-xl shadow-lg p-3 sm:p-4">
                <h3 className="text-base sm:text-lg font-bold text-gray-800 mb-2 sm:mb-3 flex items-center gap-2">
                  <svg className="w-4 h-4 sm:w-5 sm:h-5 text-blue-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  <span className="truncate">{t.results?.title}</span>
                </h3>
                <div className="overflow-x-auto -mx-3 sm:mx-0">
                  <div className="inline-block min-w-full align-middle">
                    <div className="overflow-hidden">
                      <table className="min-w-full divide-y divide-gray-200 text-xs">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className={`px-3 py-2 text-${isRTL ? 'right' : 'left'} text-[10px] font-medium text-gray-500 uppercase tracking-wider`}>
                          {t.results?.tableHeaders?.student}
                        </th>
                        {result.report_data[0].grades.map((g: any, idx: number) => (
                          <th key={idx} className={`px-3 py-2 text-${isRTL ? 'right' : 'left'} text-[10px] font-medium text-gray-500 uppercase tracking-wider`}>
                            {g.assignment}
                          </th>
                        ))}
                        <th className={`px-3 py-2 text-${isRTL ? 'right' : 'left'} text-[10px] font-medium text-gray-500 uppercase tracking-wider bg-blue-50`}>
                          {t.results?.tableHeaders?.average}
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {result.report_data.map((student: any, idx: number) => (
                        <tr key={idx} className="hover:bg-gray-50">
                          <td className="px-3 py-2 whitespace-nowrap">
                            <div className="text-xs font-medium text-gray-900">{student.name}</div>
                            <div className="text-[10px] text-gray-500">{student.email}</div>
                          </td>
                          {student.grades.map((g: any, gIdx: number) => (
                            <td key={gIdx} className="px-3 py-2 whitespace-nowrap text-xs text-gray-900">
                              {g.display === 'Not Graded Yet' ? t.status?.notGraded : 
                               g.display === 'Not Submitted' ? t.status?.notSubmitted : g.display}
                            </td>
                          ))}
                          <td className="px-3 py-2 whitespace-nowrap text-xs font-bold text-blue-600 bg-blue-50">
                            {student.average}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Analysis Section */}
            {result.analysis && (
              <div className="bg-white rounded-xl shadow-lg p-3 sm:p-4">
                <h3 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
                  <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                  {t.results?.analysis?.title}
                </h3>
                
                {/* Class Statistics */}
                {result.analysis.class_stats && (
                  <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-3 mb-3">
                    <h4 className="text-sm font-semibold text-gray-800 mb-2">{t.results?.analysis?.classStats}</h4>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                      <div className="bg-white rounded-lg p-2 shadow-sm">
                        <div className="text-[10px] text-gray-600 mb-0.5">{t.results?.analysis?.average}</div>
                        <div className="text-lg font-bold text-blue-600">{result.analysis.class_stats.average}</div>
                      </div>
                      <div className="bg-white rounded-lg p-2 shadow-sm">
                        <div className="text-[10px] text-gray-600 mb-0.5">{t.results?.analysis?.highest}</div>
                        <div className="text-lg font-bold text-green-600">{result.analysis.class_stats.highest}</div>
                      </div>
                      <div className="bg-white rounded-lg p-2 shadow-sm">
                        <div className="text-[10px] text-gray-600 mb-0.5">{t.results?.analysis?.lowest}</div>
                        <div className="text-lg font-bold text-orange-600">{result.analysis.class_stats.lowest}</div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Key Insights */}
                {result.analysis.insights && result.analysis.insights.length > 0 && (
                  <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-3 mb-3">
                    <h4 className="text-sm font-semibold text-gray-800 mb-2 flex items-center gap-2">
                      <svg className="w-4 h-4 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z" />
                      </svg>
                      {t.results?.analysis?.insights}
                    </h4>
                    <ul className="space-y-1.5">
                      {result.analysis.insights.map((insight: any, idx: number) => {
                        const insightKey = insight.key;
                        const insightValue = insight.value;
                        let message = (t.results?.analysis?.insightMessages as any)?.[insightKey] || '';
                        
                        // Replace placeholders
                        if (insightValue !== null) {
                          message = message.replace('{count}', insightValue).replace('{spread}', insightValue);
                        }
                        
                        return (
                          <li key={idx} className="flex items-start gap-2">
                            <span className="text-purple-600 text-xs mt-0.5">•</span>
                            <span className="text-xs text-gray-700">{message}</span>
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                )}

                {/* Assignment Performance */}
                {result.analysis.assignments && result.analysis.assignments.length > 0 && (
                  <div>
                    <h4 className="text-sm font-semibold text-gray-800 mb-2">{t.results?.analysis?.assignments}</h4>
                    <div className="overflow-x-auto">
                      <table className="min-w-full divide-y divide-gray-200 text-xs">
                        <thead className="bg-gray-50">
                          <tr>
                            <th className={`px-3 py-2 text-${isRTL ? 'right' : 'left'} text-[10px] font-medium text-gray-500 uppercase`}>
                              Assignment
                            </th>
                            <th className={`px-3 py-2 text-${isRTL ? 'right' : 'left'} text-[10px] font-medium text-gray-500 uppercase`}>
                              {t.results?.analysis?.average}
                            </th>
                            <th className={`px-3 py-2 text-${isRTL ? 'right' : 'left'} text-[10px] font-medium text-gray-500 uppercase`}>
                              {t.results?.analysis?.highest}
                            </th>
                            <th className={`px-3 py-2 text-${isRTL ? 'right' : 'left'} text-[10px] font-medium text-gray-500 uppercase`}>
                              {t.results?.analysis?.lowest}
                            </th>
                            <th className={`px-3 py-2 text-${isRTL ? 'right' : 'left'} text-[10px] font-medium text-gray-500 uppercase`}>
                              {t.results?.analysis?.graded}
                            </th>
                          </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                          {result.analysis.assignments.map((assignment: any, idx: number) => (
                            <tr key={idx} className="hover:bg-gray-50">
                              <td className="px-3 py-2 text-xs font-medium text-gray-900">{assignment.title}</td>
                              <td className="px-3 py-2 text-xs text-gray-900">{assignment.average}</td>
                              <td className="px-3 py-2 text-xs text-green-600">{assignment.highest}</td>
                              <td className="px-3 py-2 text-xs text-orange-600">{assignment.lowest}</td>
                              <td className="px-3 py-2 text-xs text-gray-900">
                                {assignment.graded}/{assignment.submissions}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Download Section */}
            <div className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-500 rounded-xl shadow-lg p-3 sm:p-4">
              <div className="flex flex-col sm:flex-row items-start justify-between mb-2 sm:mb-3 gap-2">
                <div>
                  <h3 className="text-base sm:text-lg font-bold text-green-800 mb-1 flex items-center">
                    <span className={`${isRTL ? 'ml-2' : 'mr-2'}`}>✓</span> {t.results?.success}
                  </h3>
                  <p className="text-xs sm:text-sm text-green-700">{result.message}</p>
                </div>
              </div>
              <div className="bg-white rounded-lg p-3 mt-2 sm:mt-3 space-y-3">
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-3 border-b gap-2">
                  <div className="flex-1 min-w-0">
                    <p className="text-xs text-gray-600 mb-0.5">{t.results?.excelLabel}</p>
                    <p className="text-xs sm:text-sm font-semibold text-gray-800 truncate">{result.excel_file}</p>
                  </div>
                  <a
                    href={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001'}/api/reports/download/${encodeURIComponent(result.excel_file)}`}
                    download
                    className="w-full sm:w-auto flex items-center justify-center gap-2 bg-blue-600 text-white px-3 sm:px-4 py-2 rounded-lg text-xs font-semibold hover:bg-blue-700 transition shadow-md flex-shrink-0"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    {t.results?.downloadExcel}
                  </a>
                </div>
                {result.report_cards && result.report_cards.length > 0 && (
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-xs text-gray-600 mb-0.5">{t.results?.reportCardsLabel}</p>
                      <p className="text-sm font-semibold text-gray-800">{result.report_cards.length} {t.results?.students}</p>
                    </div>
                    <a
                      href={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001'}/api/reports/download-cards/${result.report_id}`}
                      download
                      className="flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg text-xs font-semibold hover:bg-green-700 transition shadow-md"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                      </svg>
                      {t.results?.downloadCards}
                    </a>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
