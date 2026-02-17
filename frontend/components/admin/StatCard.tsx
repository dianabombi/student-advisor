interface StatCardProps {
    title: string;
    value: number | string;
    icon: React.ReactNode;
    trend?: {
        value: number;
        isPositive: boolean;
    };
    loading?: boolean;
}

export default function StatCard({ title, value, icon, trend, loading }: StatCardProps) {
    if (loading) {
        return (
            <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 animate-pulse">
                <div className="flex items-center justify-between">
                    <div className="space-y-3 flex-1">
                        <div className="h-4 bg-gray-700 rounded w-1/2"></div>
                        <div className="h-8 bg-gray-700 rounded w-3/4"></div>
                    </div>
                    <div className="w-12 h-12 bg-gray-700 rounded-lg"></div>
                </div>
            </div>
        );
    }

    return (
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 hover:border-gray-600 transition-all duration-200 hover:shadow-lg hover:shadow-blue-500/10">
            <div className="flex items-center justify-between">
                <div className="space-y-2">
                    <p className="text-gray-400 text-sm font-medium">{title}</p>
                    <p className="text-3xl font-bold text-white">{value}</p>

                    {trend && (
                        <div className={`flex items-center gap-1 text-sm ${trend.isPositive ? 'text-green-400' : 'text-red-400'
                            }`}>
                            <span>{trend.isPositive ? '↑' : '↓'}</span>
                            <span>{Math.abs(trend.value)}%</span>
                            <span className="text-gray-500">vs last month</span>
                        </div>
                    )}
                </div>

                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white">
                    {icon}
                </div>
            </div>
        </div>
    );
}
