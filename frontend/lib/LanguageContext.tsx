'use client';

import React, { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';

// Import all locale files
import en from '@/locales/en/common.json';
import sk from '@/locales/sk/common.json';
import cs from '@/locales/cs/common.json';
import de from '@/locales/de/common.json';
import es from '@/locales/es/common.json';
import fr from '@/locales/fr/common.json';
import it from '@/locales/it/common.json';
import pl from '@/locales/pl/common.json';
import pt from '@/locales/pt/common.json';
import ru from '@/locales/ru/common.json';
import uk from '@/locales/uk/common.json';

const translations: Record<string, Record<string, any>> = {
    en,
    sk,
    cs,
    de,
    es,
    fr,
    it,
    pl,
    pt,
    ru,
    uk,
};

type Language = 'en' | 'sk' | 'cs' | 'de' | 'es' | 'fr' | 'it' | 'pl' | 'pt' | 'ru' | 'uk';

interface LanguageContextType {
    language: Language;
    setLanguage: (lang: Language) => void;
    t: (key: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

function getNestedValue(obj: Record<string, any>, path: string): string | undefined {
    const keys = path.split('.');
    let current: any = obj;
    for (const key of keys) {
        if (current === undefined || current === null) return undefined;
        current = current[key];
    }
    return typeof current === 'string' ? current : undefined;
}

export function LanguageProvider({ children }: { children: ReactNode }) {
    const [language, setLanguageState] = useState<Language>('sk');

    // Load language from localStorage on mount
    useEffect(() => {
        const saved = localStorage.getItem('codex_language') as Language;
        if (saved && translations[saved]) {
            setLanguageState(saved);
        }
    }, []);

    // Listen for jurisdiction language switch requests
    useEffect(() => {
        const checkForLanguageSwitch = () => {
            const switchTo = localStorage.getItem('codex_switch_to_default_lang');
            if (switchTo && translations[switchTo]) {
                setLanguageState(switchTo as Language);
                localStorage.setItem('codex_language', switchTo);
                localStorage.removeItem('codex_switch_to_default_lang');
            }
        };

        // Check on mount and on storage events
        checkForLanguageSwitch();
        window.addEventListener('storage', checkForLanguageSwitch);
        
        // Also check periodically for same-tab changes
        const interval = setInterval(checkForLanguageSwitch, 500);

        return () => {
            window.removeEventListener('storage', checkForLanguageSwitch);
            clearInterval(interval);
        };
    }, []);

    const setLanguage = useCallback((lang: Language) => {
        setLanguageState(lang);
        localStorage.setItem('codex_language', lang);
    }, []);

    const t = useCallback((key: string): string => {
        // Try current language first, then fall back to English, then return the key
        const value = getNestedValue(translations[language], key)
            ?? getNestedValue(translations['en'], key)
            ?? key;
        return value;
    }, [language]);

    return (
        <LanguageContext.Provider value={{ language, setLanguage, t }}>
            {children}
        </LanguageContext.Provider>
    );
}

export function useLanguage() {
    const context = useContext(LanguageContext);
    if (context === undefined) {
        throw new Error('useLanguage must be used within a LanguageProvider');
    }
    return context;
}
