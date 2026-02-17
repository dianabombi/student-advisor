export function StatCardSkeleton() {
    return (
        <div className="bg-gray-800 rounded-xl border border-gray-700 p-6 animate-pulse">
            <div className="flex items-center justify-between">
                <div className="flex-1">
                    <div className="h-4 bg-gray-700 rounded w-24 mb-3"></div>
                    <div className="h-8 bg-gray-700 rounded w-16"></div>
                </div>
                <div className="w-12 h-12 bg-gray-700 rounded-lg"></div>
            </div>
        </div>
    );
}

export function TableRowSkeleton() {
    return (
        <tr className="border-b border-gray-800 animate-pulse">
            <td className="px-6 py-4">
                <div className="h-4 bg-gray-700 rounded w-32"></div>
            </td>
            <td className="px-6 py-4">
                <div className="h-4 bg-gray-700 rounded w-48"></div>
            </td>
            <td className="px-6 py-4">
                <div className="h-4 bg-gray-700 rounded w-24"></div>
            </td>
            <td className="px-6 py-4">
                <div className="h-6 bg-gray-700 rounded-full w-20"></div>
            </td>
            <td className="px-6 py-4">
                <div className="flex gap-2">
                    <div className="h-8 bg-gray-700 rounded w-16"></div>
                    <div className="h-8 bg-gray-700 rounded w-16"></div>
                </div>
            </td>
        </tr>
    );
}

export function ChartSkeleton() {
    return (
        <div className="bg-gray-800 rounded-xl border border-gray-700 animate-pulse">
            <div className="p-6 border-b border-gray-700">
                <div className="h-6 bg-gray-700 rounded w-32"></div>
            </div>
            <div className="p-6">
                <div className="h-[300px] bg-gray-700/30 rounded"></div>
            </div>
        </div>
    );
}

export function ActivityFeedSkeleton() {
    return (
        <div className="space-y-4">
            {[...Array(5)].map((_, i) => (
                <div key={i} className="flex items-start gap-4 animate-pulse">
                    <div className="w-10 h-10 bg-gray-700 rounded-full flex-shrink-0"></div>
                    <div className="flex-1 space-y-2">
                        <div className="h-4 bg-gray-700 rounded w-3/4"></div>
                        <div className="h-3 bg-gray-700 rounded w-1/4"></div>
                    </div>
                </div>
            ))}
        </div>
    );
}

export function FormSkeleton() {
    return (
        <div className="space-y-6 animate-pulse">
            {[...Array(4)].map((_, i) => (
                <div key={i} className="space-y-2">
                    <div className="h-4 bg-gray-700 rounded w-32"></div>
                    <div className="h-10 bg-gray-700 rounded w-full"></div>
                </div>
            ))}
            <div className="h-10 bg-gray-700 rounded w-24"></div>
        </div>
    );
}
