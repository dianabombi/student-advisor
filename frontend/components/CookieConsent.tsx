'use client';

import { useState, useEffect } from 'react';
import { useLanguage } from '@/lib/LanguageContext';
import { Cookie, Settings, Shield, X, ChevronDown, ChevronUp } from 'lucide-react';

interface CookiePreferences {
    necessary: boolean;
    analytics: boolean;
    marketing: boolean;
    functional: boolean;
}

const DEFAULT_PREFERENCES: CookiePreferences = {
    necessary: true,
    analytics: false,
    marketing: false,
    functional: false,
};

export default function CookieConsent() {
    const [visible, setVisible] = useState(false);
    const [showManage, setShowManage] = useState(false);
    const [showConditions, setShowConditions] = useState(false);
    const [preferences, setPreferences] = useState<CookiePreferences>(DEFAULT_PREFERENCES);
    const { t } = useLanguage();

    useEffect(() => {
        const consent = localStorage.getItem('cookie-consent');
        if (!consent) {
            // Small delay so it doesn't flash on page load
            const timer = setTimeout(() => setVisible(true), 800);
            return () => clearTimeout(timer);
        }
    }, []);

    const acceptAll = () => {
        const allAccepted: CookiePreferences = {
            necessary: true,
            analytics: true,
            marketing: true,
            functional: true,
        };
        localStorage.setItem('cookie-consent', JSON.stringify(allAccepted));
        localStorage.setItem('cookie-consent-date', new Date().toISOString());
        setVisible(false);
    };

    const rejectAll = () => {
        localStorage.setItem('cookie-consent', JSON.stringify(DEFAULT_PREFERENCES));
        localStorage.setItem('cookie-consent-date', new Date().toISOString());
        setVisible(false);
    };

    const savePreferences = () => {
        localStorage.setItem('cookie-consent', JSON.stringify(preferences));
        localStorage.setItem('cookie-consent-date', new Date().toISOString());
        setShowManage(false);
        setVisible(false);
    };

    if (!visible) return null;

    return (
        <>
            {/* Backdrop */}
            <div className="fixed inset-0 bg-black/30 backdrop-blur-sm z-[998] transition-opacity" />

            {/* Cookie Banner */}
            <div className="fixed bottom-0 left-0 right-0 z-[999] p-4 sm:p-6 animate-slide-up">
                <div className="max-w-3xl mx-auto bg-white rounded-2xl shadow-2xl border border-gray-100 overflow-hidden">

                    {/* Main Banner */}
                    {!showManage && !showConditions && (
                        <div className="p-6">
                            <div className="flex items-start gap-4">
                                <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center flex-shrink-0">
                                    <Cookie className="w-6 h-6 text-blue-600" />
                                </div>
                                <div className="flex-1">
                                    <h3 className="text-lg font-bold text-gray-900 mb-1">
                                        {t('cookies.title')}
                                    </h3>
                                    <p className="text-sm text-gray-600 leading-relaxed">
                                        {t('cookies.description')}
                                    </p>
                                </div>
                            </div>

                            <div className="flex flex-col sm:flex-row gap-3 mt-5">
                                <button
                                    onClick={acceptAll}
                                    className="flex-1 bg-blue-600 text-white px-6 py-2.5 rounded-xl font-semibold hover:bg-blue-700 transition-colors text-sm shadow-md"
                                >
                                    {t('cookies.acceptAll')}
                                </button>
                                <button
                                    onClick={rejectAll}
                                    className="flex-1 bg-gray-100 text-gray-700 px-6 py-2.5 rounded-xl font-semibold hover:bg-gray-200 transition-colors text-sm"
                                >
                                    {t('cookies.rejectAll')}
                                </button>
                            </div>

                            <div className="flex justify-center gap-6 mt-4 pt-3 border-t border-gray-100">
                                <button
                                    onClick={() => setShowManage(true)}
                                    className="flex items-center gap-1.5 text-sm text-gray-500 hover:text-blue-600 transition-colors"
                                >
                                    <Settings className="w-4 h-4" />
                                    {t('cookies.manageCookies')}
                                </button>
                                <button
                                    onClick={() => setShowConditions(true)}
                                    className="flex items-center gap-1.5 text-sm text-gray-500 hover:text-blue-600 transition-colors"
                                >
                                    <Shield className="w-4 h-4" />
                                    {t('cookies.conditions')}
                                </button>
                            </div>
                        </div>
                    )}

                    {/* Manage Cookies Panel */}
                    {showManage && (
                        <div className="p-6">
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                                    <Settings className="w-5 h-5 text-blue-600" />
                                    {t('cookies.manageCookies')}
                                </h3>
                                <button
                                    onClick={() => setShowManage(false)}
                                    className="text-gray-400 hover:text-gray-600 transition-colors"
                                >
                                    <X className="w-5 h-5" />
                                </button>
                            </div>

                            <div className="space-y-3">
                                {/* Necessary */}
                                <div className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
                                    <div>
                                        <p className="text-sm font-semibold text-gray-900">{t('cookies.necessary.title')}</p>
                                        <p className="text-xs text-gray-500">{t('cookies.necessary.description')}</p>
                                    </div>
                                    <div className="bg-green-100 text-green-700 text-xs font-medium px-2.5 py-1 rounded-lg">
                                        {t('cookies.alwaysOn')}
                                    </div>
                                </div>

                                {/* Analytics */}
                                <label className="flex items-center justify-between p-3 bg-gray-50 rounded-xl cursor-pointer hover:bg-gray-100 transition-colors">
                                    <div>
                                        <p className="text-sm font-semibold text-gray-900">{t('cookies.analytics.title')}</p>
                                        <p className="text-xs text-gray-500">{t('cookies.analytics.description')}</p>
                                    </div>
                                    <div className="relative">
                                        <input
                                            type="checkbox"
                                            checked={preferences.analytics}
                                            onChange={(e) => setPreferences({ ...preferences, analytics: e.target.checked })}
                                            className="sr-only peer"
                                        />
                                        <div className="w-10 h-5 bg-gray-300 peer-checked:bg-blue-600 rounded-full transition-colors"></div>
                                        <div className="absolute left-0.5 top-0.5 w-4 h-4 bg-white rounded-full shadow peer-checked:translate-x-5 transition-transform"></div>
                                    </div>
                                </label>

                                {/* Marketing */}
                                <label className="flex items-center justify-between p-3 bg-gray-50 rounded-xl cursor-pointer hover:bg-gray-100 transition-colors">
                                    <div>
                                        <p className="text-sm font-semibold text-gray-900">{t('cookies.marketing.title')}</p>
                                        <p className="text-xs text-gray-500">{t('cookies.marketing.description')}</p>
                                    </div>
                                    <div className="relative">
                                        <input
                                            type="checkbox"
                                            checked={preferences.marketing}
                                            onChange={(e) => setPreferences({ ...preferences, marketing: e.target.checked })}
                                            className="sr-only peer"
                                        />
                                        <div className="w-10 h-5 bg-gray-300 peer-checked:bg-blue-600 rounded-full transition-colors"></div>
                                        <div className="absolute left-0.5 top-0.5 w-4 h-4 bg-white rounded-full shadow peer-checked:translate-x-5 transition-transform"></div>
                                    </div>
                                </label>

                                {/* Functional */}
                                <label className="flex items-center justify-between p-3 bg-gray-50 rounded-xl cursor-pointer hover:bg-gray-100 transition-colors">
                                    <div>
                                        <p className="text-sm font-semibold text-gray-900">{t('cookies.functional.title')}</p>
                                        <p className="text-xs text-gray-500">{t('cookies.functional.description')}</p>
                                    </div>
                                    <div className="relative">
                                        <input
                                            type="checkbox"
                                            checked={preferences.functional}
                                            onChange={(e) => setPreferences({ ...preferences, functional: e.target.checked })}
                                            className="sr-only peer"
                                        />
                                        <div className="w-10 h-5 bg-gray-300 peer-checked:bg-blue-600 rounded-full transition-colors"></div>
                                        <div className="absolute left-0.5 top-0.5 w-4 h-4 bg-white rounded-full shadow peer-checked:translate-x-5 transition-transform"></div>
                                    </div>
                                </label>
                            </div>

                            <div className="flex gap-3 mt-5">
                                <button
                                    onClick={savePreferences}
                                    className="flex-1 bg-blue-600 text-white px-6 py-2.5 rounded-xl font-semibold hover:bg-blue-700 transition-colors text-sm shadow-md"
                                >
                                    {t('cookies.savePreferences')}
                                </button>
                                <button
                                    onClick={acceptAll}
                                    className="flex-1 bg-gray-100 text-gray-700 px-6 py-2.5 rounded-xl font-semibold hover:bg-gray-200 transition-colors text-sm"
                                >
                                    {t('cookies.acceptAll')}
                                </button>
                            </div>
                        </div>
                    )}

                    {/* Conditions Panel */}
                    {showConditions && (
                        <div className="p-6">
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                                    <Shield className="w-5 h-5 text-blue-600" />
                                    {t('cookies.conditionsTitle')}
                                </h3>
                                <button
                                    onClick={() => setShowConditions(false)}
                                    className="text-gray-400 hover:text-gray-600 transition-colors"
                                >
                                    <X className="w-5 h-5" />
                                </button>
                            </div>

                            <div className="max-h-64 overflow-y-auto text-sm text-gray-600 space-y-3 pr-2">
                                <p>{t('cookies.conditionsText1')}</p>
                                <p>{t('cookies.conditionsText2')}</p>
                                <p>{t('cookies.conditionsText3')}</p>
                                <p>{t('cookies.conditionsText4')}</p>
                            </div>

                            <div className="flex gap-3 mt-5">
                                <button
                                    onClick={() => setShowConditions(false)}
                                    className="flex-1 bg-gray-100 text-gray-700 px-6 py-2.5 rounded-xl font-semibold hover:bg-gray-200 transition-colors text-sm"
                                >
                                    {t('cookies.back')}
                                </button>
                                <button
                                    onClick={acceptAll}
                                    className="flex-1 bg-blue-600 text-white px-6 py-2.5 rounded-xl font-semibold hover:bg-blue-700 transition-colors text-sm shadow-md"
                                >
                                    {t('cookies.acceptAll')}
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </>
    );
}
