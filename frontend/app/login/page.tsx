'use client';

import { useState, Suspense } from 'react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { Sparkles, Mail, Lock, ArrowRight, ArrowLeft } from 'lucide-react';
import { useLanguage } from '@/lib/LanguageContext';


function LoginForm() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const registered = searchParams.get('registered');
    const { t } = useLanguage();

    const [formData, setFormData] = useState({
        email: '',
        password: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            // Prepare form data for OAuth2PasswordRequestForm
            const formDataToSend = new URLSearchParams();
            formDataToSend.append('username', formData.email); // OAuth2 uses 'username' field
            formDataToSend.append('password', formData.password);

            console.log('🔐 Attempting login for:', formData.email);

            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formDataToSend.toString()
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('user', JSON.stringify(data.user));

                // Redirect based on role
                if (data.user.role === 'admin') {
                    router.push('/admin/dashboard');
                } else {
                    router.push('/dashboard');
                }
            } else {
                const data = await response.json();
                // Handle different error formats from backend
                let errorMessage = t('auth.login.error_invalid');
                if (typeof data.detail === 'string') {
                    errorMessage = data.detail;
                } else if (Array.isArray(data.detail)) {
                    // Handle validation errors array
                    errorMessage = data.detail.map((err: any) => err.msg || err).join(', ');
                } else if (data.detail && typeof data.detail === 'object') {
                    // Handle error object
                    errorMessage = data.detail.msg || JSON.stringify(data.detail);
                }
                setError(errorMessage);
            }
        } catch (err: any) {
            console.error('Login error:', err);
            setError(t('auth.login.error_connection') || 'Connection error. Please check if the server is running.');
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
                    <h2 className="text-3xl font-bold text-gray-900 mb-2">{t('auth.login.welcome')}</h2>
                    <p className="text-gray-600 mb-8">{t('auth.login.subtitle')}</p>

                    {registered && (
                        <div className="bg-green-50 border border-green-300 text-green-800 px-4 py-3 rounded-lg mb-6">
                            {t('auth.login.success_registered')}
                        </div>
                    )}

                    {error && (
                        <div className="bg-red-50 border border-red-300 text-red-800 px-4 py-3 rounded-lg mb-6">
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-6">
                        {/* Email */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                {t('auth.login.email')}
                            </label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                                <input
                                    type="email"
                                    required
                                    value={formData.email}
                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                    className="w-full pl-12 pr-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    placeholder={t('auth.login.placeholder_email')}
                                />
                            </div>
                        </div>

                        {/* Password */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                {t('auth.login.password')}
                            </label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                                <input
                                    type="password"
                                    required
                                    value={formData.password}
                                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                    className="w-full pl-12 pr-4 py-3 bg-white border border-gray-300 rounded-lg text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    placeholder={t('auth.login.placeholder_password')}
                                />
                            </div>
                        </div>

                        {/* Submit Button */}
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                        >
                            <span>{loading ? t('auth.login.button_loading') : t('auth.login.button')}</span>
                            {!loading && <ArrowRight className="w-5 h-5" />}
                        </button>
                    </form>

                    {/* Register Link */}
                    <p className="mt-6 text-center text-gray-600">
                        {t('auth.login.no_account')}{' '}
                        <Link href="/register" className="text-blue-600 hover:text-blue-700 font-medium">
                            {t('auth.login.register_link')}
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}

export default function LoginPage() {
    return (
        <Suspense fallback={
            <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
                <div className="text-white">Loading...</div>
            </div>
        }>
            <LoginForm />
        </Suspense>
    );
}
