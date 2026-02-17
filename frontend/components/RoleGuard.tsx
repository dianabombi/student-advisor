'use client';

import { ReactNode } from 'react';
import { useAuth } from '@/contexts/AuthContext';

interface RoleGuardProps {
    children: ReactNode;
    allowedRoles: string[];
    fallback?: ReactNode;
}

/**
 * Component to conditionally render content based on user role
 */
export function RoleGuard({ children, allowedRoles, fallback = null }: RoleGuardProps) {
    const { user } = useAuth();

    if (!user || !allowedRoles.includes(user.role)) {
        return <>{fallback}</>;
    }

    return <>{children}</>;
}

/**
 * Show content only to admins
 */
export function AdminOnly({ children, fallback = null }: { children: ReactNode; fallback?: ReactNode }) {
    return (
        <RoleGuard allowedRoles={['admin']} fallback={fallback}>
            {children}
        </RoleGuard>
    );
}

/**
 * Show content only to lawyers (including admins)
 */
export function LawyerOnly({ children, fallback = null }: { children: ReactNode; fallback?: ReactNode }) {
    return (
        <RoleGuard allowedRoles={['admin', 'partner_lawyer']} fallback={fallback}>
            {children}
        </RoleGuard>
    );
}

/**
 * Show content only to regular users
 */
export function UserOnly({ children, fallback = null }: { children: ReactNode; fallback?: ReactNode }) {
    return (
        <RoleGuard allowedRoles={['user']} fallback={fallback}>
            {children}
        </RoleGuard>
    );
}
