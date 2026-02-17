'use client';

import { useLanguage } from '@/lib/LanguageContext';
import { X } from 'lucide-react';
import { useRouter } from 'next/navigation';

interface AuthPromptModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export default function AuthPromptModal({ isOpen, onClose }: AuthPromptModalProps) {
    const { t, language } = useLanguage();
    const router = useRouter();

    // Fallback translations for all 10 languages
    const translations: Record<string, any> = {
        sk: {
            title: "Vyžaduje sa registrácia",
            message: "Pre prístup k tejto funkcii sa prosím zaregistrujte alebo prihláste",
            register: "Zaregistrovať sa",
            login: "Prihlásiť sa"
        },
        en: {
            title: "Registration Required",
            message: "Please register or login to access this feature",
            register: "Register",
            login: "Login"
        },
        cs: {
            title: "Vyžaduje se registrace",
            message: "Pro přístup k této funkci se prosím zaregistrujte nebo přihlaste",
            register: "Zaregistrovat se",
            login: "Přihlásit se"
        },
        pl: {
            title: "Wymagana rejestracja",
            message: "Aby uzyskać dostęp do tej funkcji, zarejestruj się lub zaloguj",
            register: "Zarejestruj się",
            login: "Zaloguj się"
        },
        de: {
            title: "Registrierung erforderlich",
            message: "Bitte registrieren Sie sich oder melden Sie sich an, um auf diese Funktion zuzugreifen",
            register: "Registrieren",
            login: "Anmelden"
        },
        fr: {
            title: "Inscription requise",
            message: "Veuillez vous inscrire ou vous connecter pour accéder à cette fonctionnalité",
            register: "S'inscrire",
            login: "Se connecter"
        },
        es: {
            title: "Registro requerido",
            message: "Por favor, regístrese o inicie sesión para acceder a esta función",
            register: "Registrarse",
            login: "Iniciar sesión"
        },
        uk: {
            title: "Потрібна реєстрація",
            message: "Будь ласка, зареєструйтеся або увійдіть, щоб отримати доступ до цієї функції",
            register: "Зареєструватися",
            login: "Увійти"
        },
        it: {
            title: "Registrazione richiesta",
            message: "Si prega di registrarsi o accedere per accedere a questa funzione",
            register: "Registrati",
            login: "Accedi"
        },
        ru: {
            title: "Требуется регистрация",
            message: "Пожалуйста, зарегистрируйтесь или войдите, чтобы получить доступ к этой функции",
            register: "Зарегистрироваться",
            login: "Войти"
        }
    };

    const getText = (key: string) => {
        const translationKey = `student.authPrompt.${key}`;
        const translated = t(translationKey);

        // If translation returns the key itself, it means translation not found
        if (translated === translationKey) {
            return translations[language]?.[key] || translations.en[key];
        }

        return translated;
    };


    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
            {/* Backdrop */}
            <div
                className="absolute inset-0 bg-black/50 backdrop-blur-sm"
                onClick={onClose}
            />

            {/* Modal */}
            <div className="relative bg-white rounded-2xl shadow-2xl max-w-md w-full mx-4 p-8 animate-fadeIn">
                {/* Close button */}
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
                >
                    <X className="w-6 h-6" />
                </button>

                {/* Content */}
                <div className="text-center">
                    <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                        </svg>
                    </div>

                    <h2 className="text-2xl font-bold text-gray-900 mb-2">
                        {getText('title')}
                    </h2>

                    <p className="text-gray-600 mb-8">
                        {getText('message')}
                    </p>

                    {/* Action buttons */}
                    <div className="flex flex-col gap-3">
                        <button
                            onClick={() => {
                                onClose();
                                router.push('/register');
                            }}
                            className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                        >
                            {getText('register')}
                        </button>

                        <button
                            onClick={() => {
                                onClose();
                                router.push('/login');
                            }}
                            className="w-full bg-white text-blue-600 py-3 px-6 rounded-lg font-semibold border-2 border-blue-600 hover:bg-blue-50 transition-colors"
                        >
                            {getText('login')}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
