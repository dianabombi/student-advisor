'use client';

import { useJurisdiction, JURISDICTIONS, JurisdictionCode } from '@/contexts/JurisdictionContext';
import { useState, useRef, useEffect } from 'react';

// SVG Flag Components
const FlagSK = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="6" fill="#FFFFFF" />
        <rect y="6" width="24" height="6" fill="#0B4EA2" />
        <rect y="12" width="24" height="6" fill="#EE1C25" />
    </svg>
);

const FlagCZ = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="9" fill="#FFFFFF" />
        <rect y="9" width="24" height="9" fill="#D7141A" />
        <path d="M0 0L12 9L0 18V0Z" fill="#11457E" />
    </svg>
);

const FlagPL = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="9" fill="#FFFFFF" />
        <rect y="9" width="24" height="9" fill="#DC143C" />
    </svg>
);

const FlagAT = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="6" fill="#ED2939" />
        <rect y="6" width="24" height="6" fill="#FFFFFF" />
        <rect y="12" width="24" height="6" fill="#ED2939" />
    </svg>
);

const FlagDE = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="6" fill="#000000" />
        <rect y="6" width="24" height="6" fill="#DD0000" />
        <rect y="12" width="24" height="6" fill="#FFCE00" />
    </svg>
);

const FlagFI = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="18" fill="#FFFFFF" />
        <rect x="6" width="3" height="18" fill="#003580" />
        <rect y="7.5" width="24" height="3" fill="#003580" />
    </svg>
);

const FlagHU = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="6" fill="#CD2A3E" />
        <rect y="6" width="24" height="6" fill="#FFFFFF" />
        <rect y="12" width="24" height="6" fill="#436F4D" />
    </svg>
);

const FlagFR = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="8" height="18" fill="#002395" />
        <rect x="8" width="8" height="18" fill="#FFFFFF" />
        <rect x="16" width="8" height="18" fill="#ED2939" />
    </svg>
);

const FlagGB = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="18" fill="#012169" />
        <path d="M0 0 L24 18 M24 0 L0 18" stroke="#FFFFFF" strokeWidth="3" />
        <path d="M0 0 L24 18 M24 0 L0 18" stroke="#C8102E" strokeWidth="2" />
        <path d="M12 0 V18 M0 9 H24" stroke="#FFFFFF" strokeWidth="5" />
        <path d="M12 0 V18 M0 9 H24" stroke="#C8102E" strokeWidth="3" />
    </svg>
);

const FlagES = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="4.5" fill="#AA151B" />
        <rect y="4.5" width="24" height="9" fill="#F1BF00" />
        <rect y="13.5" width="24" height="4.5" fill="#AA151B" />
    </svg>
);

const FlagNL = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="6" fill="#AE1C28" />
        <rect y="6" width="24" height="6" fill="#FFFFFF" />
        <rect y="12" width="24" height="6" fill="#21468B" />
    </svg>
);

const FlagBE = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="8" height="18" fill="#000000" />
        <rect x="8" width="8" height="18" fill="#FDDA24" />
        <rect x="16" width="8" height="18" fill="#EF3340" />
    </svg>
);

const FlagIT = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="8" height="18" fill="#009246" />
        <rect x="8" width="8" height="18" fill="#FFFFFF" />
        <rect x="16" width="8" height="18" fill="#CE2B37" />
    </svg>
);

const FlagPT = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="9.6" height="18" fill="#006600" />
        <rect x="9.6" width="14.4" height="18" fill="#FF0000" />
    </svg>
);

const FlagSE = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="18" fill="#006AA7" />
        <rect x="7" width="3" height="18" fill="#FECC00" />
        <rect y="7.5" width="24" height="3" fill="#FECC00" />
    </svg>
);

const FlagCH = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="18" fill="#FF0000" />
        <rect x="9" y="5" width="6" height="8" fill="#FFFFFF" />
        <rect x="6" y="7.5" width="12" height="3" fill="#FFFFFF" />
    </svg>
);

const FlagLU = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="6" fill="#ED2939" />
        <rect y="6" width="24" height="6" fill="#FFFFFF" />
        <rect y="12" width="24" height="6" fill="#00A1DE" />
    </svg>
);

const FlagLI = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="9" fill="#002B7F" />
        <rect y="9" width="24" height="9" fill="#CE1126" />
    </svg>
);

const FlagDK = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="18" fill="#C8102E" />
        <rect x="7" width="3" height="18" fill="#FFFFFF" />
        <rect y="7.5" width="24" height="3" fill="#FFFFFF" />
    </svg>
);

const FlagNO = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="18" fill="#BA0C2F" />
        <rect x="6" width="4" height="18" fill="#FFFFFF" />
        <rect y="7" width="24" height="4" fill="#FFFFFF" />
        <rect x="7" width="2" height="18" fill="#00205B" />
        <rect y="8" width="24" height="2" fill="#00205B" />
    </svg>
);

const FlagIE = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="8" height="18" fill="#169B62" />
        <rect x="8" width="8" height="18" fill="#FFFFFF" />
        <rect x="16" width="8" height="18" fill="#FF883E" />
    </svg>
);

const FlagGR = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="2" fill="#0D5EAF" />
        <rect y="2" width="24" height="2" fill="#FFFFFF" />
        <rect y="4" width="24" height="2" fill="#0D5EAF" />
        <rect y="6" width="24" height="2" fill="#FFFFFF" />
        <rect y="8" width="24" height="2" fill="#0D5EAF" />
        <rect y="10" width="24" height="2" fill="#FFFFFF" />
        <rect y="12" width="24" height="2" fill="#0D5EAF" />
        <rect y="14" width="24" height="2" fill="#FFFFFF" />
        <rect y="16" width="24" height="2" fill="#0D5EAF" />
        <rect width="10" height="10" fill="#0D5EAF" />
        <rect x="4" y="0" width="2" height="10" fill="#FFFFFF" />
        <rect x="0" y="4" width="10" height="2" fill="#FFFFFF" />
    </svg>
);

const FlagVA = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="12" height="18" fill="#FFD700" />
        <rect x="12" width="12" height="18" fill="#FFFFFF" />
    </svg>
);

const FlagSM = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="9" fill="#FFFFFF" />
        <rect y="9" width="24" height="9" fill="#5EB3D6" />
    </svg>
);

const FlagMC = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="9" fill="#CE1126" />
        <rect y="9" width="24" height="9" fill="#FFFFFF" />
    </svg>
);

const FlagAD = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="8" height="18" fill="#0018A8" />
        <rect x="8" width="8" height="18" fill="#FEDF00" />
        <rect x="16" width="8" height="18" fill="#D52B1E" />
    </svg>
);

const FlagSI = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="6" fill="#FFFFFF" />
        <rect y="6" width="24" height="6" fill="#0000FF" />
        <rect y="12" width="24" height="6" fill="#FF0000" />
    </svg>
);

const FlagHR = () => (
    <svg width="24" height="18" viewBox="0 0 24 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="24" height="6" fill="#FF0000" />
        <rect y="6" width="24" height="6" fill="#FFFFFF" />
        <rect y="12" width="24" height="6" fill="#0000FF" />
    </svg>
);

const FLAGS: Record<JurisdictionCode, () => JSX.Element> = {
    SK: FlagSK,
    CZ: FlagCZ,
    PL: FlagPL,
    AT: FlagAT,
    DE: FlagDE,
    FI: FlagFI,
    HU: FlagHU,
    FR: FlagFR,
    GB: FlagGB,
    ES: FlagES,
    NL: FlagNL,
    BE: FlagBE,
    IT: FlagIT,
    PT: FlagPT,
    SE: FlagSE,
    CH: FlagCH,
    LU: FlagLU,
    LI: FlagLI,
    DK: FlagDK,
    NO: FlagNO,
    IE: FlagIE,
    GR: FlagGR,
    VA: FlagVA,
    SM: FlagSM,
    MC: FlagMC,
    AD: FlagAD,
    SI: FlagSI,
    HR: FlagHR
};

export default function JurisdictionSelector() {
    const { jurisdiction, setJurisdiction, currentJurisdiction } = useJurisdiction();
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);

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

    const CurrentFlag = FLAGS[jurisdiction];

    return (
        <div className="relative" ref={dropdownRef}>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center space-x-2 px-3 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 transition-colors text-white border border-blue-700"
                title="Select Jurisdiction"
            >
                <CurrentFlag />
                <span className="hidden sm:inline text-sm">{currentJurisdiction.name}</span>
            </button>

            {isOpen && (
                <div className="absolute right-0 mt-2 w-56 bg-slate-900 border border-white/10 rounded-xl shadow-xl overflow-hidden z-50 backdrop-blur-xl">
                    <div className="py-1">
                        {jurisdictions.map((j) => {
                            const Flag = FLAGS[j.code];
                            return (
                                <button
                                    key={j.code}
                                    onClick={() => {
                                        setJurisdiction(j.code as JurisdictionCode);
                                        setIsOpen(false);
                                        // Trigger language switch check
                                        window.dispatchEvent(new CustomEvent('codex_language_update', { detail: 'check_language_switch' }));
                                    }}
                                    className={`w-full text-left px-4 py-3 text-sm flex items-center space-x-3 hover:bg-white/10 transition-colors ${jurisdiction === j.code ? 'bg-white/5 text-purple-400' : 'text-gray-300'
                                        }`}
                                >
                                    <Flag />
                                    <span>{j.name}</span>
                                </button>
                            );
                        })}
                    </div>
                </div>
            )}
        </div>
    );
}
