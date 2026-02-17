'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import TemplateManagement from '@/components/TemplateManagement';

export default function AdminTemplatesPage() {
    const router = useRouter();
    const [isAdmin, setIsAdmin] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        checkAdminAccess();
    }, []);

    const checkAdminAccess = async () => {
        try {
            const token = localStorage.getItem('token');

            if (!token) {
                router.push('/login');
                return;
            }

            // Verify admin role
            const response = await fetch('/api/auth/me', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                router.push('/login');
                return;
            }

            const userData = await response.json();

            if (!userData.is_admin) {
                // Not an admin - redirect to home
                router.push('/');
                return;
            }

            setIsAdmin(true);
        } catch (error) {
            console.error('Auth check failed:', error);
            router.push('/login');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto"></div>
                    <p className="mt-4 text-gray-600">Verifying access...</p>
                </div>
            </div>
        );
    }

    if (!isAdmin) {
        return null; // Will redirect
    }

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Admin Badge */}
                <div className="mb-6">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-800">
                        🔒 Admin Access Only
                    </span>
                </div>

                {/* Template Management Component */}
                <TemplateManagement />
            </div>
        </div>
    );
}
