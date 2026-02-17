'use client';

import { useEffect, useState } from 'react';
import { Shield, UserPlus, Edit2, Trash2, ChevronLeft, Search } from 'lucide-react';
import Link from 'next/link';
import { useLanguage } from '@/lib/LanguageContext';
import AddAdminModal from '@/components/admin/AddAdminModal';
import EditPermissionsModal from '@/components/admin/EditPermissionsModal';
import DeleteConfirmModal from '@/components/admin/DeleteConfirmModal';

interface Administrator {
    id: number;
    name: string;
    email: string;
    role: 'super_admin' | 'admin';
    is_active: boolean;
    created_at: string;
    permissions?: Permission[];
}

interface Permission {
    id: string;
    name: string;
    granted: boolean;
}

export default function AdministratorsPage() {
    const { t } = useLanguage();
    const [administrators, setAdministrators] = useState<Administrator[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [isEditModalOpen, setIsEditModalOpen] = useState(false);
    const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
    const [selectedAdmin, setSelectedAdmin] = useState<Administrator | null>(null);

    // Mock data for demonstration
    useEffect(() => {
        // Simulate API call
        setTimeout(() => {
            setAdministrators([
                {
                    id: 1,
                    name: 'Super Admin',
                    email: 'admin@student.com',
                    role: 'super_admin',
                    is_active: true,
                    created_at: '2024-01-01T00:00:00Z',
                },
                {
                    id: 2,
                    name: 'John Doe',
                    email: 'john@student.com',
                    role: 'admin',
                    is_active: true,
                    created_at: '2024-02-15T10:30:00Z',
                    permissions: [
                        { id: 'users.view', name: 'View Users', granted: true },
                        { id: 'users.edit', name: 'Edit Users', granted: true },
                        { id: 'universities.view', name: 'View Universities', granted: true },
                    ],
                },
            ]);
            setLoading(false);
        }, 500);
    }, []);

    const handleAddAdmin = () => {
        setIsAddModalOpen(true);
    };

    const handleEditPermissions = (admin: Administrator) => {
        setSelectedAdmin(admin);
        setIsEditModalOpen(true);
    };

    const handleDeleteAdmin = (admin: Administrator) => {
        setSelectedAdmin(admin);
        setIsDeleteModalOpen(true);
    };

    const handleAdminAdded = (newAdmin: Administrator) => {
        setAdministrators([...administrators, newAdmin]);
        setIsAddModalOpen(false);
    };

    const handlePermissionsUpdated = (updatedAdmin: Administrator) => {
        setAdministrators(
            administrators.map((admin) =>
                admin.id === updatedAdmin.id ? updatedAdmin : admin
            )
        );
        setIsEditModalOpen(false);
        setSelectedAdmin(null);
    };

    const handleAdminDeleted = (adminId: number) => {
        setAdministrators(administrators.filter((admin) => admin.id !== adminId));
        setIsDeleteModalOpen(false);
        setSelectedAdmin(null);
    };

    const filteredAdmins = administrators.filter(
        (admin) =>
            admin.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            admin.email.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const formatDate = (dateString: string) => {
        try {
            return new Date(dateString).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
            });
        } catch {
            return dateString;
        }
    };

    const getInitials = (name: string) => {
        return name
            .split(' ')
            .map((n) => n[0])
            .join('')
            .toUpperCase()
            .slice(0, 2);
    };

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
                        <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                            <Shield className="w-8 h-8 text-blue-400" />
                            {t('admin.administrators.title')}
                        </h1>
                        <p className="text-gray-400 mt-2">{t('admin.administrators.subtitle')}</p>
                    </div>
                </div>
                <button
                    onClick={handleAddAdmin}
                    className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                    <UserPlus className="w-5 h-5" />
                    {t('admin.administrators.addAdmin')}
                </button>
            </div>

            {/* Search Bar */}
            <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                        type="text"
                        placeholder={t('admin.administrators.searchPlaceholder')}
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="w-full pl-10 pr-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors"
                    />
                </div>
            </div>

            {/* Administrators Table */}
            <div className="bg-gray-800 rounded-xl border border-gray-700 overflow-hidden">
                {loading ? (
                    <div className="p-12 text-center">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                        <p className="mt-4 text-gray-400">{t('admin.administrators.loading')}</p>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead className="bg-gray-900 border-b border-gray-700">
                                <tr>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">
                                        {t('admin.administrators.table.admin')}
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">
                                        {t('admin.administrators.table.email')}
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">
                                        {t('admin.administrators.table.role')}
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">
                                        {t('admin.administrators.table.created')}
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">
                                        {t('admin.administrators.table.status')}
                                    </th>
                                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">
                                        {t('admin.administrators.table.actions')}
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-700">
                                {filteredAdmins.map((admin) => (
                                    <tr
                                        key={admin.id}
                                        className="hover:bg-gray-700/50 transition-colors"
                                    >
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <div className="flex items-center gap-3">
                                                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-semibold">
                                                    {getInitials(admin.name)}
                                                </div>
                                                <div className="text-white font-medium">
                                                    {admin.name}
                                                </div>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-gray-300">
                                            {admin.email}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span
                                                className={`px-3 py-1 rounded-full text-xs font-medium ${admin.role === 'super_admin'
                                                        ? 'bg-red-900/50 text-red-300'
                                                        : 'bg-blue-900/50 text-blue-300'
                                                    }`}
                                            >
                                                {admin.role === 'super_admin'
                                                    ? t('admin.administrators.roles.superAdmin')
                                                    : t('admin.administrators.roles.admin')}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-gray-400">
                                            {formatDate(admin.created_at)}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span
                                                className={`px-3 py-1 rounded-full text-xs font-medium ${admin.is_active
                                                        ? 'bg-green-900/50 text-green-300'
                                                        : 'bg-gray-700 text-gray-400'
                                                    }`}
                                            >
                                                {admin.is_active
                                                    ? t('admin.administrators.status.active')
                                                    : t('admin.administrators.status.inactive')}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <div className="flex items-center gap-2">
                                                {admin.role !== 'super_admin' && (
                                                    <>
                                                        <button
                                                            onClick={() => handleEditPermissions(admin)}
                                                            className="p-2 hover:bg-gray-600 rounded-lg transition-colors text-blue-400 hover:text-blue-300"
                                                            title={t('admin.administrators.actions.editPermissions')}
                                                        >
                                                            <Edit2 className="w-4 h-4" />
                                                        </button>
                                                        <button
                                                            onClick={() => handleDeleteAdmin(admin)}
                                                            className="p-2 hover:bg-gray-600 rounded-lg transition-colors text-red-400 hover:text-red-300"
                                                            title={t('admin.administrators.actions.delete')}
                                                        >
                                                            <Trash2 className="w-4 h-4" />
                                                        </button>
                                                    </>
                                                )}
                                                {admin.role === 'super_admin' && (
                                                    <span className="text-gray-500 text-sm italic">
                                                        {t('admin.administrators.protected')}
                                                    </span>
                                                )}
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>

                        {filteredAdmins.length === 0 && (
                            <div className="p-12 text-center text-gray-400">
                                {t('admin.administrators.noAdmins')}
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* Modals */}
            <AddAdminModal
                isOpen={isAddModalOpen}
                onClose={() => setIsAddModalOpen(false)}
                onAdminAdded={handleAdminAdded}
            />

            {selectedAdmin && (
                <>
                    <EditPermissionsModal
                        isOpen={isEditModalOpen}
                        admin={selectedAdmin}
                        onClose={() => {
                            setIsEditModalOpen(false);
                            setSelectedAdmin(null);
                        }}
                        onPermissionsUpdated={handlePermissionsUpdated}
                    />

                    <DeleteConfirmModal
                        isOpen={isDeleteModalOpen}
                        admin={selectedAdmin}
                        onClose={() => {
                            setIsDeleteModalOpen(false);
                            setSelectedAdmin(null);
                        }}
                        onConfirm={() => handleAdminDeleted(selectedAdmin.id)}
                    />
                </>
            )}
        </div>
    );
}
