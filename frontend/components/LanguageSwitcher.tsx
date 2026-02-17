'use client';

import { useLanguage } from '@/lib/LanguageContext';
import { useJurisdiction } from '@/contexts/JurisdictionContext';
import { Globe } from 'lucide-react';
import { useState, useRef, useEffect } from 'react';

const ALL_LANGUAGES = {
    sk: { code: 'sk', label: 'Slovenčina', flag: '🇸🇰' },
    cs: { code: 'cs', label: 'Čeština', flag: '🇨🇿' },
    pl: { code: 'pl', label: 'Polski', flag: '🇵🇱' },
    en: { code: 'en', label: 'English', flag: '🇬🇧' },
    de: { code: 'de', label: 'Deutsch', flag: '🇩🇪' },
    fr: { code: 'fr', label: 'Français', flag: '🇫🇷' },
    es: { code: 'es', label: 'Español', flag: '🇪🇸' },
    uk: { code: 'uk', label: 'Українська', flag: '🇺🇦' },
    it: { code: 'it', label: 'Italiano', flag: '🇮🇹' },
    ru: { code: 'ru', label: 'Русский', flag: '🇷🇺' },
    pt: { code: 'pt', label: 'Português', flag: '🇵🇹' },
} as const;

export default function LanguageSwitcher() {
    const { language, setLanguage } = useLanguage();
    const { currentJurisdiction } = useJurisdiction();
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);

    // Get languages in order based on jurisdiction
    const languages = currentJurisdiction.languages.map(code => ALL_LANGUAGES[code as keyof typeof ALL_LANGUAGES]);

    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        }
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const currentLanguage = languages.find(l => l.code === language) || languages[0];

    return (
        <div className="relative" ref={dropdownRef}>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center space-x-2 px-3 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 transition-colors text-white border border-blue-700"
            >
                <Globe className="w-4 h-4" />
                <span className="hidden sm:inline">{currentLanguage.label}</span>
                <span className="sm:hidden">{currentLanguage.flag}</span>
            </button>

            {isOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-slate-900 border border-white/10 rounded-xl shadow-xl overflow-hidden z-50 backdrop-blur-xl">
                    <div className="py-1">
                        {languages.map((lang) => (
                            <button
                                key={lang.code}
                                onClick={() => {
                                    setLanguage(lang.code as any);
                                    setIsOpen(false);
                                }}
                                className={`w-full text-left px-4 py-3 text-sm flex items-center space-x-3 hover:bg-white/10 transition-colors ${language === lang.code ? 'bg-white/5 text-purple-400' : 'text-gray-300'
                                    }`}
                            >
                                <span className="text-lg">{lang.flag}</span>
                                <span>{lang.label}</span>
                            </button>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
