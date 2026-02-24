'use client';

import { useState } from 'react';
import { X, Shield, Users, GraduationCap, BarChart3, Settings as SettingsIcon, Bot } from 'lucide-react';
import { useLanguage } from '@/lib/LanguageContext';

interface Permission {
    id: string;
    name: string;
    granted: boolean;
}

interface Administrator {
    id: number;
    name: string;
    email: string;
    role: 'super_admin' | 'admin';
    is_active: boolean;
    created_at: string;
    permissions?: Permission[];
}

interface EditPermissionsModalProps {
    isOpen: boolean;
    admin: Administrator;
    onClose: () => void;
    onPermissionsUpdated: (admin: Administrator) => void;
}

interface PermissionCategory {
    id: string;
    name: string;
    icon: any;
    permissions: Permission[];
}

export default function EditPermissionsModal({
    isOpen,
    admin,
    onClose,
    onPermissionsUpdated,
}: EditPermissionsModalProps) {
    const { t } = useLanguage();

    const [permissions, setPermissions] = useState<PermissionCategory[]>([
        {
            id: 'users',
            name: t('admin.administrators.permissions.categories.users'),
            icon: Users,
            permissions: [
                { id: 'users.view', name: t('admin.administrators.permissions.users.view'), granted: true },
                { id: 'users.edit', name: t('admin.administrators.permissions.users.edit'), granted: true },
                { id: 'users.delete', name: t('admin.administrators.permissions.users.delete'), granted: false },
            ],
        },
        {
            id: 'universities',
            name: t('admin.administrators.permissions.categories.universities'),
            icon: GraduationCap,
            permissions: [
                { id: 'universities.view', name: t('admin.administrators.permissions.universities.view'), granted: true },
                { id: 'universities.edit', name: t('admin.administrators.permissions.universities.edit'), granted: false },
                { id: 'universities.create', name: t('admin.administrators.permissions.universities.create'), granted: false },
                { id: 'universities.delete', name: t('admin.administrators.permissions.universities.delete'), granted: false },
            ],
        },
        {
            id: 'analytics',
            name: t('admin.administrators.permissions.categories.analytics'),
            icon: BarChart3,
            permissions: [
                { id: 'analytics.view', name: t('admin.administrators.permissions.analytics.view'), granted: true },
            ],
        },
        {
            id: 'settings',
            name: t('admin.administrators.permissions.categories.settings'),
            icon: SettingsIcon,
            permissions: [
                { id: 'settings.edit', name: t('admin.administrators.permissions.settings.edit'), granted: false },
            ],
        },
        {
            id: 'ai',
            name: t('admin.administrators.permissions.categories.ai'),
            icon: Bot,
            permissions: [
                { id: 'ai.manage', name: t('admin.administrators.permissions.ai.manage'), granted: false },
            ],
        },
    ]);

    const [loading, setLoading] = useState(false);

    if (!isOpen) return null;

    const handleTogglePermission = (categoryId: string, permissionId: string) => {
        setPermissions(
            permissions.map((category) =>
                category.id === categoryId
                    ? {
                        ...category,
                        permissions: category.permissions.map((perm) =>
                            perm.id === permissionId ? { ...perm, granted: !perm.granted } : perm
                        ),
                    }
                    : category
            )
        );
    };

    const handleSave = async () => {
        setLoading(true);

        // Simulate API call
        setTimeout(() => {
            const allPermissions = permissions.flatMap((cat) => cat.permissions);
            const updatedAdmin = {
                ...admin,
                permissions: allPermissions,
            };

            onPermissionsUpdated(updatedAdmin);
            setLoading(false);
        }, 500);
    };

    const handleBackdropClick = (e: React.MouseEvent) => {
        if (e.target === e.currentTarget) {
            onClose();
        }
    };

    return (
        <div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
            onClick={handleBackdropClick}
        >
            <div className="bg-gray-800 rounded-xl border border-gray-700 w-full max-w-2xl shadow-2xl max-h-[90vh] overflow-hidden flex flex-col">
                {/* Header */}
                <div className="flex items-center justify-between p-6 border-b border-gray-700">
                    <div>
                        <h2 className="text-xl font-bold text-white flex items-center gap-2">
                            <Shield className="w-6 h-6 text-blue-400" />
                            {t('admin.administrators.modals.permissions.title')}
                        </h2>
                        <p className="text-sm text-gray-400 mt-1">
                            {admin.name} ({admin.email})
                        </p>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-gray-700 rounded-lg transition-colors text-gray-400 hover:text-white"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Permissions List */}
                <div className="p-6 space-y-6 overflow-y-auto flex-1">
                    {permissions.map((category) => {
                        const Icon = category.icon;
                        return (
                            <div key={category.id} className="bg-gray-900 rounded-lg p-4 border border-gray-700">
                                <div className="flex items-center gap-2 mb-4">
                                    <Icon className="w-5 h-5 text-blue-400" />
                                    <h3 className="text-white font-semibold">{category.name}</h3>
                                </div>
                                <div className="space-y-3">
                                    {category.permissions.map((permission) => (
                                        <label
                                            key={permission.id}
                                            className="flex items-center gap-3 p-3 hover:bg-gray-800 rounded-lg cursor-pointer transition-colors"
                                        >
                                            <input
                                                type="checkbox"
                                                checked={permission.granted}
                                                onChange={() =>
                                                    handleTogglePermission(category.id, permission.id)
                                                }
                                                className="w-5 h-5 rounded border-gray-600 text-blue-600 focus:ring-blue-500 focus:ring-offset-gray-800 bg-gray-700 cursor-pointer"
                                            />
                                            <span className="text-gray-300 flex-1">{permission.name}</span>
                                        </label>
                                    ))}
                                </div>
                            </div>
                        );
                    })}
                </div>

                {/* Actions */}
                <div className="flex items-center gap-3 p-6 border-t border-gray-700">
                    <button
                        type="button"
                        onClick={onClose}
                        className="flex-1 px-4 py-3 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
                    >
                        {t('admin.administrators.modals.permissions.cancel')}
                    </button>
                    <button
                        type="button"
                        onClick={handleSave}
                        disabled={loading}
                        className="flex-1 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
                    >
                        {loading ? (
                            <>
                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                                {t('admin.administrators.modals.permissions.saving')}
                            </>
                        ) : (
                            t('admin.administrators.modals.permissions.save')
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
}
