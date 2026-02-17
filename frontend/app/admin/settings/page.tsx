'use client';

import { useEffect, useState } from 'react';
import { Save, Eye, EyeOff, ChevronLeft } from 'lucide-react';
import Link from 'next/link';
import { showSuccess, showError } from '@/lib/toast';
import { FormSkeleton } from '@/components/admin/LoadingSkeletons';
import ErrorState from '@/components/admin/ErrorState';
import { useLanguage } from '@/lib/LanguageContext';

interface Settings {
    platform_name: string;
    support_email: string;
    maintenance_mode: boolean;
    openai_api_key: string;
}

export default function SettingsPage() {
    const { t } = useLanguage();
    const [settings, setSettings] = useState<Settings>({
        platform_name: '',
        support_email: '',
        maintenance_mode: false,
        openai_api_key: ''
    });
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [showApiKey, setShowApiKey] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetchSettings();
    }, []);

    const fetchSettings = async () => {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                window.location.href = '/auth/login';
                return;
            }

            const response = await fetch('/api/admin/settings', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                setSettings(data);
            } else if (response.status === 401 || response.status === 403) {
                window.location.href = '/auth/login';
            }
        } catch (error) {
            console.error('Failed to fetch settings:', error);
            setError(t('admin.settings.messages.loadError'));
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        try {
            const token = localStorage.getItem('token');
            if (!token) return;

            setSaving(true);

            const response = await fetch('/api/admin/settings', {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(settings)
            });

            if (response.ok) {
                showSuccess(t('admin.settings.messages.saveSuccess'));
            } else {
                showError(t('admin.settings.messages.saveError'));
            }
        } catch (error) {
            console.error('Failed to save settings:', error);
            showError(t('admin.settings.messages.saveError'));
        } finally {
            setSaving(false);
        }
    };

    const maskApiKey = (key: string) => {
        if (!key || key.length < 8) return key;
        return key.substring(0, 4) + '•'.repeat(key.length - 8) + key.substring(key.length - 4);
    };

    if (loading) {
        return (
            <div className="space-y-6">
                <div>
                    <h1 className="text-3xl font-bold text-white">{t('admin.settings.title')}</h1>
                    <p className="text-gray-400 mt-2">{t('admin.settings.subtitle')}</p>
                </div>
                <div className="bg-gray-800 rounded-xl border border-gray-700 p-6">
                    <FormSkeleton />
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="space-y-6">
                <div>
                    <h1 className="text-3xl font-bold text-white">{t('admin.settings.title')}</h1>
                    <p className="text-gray-400 mt-2">{t('admin.settings.subtitle')}</p>
                </div>
                <ErrorState
                    message={error}
                    onRetry={fetchSettings}
                />
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <Link
                        href="/admin/dashboard"
                        className="p-2 hover:bg-gray-800 rounded-lg transition-colors text-gray-400 hover:text-white"
                    >
                        <ChevronLeft className="w-5 h-5" />
                    </Link>
                    <div>
                        <h1 className="text-3xl font-bold text-white">{t('admin.settings.title')}</h1>
                        <p className="text-gray-400 mt-2">{t('admin.settings.subtitle')}</p>
                    </div>
                </div>
            </div>

            {/* Settings Form */}
            <div className="bg-gray-800 rounded-xl border border-gray-700">
                <div className="p-6 border-b border-gray-700">
                    <h2 className="text-xl font-semibold text-white">{t('admin.settings.platformConfig')}</h2>
                </div>

                <div className="p-6 space-y-6">
                    {/* Platform Name */}
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                            {t('admin.settings.fields.platformName.label')}
                        </label>
                        <input
                            type="text"
                            value={settings.platform_name}
                            onChange={(e) => setSettings({ ...settings, platform_name: e.target.value })}
                            className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors"
                            placeholder={t('admin.settings.fields.platformName.placeholder')}
                        />
                        <p className="mt-2 text-sm text-gray-400">
                            {t('admin.settings.fields.platformName.description')}
                        </p>
                    </div>

                    {/* Support Email */}
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                            {t('admin.settings.fields.supportEmail.label')}
                        </label>
                        <input
                            type="email"
                            value={settings.support_email}
                            onChange={(e) => setSettings({ ...settings, support_email: e.target.value })}
                            className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors"
                            placeholder={t('admin.settings.fields.supportEmail.placeholder')}
                        />
                        <p className="mt-2 text-sm text-gray-400">
                            {t('admin.settings.fields.supportEmail.description')}
                        </p>
                    </div>

                    {/* Maintenance Mode */}
                    <div>
                        <div className="flex items-center justify-between">
                            <div>
                                <label className="block text-sm font-medium text-gray-300">
                                    {t('admin.settings.fields.maintenanceMode.label')}
                                </label>
                                <p className="mt-1 text-sm text-gray-400">
                                    {t('admin.settings.fields.maintenanceMode.description')}
                                </p>
                            </div>
                            <button
                                onClick={() => setSettings({ ...settings, maintenance_mode: !settings.maintenance_mode })}
                                className={`relative inline-flex h-8 w-14 items-center rounded-full transition-colors ${settings.maintenance_mode ? 'bg-blue-600' : 'bg-gray-700'
                                    }`}
                            >
                                <span
                                    className={`inline-block h-6 w-6 transform rounded-full bg-white transition-transform ${settings.maintenance_mode ? 'translate-x-7' : 'translate-x-1'
                                        }`}
                                />
                            </button>
                        </div>
                        {settings.maintenance_mode && (
                            <div className="mt-3 p-3 bg-yellow-900/20 border border-yellow-700 rounded-lg">
                                <p className="text-sm text-yellow-400">
                                    {t('admin.settings.fields.maintenanceMode.warning')}
                                </p>
                            </div>
                        )}
                    </div>

                    {/* OpenAI API Key */}
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                            {t('admin.settings.fields.openaiApiKey.label')}
                        </label>
                        <div className="relative">
                            <input
                                type={showApiKey ? 'text' : 'password'}
                                value={showApiKey ? settings.openai_api_key : maskApiKey(settings.openai_api_key)}
                                onChange={(e) => setSettings({ ...settings, openai_api_key: e.target.value })}
                                className="w-full px-4 py-3 pr-12 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors font-mono"
                                placeholder={t('admin.settings.fields.openaiApiKey.placeholder')}
                            />
                            <button
                                type="button"
                                onClick={() => setShowApiKey(!showApiKey)}
                                className="absolute right-3 top-1/2 -translate-y-1/2 p-2 text-gray-400 hover:text-white transition-colors"
                            >
                                {showApiKey ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                            </button>
                        </div>
                        <p className="mt-2 text-sm text-gray-400">
                            {t('admin.settings.fields.openaiApiKey.description')}
                        </p>
                    </div>

                    {/* Save Button */}
                    <div className="flex items-center gap-4 pt-4">
                        <button
                            onClick={handleSave}
                            disabled={saving}
                            className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                            <Save className="w-5 h-5" />
                            {saving ? t('admin.settings.actions.saving') : t('admin.settings.actions.save')}
                        </button>
                    </div>
                </div>
            </div>

            {/* Danger Zone */}
            <div className="bg-gray-800 rounded-xl border border-red-900/50">
                <div className="p-6 border-b border-red-900/50">
                    <h2 className="text-xl font-semibold text-red-400">{t('admin.settings.dangerZone.title')}</h2>
                </div>
                <div className="p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <h3 className="text-white font-medium">{t('admin.settings.dangerZone.resetAll')}</h3>
                            <p className="text-sm text-gray-400 mt-1">
                                {t('admin.settings.dangerZone.resetDescription')}
                            </p>
                        </div>
                        <button className="px-4 py-2 bg-red-900/50 text-red-400 border border-red-700 rounded-lg hover:bg-red-900 transition-colors">
                            {t('admin.settings.actions.reset')}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
