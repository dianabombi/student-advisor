'use client';

interface PieChartProps {
    data: { label: string; value: number; color: string }[];
    size?: number;
}

export default function PieChart({ data, size = 200 }: PieChartProps) {
    const total = data.reduce((sum, item) => sum + item.value, 0);
    let currentAngle = -90; // Start from top

    const slices = data.map((item) => {
        const percentage = (item.value / total) * 100;
        const angle = (percentage / 100) * 360;
        const startAngle = currentAngle;
        const endAngle = currentAngle + angle;

        currentAngle = endAngle;

        // Calculate path for pie slice
        const startRad = (startAngle * Math.PI) / 180;
        const endRad = (endAngle * Math.PI) / 180;
        const radius = size / 2 - 10;
        const centerX = size / 2;
        const centerY = size / 2;

        const x1 = centerX + radius * Math.cos(startRad);
        const y1 = centerY + radius * Math.sin(startRad);
        const x2 = centerX + radius * Math.cos(endRad);
        const y2 = centerY + radius * Math.sin(endRad);

        const largeArc = angle > 180 ? 1 : 0;

        const path = [
            `M ${centerX} ${centerY}`,
            `L ${x1} ${y1}`,
            `A ${radius} ${radius} 0 ${largeArc} 1 ${x2} ${y2}`,
            'Z',
        ].join(' ');

        return {
            path,
            color: item.color,
            label: item.label,
            percentage: percentage.toFixed(1),
        };
    });

    return (
        <div className="flex items-center gap-6">
            <svg width={size} height={size} className="transform transition-transform hover:scale-105">
                {slices.map((slice, index) => (
                    <g key={index}>
                        <path
                            d={slice.path}
                            fill={slice.color}
                            className="transition-opacity hover:opacity-80 cursor-pointer"
                        />
                    </g>
                ))}
            </svg>
            <div className="flex flex-col gap-2">
                {data.map((item, index) => (
                    <div key={index} className="flex items-center gap-2">
                        <div
                            className="w-3 h-3 rounded-sm"
                            style={{ backgroundColor: item.color }}
                        />
                        <span className="text-sm text-gray-300">
                            {item.label}: <span className="text-white font-semibold">{slices[index].percentage}%</span>
                        </span>
                    </div>
                ))}
            </div>
        </div>
    );
}
