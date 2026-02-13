'use client';

import { useLocale } from './LocaleProvider';

export default function LanguageSwitcher() {
  const { locale, setLocale, isRTL } = useLocale();

  return (
    <div className="flex items-center gap-2 bg-gray-100 rounded-lg p-1">
      <button
        onClick={() => setLocale('en')}
        className={`px-3 py-1 rounded-md text-sm font-medium transition ${
          locale === 'en'
            ? 'bg-white text-blue-600 shadow-sm'
            : 'text-gray-600 hover:text-gray-900'
        }`}
      >
        English
      </button>
      <button
        onClick={() => setLocale('ar')}
        className={`px-3 py-1 rounded-md text-sm font-medium transition ${
          locale === 'ar'
            ? 'bg-white text-blue-600 shadow-sm'
            : 'text-gray-600 hover:text-gray-900'
        }`}
      >
        العربية
      </button>
    </div>
  );
}
