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
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center px-6">
            <div className="max-w-md w-full">
                {/* Logo */}
                <div className="flex items-center justify-between mb-8">
                    <Link href="/" className="flex items-center space-x-2">
                        <Sparkles className="w-10 h-10 text-blue-600" />
                        <span className="text-3xl font-bold text-gray-900">Student Advisor</span>
                    </Link>
                </div>

                {/* Back Button */}
                <Link
                    href="/"
                    className="mb-6 inline-flex items-center gap-3 px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-bold text-lg rounded-xl hover:shadow-lg hover:shadow-green-500/50 transform hover:scale-105 transition-all duration-200"
                >
                    <ArrowLeft className="w-8 h-8" />
                    <span>{t('common.back')}</span>
                </Link>

                {/* Card */}
                <div className="bg-white rounded-2xl p-8 border border-gray-200 shadow-xl">
                    <h2 className="text-3xl font-bold text-gray-900 mb-2">{t('auth.register.create_account')}</h2>
                    <p className="text-gray-600 mb-8">{t('auth.register.subtitle')}</p>

                    {error && (
                        <div className="bg-red-50 border border-red-300 text-red-800 px-4 py-3 rounded-lg mb-6">
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-6">
                        {/* First Name */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                {t('auth.register.firstName')}
                            </label>
                            <div className="relative">
                                <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                                <input
                                    type="text"
                                    required
                                    value={formData.firstName}
                                    onChange={(e) => setFormData({ ...formData, firstName: e.target.value })}
                                    className="w-full pl-12 pr-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    placeholder={t('auth.register.placeholder_firstName')}
                                />
                            </div>
                        </div>

                        {/* Last Name */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                {t('auth.register.lastName')}
                            </label>
                            <div className="relative">
                                <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                                <input
                                    type="text"
                                    required
                                    value={formData.lastName}
                                    onChange={(e) => setFormData({ ...formData, lastName: e.target.value })}
                                    className="w-full pl-12 pr-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    placeholder={t('auth.register.placeholder_lastName')}
                                />
                            </div>
                        </div>

                        {/* Email */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                {t('auth.register.email')}
                            </label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                                <input
                                    type="email"
                                    required
                                    value={formData.email}
                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                    className="w-full pl-12 pr-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    placeholder={t('auth.register.placeholder_email')}
                                />
                            </div>
                        </div>

                        {/* Password */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                {t('auth.register.password')}
                            </label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                                <input
                                    type="password"
                                    required
                                    value={formData.password}
                                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                    className="w-full pl-12 pr-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    placeholder={t('auth.register.placeholder_password')}
                                />
                            </div>
                        </div>

                        {/* Confirm Password */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                {t('auth.register.confirm_password')}
                            </label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                                <input
                                    type="password"
                                    required
                                    value={formData.confirmPassword}
                                    onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                                    className="w-full pl-12 pr-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    placeholder={t('auth.register.placeholder_confirm_password')}
                                />
                            </div>
                        </div>

                        {/* Terms of Service Checkbox */}
                        <label className="flex items-start space-x-3 cursor-pointer group p-3 rounded-lg hover:bg-white/5 transition-colors">
                            <input
                                type="checkbox"
                                checked={termsAccepted}
                                onChange={(e) => setTermsAccepted(e.target.checked)}
                                className="mt-1 w-5 h-5 rounded border-gray-400 text-purple-500 focus:ring-purple-500 focus:ring-offset-0 cursor-pointer"
                            />
                            <span className="text-sm text-gray-700 group-hover:text-gray-900 transition-colors">
                                {t('auth.register.terms_agreement') || 'I have read and agree to the'}{' '}
                                <Link href="/terms" target="_blank" className="text-blue-600 hover:text-blue-700 underline">
                                    {t('auth.register.terms_link') || 'Terms of Service'}
                                </Link>
                                {' '}{t('auth.register.and') || 'and'}{' '}
                                <Link href="/privacy" target="_blank" className="text-purple-400 hover:text-purple-300 underline">
                                    {t('auth.register.privacy_link') || 'Privacy Policy'}
                                </Link>
                            </span>
                        </label>

                        {/* Submit Button */}
                        <button
                            type="submit"
                            disabled={loading || !termsAccepted}
                            className="w-full py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                        >
                            <span>{loading ? t('auth.register.button_loading') : t('auth.register.button')}</span>
                            {!loading && <ArrowRight className="w-5 h-5" />}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}
