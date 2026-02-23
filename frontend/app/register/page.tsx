'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Sparkles, Mail, Lock, User, ArrowRight, ArrowLeft } from 'lucide-react';
import { useLanguage } from '@/lib/LanguageContext';

export default function RegisterPage() {
    const router = useRouter();
    const { t } = useLanguage();
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    // Terms of Service acceptance
    const [termsAccepted, setTermsAccepted] = useState(false);



    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        // Validate all fields are filled
        if (!formData.firstName.trim()) {
            setError(t('auth.register.error_firstName_required') || 'Please enter your first name');
            return;
        }

        if (!formData.lastName.trim()) {
            setError(t('auth.register.error_lastName_required') || 'Please enter your last name');
            return;
        }

        if (!formData.email.trim()) {
            setError(t('auth.register.error_email_required') || 'Please enter your email');
            return;
        }

        if (!formData.password) {
            setError(t('auth.register.error_password_required') || 'Please enter a password');
            return;
        }

        // Validate Terms of Service
        if (!termsAccepted) {
            setError(t('auth.register.error_terms') || 'You must accept Terms of Service');
            return;
        }

        if (formData.password !== formData.confirmPassword) {
            setError(t('auth.register.error_password_mismatch'));
            return;
        }

        setLoading(true);

        try {
            const requestData = {
                name: `${formData.firstName} ${formData.lastName}`.trim(),
                email: formData.email,
                password: formData.password,
                // Required consent fields for UPL protection
                consent_ai_tool: termsAccepted,
                consent_no_advice: termsAccepted,
                consent_no_attorney: termsAccepted
            };

            console.log('📤 Sending registration data:', requestData);

            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestData)
            });

            if (response.ok) {
                const data = await response.json();
                console.log('✅ Registration successful!', data);

                // Save token to localStorage
                if (data.access_token) {
                    localStorage.setItem('token', data.access_token);
                    localStorage.setItem('user', JSON.stringify(data.user));
                }

                // Redirect to homepage where authenticated users see full content
                router.push('/');
            } else {
                const data = await response.json();
                console.log('❌ Registration failed:', data);

                // Handle different error formats
                let errorMessage = t('auth.register.error_registration');

                if (typeof data.detail === 'string') {
                    errorMessage = data.detail;
                } else if (Array.isArray(data.detail)) {
                    // Validation errors from FastAPI
                    errorMessage = data.detail.map((err: any) => err.msg).join(', ');
                } else if (data.message) {
                    errorMessage = data.message;
                }

                setError(errorMessage);
            }
        } catch (err) {
            console.error('💥 Registration error:', err);
            setError(t('auth.register.error_connection'));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-100 flex items-center justify-center px-4 py-8">
            <div className="max-w-lg w-full">
                {/* Header with logo and back */}
                <div className="flex items-center justify-between mb-6">
                    <Link href="/" className="flex items-center space-x-2 group">
                        <Sparkles className="w-8 h-8 text-blue-600" />
                        <span className="text-2xl font-bold text-blue-600">Student Advisor</span>
                    </Link>
                    <Link
                        href="/"
                        className="flex items-center gap-1.5 text-sm text-gray-500 hover:text-blue-600 transition-colors"
                    >
                        <ArrowLeft className="w-4 h-4" />
                        <span>{t('common.back')}</span>
                    </Link>
                </div>

                {/* Card */}
                <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100">
                    <div className="text-center mb-6">
                        <h2 className="text-2xl font-bold text-gray-900 mb-1">{t('auth.register.create_account')}</h2>
                        <p className="text-gray-500 text-sm">{t('auth.register.subtitle')}</p>
                    </div>

                    {error && (
                        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl mb-5 text-sm">
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-4">
                        {/* Name fields side by side */}
                        <div className="grid grid-cols-2 gap-3">
                            <div>
                                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                                    {t('auth.register.firstName')}
                                </label>
                                <div className="relative">
                                    <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                                    <input
                                        type="text"
                                        required
                                        value={formData.firstName}
                                        onChange={(e) => setFormData({ ...formData, firstName: e.target.value })}
                                        className="w-full pl-10 pr-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white focus:border-transparent transition-all text-sm"
                                        placeholder={t('auth.register.placeholder_firstName')}
                                    />
                                </div>
                            </div>
                            <div>
                                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                                    {t('auth.register.lastName')}
                                </label>
                                <div className="relative">
                                    <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                                    <input
                                        type="text"
                                        required
                                        value={formData.lastName}
                                        onChange={(e) => setFormData({ ...formData, lastName: e.target.value })}
                                        className="w-full pl-10 pr-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white focus:border-transparent transition-all text-sm"
                                        placeholder={t('auth.register.placeholder_lastName')}
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Email */}
                        <div>
                            <label className="block text-xs font-medium text-gray-500 mb-1.5">
                                {t('auth.register.email')}
                            </label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                                <input
                                    type="email"
                                    required
                                    value={formData.email}
                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                    className="w-full pl-10 pr-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white focus:border-transparent transition-all text-sm"
                                    placeholder={t('auth.register.placeholder_email')}
                                />
                            </div>
                        </div>

                        {/* Password fields side by side */}
                        <div className="grid grid-cols-2 gap-3">
                            <div>
                                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                                    {t('auth.register.password')}
                                </label>
                                <div className="relative">
                                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                                    <input
                                        type="password"
                                        required
                                        value={formData.password}
                                        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                        className="w-full pl-10 pr-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white focus:border-transparent transition-all text-sm"
                                        placeholder={t('auth.register.placeholder_password')}
                                    />
                                </div>
                            </div>
                            <div>
                                <label className="block text-xs font-medium text-gray-500 mb-1.5">
                                    {t('auth.register.confirm_password')}
                                </label>
                                <div className="relative">
                                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                                    <input
                                        type="password"
                                        required
                                        value={formData.confirmPassword}
                                        onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                                        className="w-full pl-10 pr-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white focus:border-transparent transition-all text-sm"
                                        placeholder={t('auth.register.placeholder_confirm_password')}
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Terms of Service Checkbox */}
                        <label className="flex items-start space-x-2.5 cursor-pointer group py-1">
                            <input
                                type="checkbox"
                                checked={termsAccepted}
                                onChange={(e) => setTermsAccepted(e.target.checked)}
                                className="mt-0.5 w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500 cursor-pointer"
                            />
                            <span className="text-xs text-gray-500 leading-relaxed">
                                {t('auth.register.terms_agreement')}{' '}
                                <Link href="/terms" target="_blank" className="text-blue-600 hover:underline">
                                    {t('auth.register.terms_link')}
                                </Link>
                                {' '}{t('auth.register.and')}{' '}
                                <Link href="/privacy" target="_blank" className="text-blue-600 hover:underline">
                                    {t('auth.register.privacy_link')}
                                </Link>
                            </span>
                        </label>

                        {/* Submit Button */}
                        <button
                            type="submit"
                            disabled={loading || !termsAccepted}
                            className="w-full py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition-all disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-sm hover:shadow-md"
                        >
                            <span>{loading ? t('auth.register.button_loading') : t('auth.register.button')}</span>
                            {!loading && <ArrowRight className="w-4 h-4" />}
                        </button>

                        {/* Login link */}
                        <p className="text-center text-sm text-gray-500 pt-2">
                            {t('auth.register.have_account')}{' '}
                            <Link href="/login" className="text-blue-600 font-medium hover:underline">
                                {t('auth.register.login_link')}
                            </Link>
                        </p>
                    </form>
                </div>
            </div>
        </div>
    );
}
