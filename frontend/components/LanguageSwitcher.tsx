'use client';

import { useLanguage } from '@/lib/LanguageContext';
import { useJurisdiction, JURISDICTIONS, JurisdictionCode } from '@/contexts/JurisdictionContext';
import { Globe, ChevronDown } from 'lucide-react';
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
    const { jurisdiction, setJurisdiction, currentJurisdiction } = useJurisdiction();
    const [isOpen, setIsOpen] = useState(false);
    const [activeTab, setActiveTab] = useState<'language' | 'country'>('language');
    const dropdownRef = useRef<HTMLDivElement>(null);

    const languages = currentJurisdiction.languages.map(code => ALL_LANGUAGES[code as keyof typeof ALL_LANGUAGES]);
    const jurisdictions = Object.values(JURISDICTIONS);

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
                className="flex items-center space-x-1.5 px-2.5 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-700 transition-colors text-white border border-blue-700 text-sm"
            >
                <span className="text-sm">{currentJurisdiction.flag}</span>
                <Globe className="w-3.5 h-3.5" />
                <ChevronDown className="w-3 h-3" />
            </button>

            {isOpen && (
                <div className="absolute right-0 mt-2 w-56 bg-slate-900 border border-white/10 rounded-xl shadow-xl overflow-hidden z-50 backdrop-blur-xl">
                    {/* Tabs */}
                    <div className="flex border-b border-white/10">
                        <button
                            onClick={() => setActiveTab('language')}
                            className={`flex-1 px-3 py-2.5 text-xs font-semibold uppercase tracking-wide transition-colors ${
                                activeTab === 'language'
                                    ? 'text-blue-400 border-b-2 border-blue-400 bg-white/5'
                                    : 'text-gray-400 hover:text-gray-200'
                            }`}
                        >
                            Language
                        </button>
                        <button
                            onClick={() => setActiveTab('country')}
                            className={`flex-1 px-3 py-2.5 text-xs font-semibold uppercase tracking-wide transition-colors ${
                                activeTab === 'country'
                                    ? 'text-blue-400 border-b-2 border-blue-400 bg-white/5'
                                    : 'text-gray-400 hover:text-gray-200'
                            }`}
                        >
                            Country
                        </button>
                    </div>

                    {/* Language list */}
                    {activeTab === 'language' && (
                        <div className="py-1 max-h-64 overflow-y-auto">
                            {languages.map((lang) => (
                                <button
                                    key={lang.code}
                                    onClick={() => {
                                        setLanguage(lang.code as any);
                                        setIsOpen(false);
                                    }}
                                    className={`w-full text-left px-4 py-2.5 text-sm flex items-center space-x-3 hover:bg-white/10 transition-colors ${
                                        language === lang.code ? 'bg-white/5 text-blue-400' : 'text-gray-300'
                                    }`}
                                >
                                    <span className="text-lg">{lang.flag}</span>
                                    <span>{lang.label}</span>
                                </button>
                            ))}
                        </div>
                    )}

                    {/* Country list */}
                    {activeTab === 'country' && (
                        <div className="py-1 max-h-64 overflow-y-auto">
                            {jurisdictions.map((j) => (
                                <button
                                    key={j.code}
                                    onClick={() => {
                                        setJurisdiction(j.code as JurisdictionCode);
                                        setIsOpen(false);
                                        window.dispatchEvent(new CustomEvent('codex_language_update', { detail: 'check_language_switch' }));
                                    }}
                                    className={`w-full text-left px-4 py-2.5 text-sm flex items-center space-x-3 hover:bg-white/10 transition-colors ${
                                        jurisdiction === j.code ? 'bg-white/5 text-blue-400' : 'text-gray-300'
                                    }`}
                                >
                                    <span>{j.flag}</span>
                                    <span>{j.name}</span>
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
