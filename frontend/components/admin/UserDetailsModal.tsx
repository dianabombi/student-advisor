'use client';

import { useEffect, useState } from 'react';
import { X, Mail, Calendar, FileText, MessageSquare, Shield, Ban, CheckCircle } from 'lucide-react';

interface UserDetails {
    id: number;
    name: string;
    email: string;
    role: string;
    is_active: boolean;
    created_at: string;
    subscription_status: string;
    total_consultations: number;
    total_documents: number;
}

interface UserDetailsModalProps {
    userId: number;
    isOpen: boolean;
    onClose: () => void;
    onUserUpdated?: () => void;
}

export default function UserDetailsModal({ userId, isOpen, onClose, onUserUpdated }: UserDetailsModalProps) {
    const [user, setUser] = useState<UserDetails | null>(null);
    const [loading, setLoading] = useState(true);
    const [updating, setUpdating] = useState(false);

    useEffect(() => {
        if (isOpen && userId) {
            fetchUserDetails();
        }
    }, [isOpen, userId]);

    const fetchUserDetails = async () => {
        try {
            const token = localStorage.getItem('token');
            if (!token) return;

            setLoading(true);
            const response = await fetch(
                `/api/admin/users/${userId}`,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );

            if (response.ok) {
                const data = await response.json();
                setUser(data);
            }
        } catch (error) {
            console.error('Failed to fetch user details:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleToggleStatus = async () => {
        if (!user) return;

        try {
            const token = localStorage.getItem('token');
            if (!token) return;

            setUpdating(true);
            const response = await fetch(
                `/api/admin/users/${userId}/status`,
                {
                    method: 'PUT',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ is_active: !user.is_active })
                }
            );

            if (response.ok) {
                // Update local state
                setUser({ ...user, is_active: !user.is_active });
                // Notify parent to refresh
                if (onUserUpdated) {
                    onUserUpdated();
                }
            }
        } catch (error) {
            console.error('Failed to update user status:', error);
        } finally {
            setUpdating(false);
        }
    };

    const formatDate = (dateString: string) => {
        try {
            return new Date(dateString).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch {
            return dateString;
        }
    };

    const getInitials = (name: string) => {
        return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    };

    const getRoleBadgeColor = (role: string) => {
        switch (role) {
            case 'admin':
                return 'bg-red-900/50 text-red-300 border-red-700';
            case 'partner_lawyer':
                return 'bg-purple-900/50 text-purple-300 border-purple-700';
            default:
                return 'bg-blue-900/50 text-blue-300 border-blue-700';
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
            <div className="bg-gray-800 rounded-2xl border border-gray-700 max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
                {/* Header */}
                <div className="sticky top-0 bg-gray-800 border-b border-gray-700 p-6 flex items-center justify-between">
                    <h2 className="text-2xl font-bold text-white">User Details</h2>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-gray-700 rounded-lg transition-colors text-gray-400 hover:text-white"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Content */}
                {loading ? (
                    <div className="p-12 text-center">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                        <p className="mt-4 text-gray-400">Loading user details...</p>
                    </div>
                ) : user ? (
                    <div className="p-6 space-y-6">
                        {/* User Avatar & Name */}
                        <div className="flex items-center gap-4">
                            <div className="w-20 h-20 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white text-2xl font-bold">
                                {getInitials(user.name)}
                            </div>
                            <div className="flex-1">
                                <h3 className="text-2xl font-bold text-white">{user.name}</h3>
                                <div className="flex items-center gap-2 mt-2">
                                    <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getRoleBadgeColor(user.role)}`}>
                                        {user.role}
                                    </span>
                                    {user.is_active ? (
                                        <span className="flex items-center gap-1 text-green-400 text-sm">
                                            <CheckCircle className="w-4 h-4" />
                                            Active
                                        </span>
                                    ) : (
                                        <span className="flex items-center gap-1 text-red-400 text-sm">
                                            <Ban className="w-4 h-4" />
                                            Blocked
                                        </span>
                                    )}
                                </div>
                            </div>
                        </div>

                        {/* Details Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {/* Email */}
                            <div className="bg-gray-900 rounded-xl p-4 border border-gray-700">
                                <div className="flex items-center gap-3">
                                    <div className="p-2 bg-blue-900/50 rounded-lg">
                                        <Mail className="w-5 h-5 text-blue-400" />
                                    </div>
                                    <div>
                                        <p className="text-xs text-gray-400 uppercase">Email</p>
                                        <p className="text-white font-medium">{user.email}</p>
                                    </div>
                                </div>
                            </div>

                            {/* Registration Date */}
                            <div className="bg-gray-900 rounded-xl p-4 border border-gray-700">
                                <div className="flex items-center gap-3">
                                    <div className="p-2 bg-purple-900/50 rounded-lg">
                                        <Calendar className="w-5 h-5 text-purple-400" />
                                    </div>
                                    <div>
                                        <p className="text-xs text-gray-400 uppercase">Registered</p>
                                        <p className="text-white font-medium">{formatDate(user.created_at)}</p>
                                    </div>
                                </div>
                            </div>

                            {/* Consultations */}
                            <div className="bg-gray-900 rounded-xl p-4 border border-gray-700">
                                <div className="flex items-center gap-3">
                                    <div className="p-2 bg-green-900/50 rounded-lg">
                                        <MessageSquare className="w-5 h-5 text-green-400" />
                                    </div>
                                    <div>
                                        <p className="text-xs text-gray-400 uppercase">Consultations</p>
                                        <p className="text-white font-medium text-2xl">{user.total_consultations}</p>
                                    </div>
                                </div>
                            </div>

                            {/* Documents */}
                            <div className="bg-gray-900 rounded-xl p-4 border border-gray-700">
                                <div className="flex items-center gap-3">
                                    <div className="p-2 bg-orange-900/50 rounded-lg">
                                        <FileText className="w-5 h-5 text-orange-400" />
                                    </div>
                                    <div>
                                        <p className="text-xs text-gray-400 uppercase">Documents</p>
                                        <p className="text-white font-medium text-2xl">{user.total_documents}</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Subscription Status */}
                        {user.subscription_status && (
                            <div className="bg-gray-900 rounded-xl p-4 border border-gray-700">
                                <div className="flex items-center gap-3">
                                    <div className="p-2 bg-yellow-900/50 rounded-lg">
                                        <Shield className="w-5 h-5 text-yellow-400" />
                                    </div>
                                    <div>
                                        <p className="text-xs text-gray-400 uppercase">Subscription Status</p>
                                        <p className="text-white font-medium capitalize">{user.subscription_status}</p>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Actions */}
                        <div className="flex gap-3 pt-4 border-t border-gray-700">
                            <button
                                onClick={handleToggleStatus}
                                disabled={updating}
                                className={`flex-1 px-6 py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 ${user.is_active
                                        ? 'bg-red-600 hover:bg-red-700 text-white'
                                        : 'bg-green-600 hover:bg-green-700 text-white'
                                    } ${updating ? 'opacity-50 cursor-not-allowed' : ''}`}
                            >
                                {updating ? (
                                    <>
                                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                                        Updating...
                                    </>
                                ) : user.is_active ? (
                                    <>
                                        <Ban className="w-5 h-5" />
                                        Block User
                                    </>
                                ) : (
                                    <>
                                        <CheckCircle className="w-5 h-5" />
                                        Activate User
                                    </>
                                )}
                            </button>
                            <button
                                onClick={onClose}
                                className="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg font-medium transition-colors"
                            >
                                Close
                            </button>
                        </div>
                    </div>
                ) : (
                    <div className="p-12 text-center text-gray-400">
                        User not found
                    </div>
                )}
            </div>
        </div>
    );
}
