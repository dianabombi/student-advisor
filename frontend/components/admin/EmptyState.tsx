import { FileQuestion, Users, GraduationCap, Activity } from 'lucide-react';

interface EmptyStateProps {
    icon?: React.ReactNode;
    title: string;
    description: string;
    action?: {
        label: string;
        onClick: () => void;
    };
}

export default function EmptyState({ icon, title, description, action }: EmptyStateProps) {
    return (
        <div className="flex flex-col items-center justify-center py-12 px-4">
            <div className="w-16 h-16 bg-gray-800 rounded-full flex items-center justify-center mb-4">
                {icon || <FileQuestion className="w-8 h-8 text-gray-600" />}
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">{title}</h3>
            <p className="text-gray-400 text-center max-w-md mb-6">{description}</p>
            {action && (
                <button
                    onClick={action.onClick}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                    {action.label}
                </button>
            )}
        </div>
    );
}

// Preset empty states
export function NoUsersFound() {
    return (
        <EmptyState
            icon={<Users className="w-8 h-8 text-gray-600" />}
            title="No users found"
            description="There are no users matching your search criteria. Try adjusting your filters or search term."
        />
    );
}

export function NoUniversitiesFound() {
    return (
        <EmptyState
            icon={<GraduationCap className="w-8 h-8 text-gray-600" />}
            title="No universities found"
            description="There are no universities matching your search criteria. Try adjusting your filters or search term."
        />
    );
}

export function NoActivityFound() {
    return (
        <EmptyState
            icon={<Activity className="w-8 h-8 text-gray-600" />}
            title="No recent activity"
            description="There hasn't been any user activity yet. Activity will appear here once users start using the platform."
        />
    );
}
