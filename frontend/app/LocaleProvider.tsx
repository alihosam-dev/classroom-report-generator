'use client';

import { createContext, useContext, useState, useEffect } from 'react';

type Locale = 'en' | 'ar';

interface LocaleContextType {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  messages: any;
  isRTL: boolean;
}

const LocaleContext = createContext<LocaleContextType | undefined>(undefined);

export function LocaleProvider({ children }: { children: React.ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>('en');
  const [messages, setMessages] = useState<any>({});

  useEffect(() => {
    // Load locale from localStorage
    const saved = localStorage.getItem('locale') as Locale;
    if (saved && (saved === 'en' || saved === 'ar')) {
      setLocaleState(saved);
    }
  }, []);

  useEffect(() => {
    // Load messages for current locale
    import(`@/messages/${locale}.json`).then((m) => setMessages(m.default));
    
    // Update HTML dir and lang attributes
    document.documentElement.dir = locale === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = locale;
    
    // Save to localStorage
    localStorage.setItem('locale', locale);
  }, [locale]);

  const setLocale = (newLocale: Locale) => {
    setLocaleState(newLocale);
  };

  return (
    <LocaleContext.Provider value={{ 
      locale, 
      setLocale, 
      messages,
      isRTL: locale === 'ar'
    }}>
      {children}
    </LocaleContext.Provider>
  );
}

export function useLocale() {
  const context = useContext(LocaleContext);
  if (!context) {
    throw new Error('useLocale must be used within LocaleProvider');
  }
  return context;
}
