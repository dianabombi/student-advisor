'use client';

import { useEffect, useState } from 'react';

interface Activity {
    id: number;
    type: string;
    user_email: string;
    timestamp: string;
    details: string;
}

interface ActivityFeedProps {
    limit?: number;
    autoRefresh?: boolean;
    refreshInterval?: number; // in seconds
}

export default function ActivityFeed({
    limit = 10,
    autoRefresh = true,
    refreshInterval = 30
}: ActivityFeedProps) {
    const [activities, setActivities] = useState<Activity[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchActivities = async () => {
        try {
            const token = localStorage.getItem('token');
            if (!token) return;

            const response = await fetch(
                `/api/admin/stats/recent-activity?limit=${limit}`,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            );

            if (response.ok) {
                const data = await response.json();
                setActivities(data);
            }
        } catch (error) {
            console.error('Failed to fetch activities:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchActivities();

        if (autoRefresh) {
            const interval = setInterval(() => {
                fetchActivities();
            }, refreshInterval * 1000);

            return () => clearInterval(interval);
        }
    }, [limit, autoRefresh, refreshInterval]);

    const getActivityIcon = (type: string) => {
        switch (type) {
            case 'registration':
                return '🟢';
            case 'consultation':
                return '🔵';
            case 'document_upload':
                return '🟠';
            case 'university_chat':
                return '💬';
            case 'subscription':
                return '⭐';
            default:
                return '📌';
        }
    };

    const getActivityColor = (type: string) => {
        switch (type) {
            case 'registration':
                return 'text-green-400';
            case 'consultation':
                return 'text-blue-400';
            case 'document_upload':
                return 'text-orange-400';
            case 'university_chat':
                return 'text-purple-400';
            case 'subscription':
                return 'text-yellow-400';
            default:
                return 'text-gray-400';
        }
    };

    const formatTimeAgo = (timestamp: string) => {
        try {
            const now = new Date();
            const activityTime = new Date(timestamp);
            const diffMs = now.getTime() - activityTime.getTime();
            const diffMins = Math.floor(diffMs / 60000);
            const diffHours = Math.floor(diffMs / 3600000);
            const diffDays = Math.floor(diffMs / 86400000);

            if (diffMins < 1) return 'just now';
            if (diffMins < 60) return `${diffMins} min ago`;
            if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
            if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;

            return activityTime.toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                year: activityTime.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
            });
        } catch {
            return timestamp;
        }
    };

    if (loading) {
        return (
            <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                    <div key={i} className="flex items-center gap-4 animate-pulse">
                        <div className="w-10 h-10 bg-gray-700 rounded-lg"></div>
                        <div className="flex-1 space-y-2">
                            <div className="h-4 bg-gray-700 rounded w-3/4"></div>
                            <div className="h-3 bg-gray-700 rounded w-1/2"></div>
                        </div>
                    </div>
                ))}
            </div>
        );
    }

    if (activities.length === 0) {
        return (
            <div className="text-center py-8 text-gray-400">
                No recent activity
            </div>
        );
    }

    return (
        <div className="space-y-3">
            {activities.map((activity) => (
                <div
                    key={activity.id}
                    className="flex items-start gap-4 p-4 rounded-lg hover:bg-gray-700/50 transition-colors"
                >
                    <div className="w-10 h-10 bg-gray-700 rounded-lg flex items-center justify-center text-xl flex-shrink-0">
                        {getActivityIcon(activity.type)}
                    </div>
                    <div className="flex-1 min-w-0">
                        <p className={`font-medium ${getActivityColor(activity.type)}`}>
                            {activity.details}
                        </p>
                        <p className="text-gray-400 text-sm mt-1">
                            {activity.user_email} • {formatTimeAgo(activity.timestamp)}
                        </p>
                    </div>
                </div>
            ))}
        </div>
    );
}
