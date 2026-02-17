'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export type JurisdictionCode = 'SK' | 'CZ' | 'PL' | 'AT' | 'DE' | 'FI' | 'HU' | 'FR' | 'GB' | 'ES' | 'NL' | 'BE' | 'IT' | 'PT' | 'SE' | 'CH' | 'LU' | 'LI' | 'DK' | 'NO' | 'IE' | 'GR' | 'VA' | 'SM' | 'MC' | 'AD' | 'SI' | 'HR';

export interface Jurisdiction {
    code: JurisdictionCode;
    name: string;
    flag: string;
    defaultLanguage: string;
    languages: string[];
}

export const JURISDICTIONS: Record<JurisdictionCode, Jurisdiction> = {
    SK: {
        code: 'SK',
        name: 'Slovenská Republika',
        flag: '🇸🇰',
        defaultLanguage: 'sk',
        languages: ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru', 'pt']
    },
    CZ: {
        code: 'CZ',
        name: 'Česká Republika',
        flag: '🇨🇿',
        defaultLanguage: 'cs',
        languages: ['cs', 'sk', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru', 'pt']
    },
    PL: {
        code: 'PL',
        name: 'Polska',
        flag: '🇵🇱',
        defaultLanguage: 'pl',
        languages: ['pl', 'sk', 'cs', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru', 'pt']
    },
    AT: {
        code: 'AT',
        name: 'Österreich',
        flag: '🇦🇹',
        defaultLanguage: 'de',
        languages: ['de', 'en', 'sk', 'cs', 'pl', 'fr', 'es', 'uk', 'it', 'ru', 'pt']
    },
    DE: {
        code: 'DE',
        name: 'Deutschland',
        flag: '🇩🇪',
        defaultLanguage: 'de',
        languages: ['de', 'en', 'sk', 'cs', 'pl', 'fr', 'es', 'uk', 'it', 'ru', 'pt']
    },
    FI: {
        code: 'FI',
        name: 'Suomi',
        flag: '🇫🇮',
        defaultLanguage: 'en',
        languages: ['en', 'de', 'sk', 'cs', 'pl', 'fr', 'es', 'uk', 'it', 'ru', 'pt']
    },
    HU: {
        code: 'HU',
        name: 'Magyarország',
        flag: '🇭🇺',
        defaultLanguage: 'en',
        languages: ['en', 'de', 'sk', 'cs', 'pl', 'fr', 'es', 'uk', 'it', 'ru', 'pt']
    },
    FR: {
        code: 'FR',
        name: 'France',
        flag: '🇫🇷',
        defaultLanguage: 'fr',
        languages: ['fr', 'en', 'de', 'sk', 'cs', 'pl', 'es', 'uk', 'it', 'ru', 'pt']
    },
    GB: {
        code: 'GB',
        name: 'United Kingdom',
        flag: '🇬🇧',
        defaultLanguage: 'en',
        languages: ['en', 'de', 'sk', 'cs', 'pl', 'fr', 'es', 'uk', 'it', 'ru', 'pt']
    },
    ES: {
        code: 'ES',
        name: 'España',
        flag: '🇪🇸',
        defaultLanguage: 'es',
        languages: ['es', 'en', 'de', 'sk', 'cs', 'pl', 'fr', 'uk', 'it', 'ru', 'pt']
    },
    NL: {
        code: 'NL',
        name: 'Nederland',
        flag: '🇳🇱',
        defaultLanguage: 'en',
        languages: ['en', 'de', 'sk', 'cs', 'pl', 'fr', 'es', 'uk', 'it', 'ru', 'pt']
    },
    BE: {
        code: 'BE',
        name: 'België',
        flag: '🇧🇪',
        defaultLanguage: 'fr',
        languages: ['fr', 'en', 'de', 'sk', 'cs', 'pl', 'es', 'uk', 'it', 'ru', 'pt']
    },
    IT: {
        code: 'IT',
        name: 'Italia',
        flag: '🇮🇹',
        defaultLanguage: 'it',
        languages: ['it', 'en', 'de', 'sk', 'cs', 'pl', 'fr', 'es', 'uk', 'ru', 'pt']
    },
    PT: {
        code: 'PT',
        name: 'Portugal',
        flag: '🇵🇹',
        defaultLanguage: 'en',
        languages: ['en', 'es', 'fr', 'de', 'sk', 'cs', 'pl', 'uk', 'it', 'ru', 'pt']
    },
    SE: {
        code: 'SE',
        name: 'Sverige',
        flag: '🇸🇪',
        defaultLanguage: 'en',
        languages: ['en', 'de', 'sk', 'cs', 'pl', 'fr', 'es', 'uk', 'it', 'ru', 'pt']
    },
    CH: {
        code: 'CH',
        name: 'Schweiz',
        flag: '🇨🇭',
        defaultLanguage: 'de',
        languages: ['de', 'fr', 'it', 'en', 'sk', 'cs', 'pl', 'es', 'uk', 'ru', 'pt']
    },
    LU: {
        code: 'LU',
        name: 'Luxembourg',
        flag: '🇱🇺',
        defaultLanguage: 'fr',
        languages: ['fr', 'de', 'en', 'sk', 'cs', 'pl', 'es', 'uk', 'it', 'ru', 'pt']
    },
    LI: {
        code: 'LI',
        name: 'Liechtenstein',
        flag: '🇱🇮',
        defaultLanguage: 'de',
        languages: ['de', 'en', 'fr', 'sk', 'cs', 'pl', 'es', 'uk', 'it', 'ru', 'pt']
    },
    DK: {
        code: 'DK',
        name: 'Danmark',
        flag: '🇩🇰',
        defaultLanguage: 'en',
        languages: ['en', 'de', 'sk', 'cs', 'pl', 'fr', 'es', 'uk', 'it', 'ru', 'pt']
    },
    NO: {
        code: 'NO',
        name: 'Norge',
        flag: '🇳🇴',
        defaultLanguage: 'en',
        languages: ['en', 'de', 'sk', 'cs', 'pl', 'fr', 'es', 'uk', 'it', 'ru', 'pt']
    },
    IE: {
        code: 'IE',
        name: 'Ireland',
        flag: '🇮🇪',
        defaultLanguage: 'en',
        languages: ['en', 'de', 'sk', 'cs', 'pl', 'fr', 'es', 'uk', 'it', 'ru', 'pt']
    },
    GR: {
        code: 'GR',
        name: 'Ελλάδα',
        flag: '🇬🇷',
        defaultLanguage: 'en',
        languages: ['en', 'de', 'sk', 'cs', 'pl', 'fr', 'es', 'uk', 'it', 'ru', 'pt']
    },
    VA: {
        code: 'VA',
        name: 'Vaticano',
        flag: '🇻🇦',
        defaultLanguage: 'it',
        languages: ['it', 'en', 'de', 'sk', 'cs', 'pl', 'fr', 'es', 'uk', 'ru', 'pt']
    },
    SM: {
        code: 'SM',
        name: 'San Marino',
        flag: '🇸🇲',
        defaultLanguage: 'it',
        languages: ['it', 'en', 'de', 'sk', 'cs', 'pl', 'fr', 'es', 'uk', 'ru', 'pt']
    },
    MC: {
        code: 'MC',
        name: 'Monaco',
        flag: '🇲🇨',
        defaultLanguage: 'fr',
        languages: ['fr', 'en', 'it', 'de', 'sk', 'cs', 'pl', 'es', 'uk', 'ru', 'pt']
    },
    AD: {
        code: 'AD',
        name: 'Andorra',
        flag: '🇦🇩',
        defaultLanguage: 'es',
        languages: ['es', 'fr', 'en', 'de', 'sk', 'cs', 'pl', 'uk', 'it', 'ru', 'pt']
    },
    SI: {
        code: 'SI',
        name: 'Slovenija',
        flag: '🇸🇮',
        defaultLanguage: 'en',
        languages: ['en', 'de', 'it', 'sk', 'cs', 'pl', 'fr', 'es', 'uk', 'ru', 'pt']
    },
    HR: {
        code: 'HR',
        name: 'Hrvatska',
        flag: '🇭🇷',
        defaultLanguage: 'en',
        languages: ['en', 'de', 'it', 'sk', 'cs', 'pl', 'fr', 'es', 'uk', 'ru', 'pt']
    }
};

interface JurisdictionContextType {
    jurisdiction: JurisdictionCode;
    setJurisdiction: (code: JurisdictionCode, switchLanguage?: boolean) => void;
    currentJurisdiction: Jurisdiction;
}

const JurisdictionContext = createContext<JurisdictionContextType | undefined>(undefined);

export function JurisdictionProvider({ children }: { children: ReactNode }) {
    const [jurisdiction, setJurisdictionState] = useState<JurisdictionCode>('SK');

    // Load jurisdiction from localStorage on mount
    useEffect(() => {
        const saved = localStorage.getItem('codex_jurisdiction') as JurisdictionCode;
        if (saved && JURISDICTIONS[saved]) {
            setJurisdictionState(saved);
        }
    }, []);

    const setJurisdiction = (code: JurisdictionCode, switchLanguage: boolean = true) => {
        setJurisdictionState(code);
        localStorage.setItem('codex_jurisdiction', code);

        // Store the flag to switch language
        if (switchLanguage) {
            localStorage.setItem('codex_switch_to_default_lang', JURISDICTIONS[code].defaultLanguage);
        }
    };

    const currentJurisdiction = JURISDICTIONS[jurisdiction];

    return (
        <JurisdictionContext.Provider value={{ jurisdiction, setJurisdiction, currentJurisdiction }}>
            {children}
        </JurisdictionContext.Provider>
    );
}

export function useJurisdiction() {
    const context = useContext(JurisdictionContext);
    if (context === undefined) {
        throw new Error('useJurisdiction must be used within a JurisdictionProvider');
    }
    return context;
}
