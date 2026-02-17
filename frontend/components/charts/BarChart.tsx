'use client';

interface BarChartProps {
    data: { label: string; value: number; color?: string }[];
    maxValue?: number;
    height?: number;
}

export default function BarChart({ data, maxValue, height = 300 }: BarChartProps) {
    const max = maxValue || Math.max(...data.map((d) => d.value));

    return (
        <div className="w-full" style={{ height: `${height}px` }}>
            <div className="flex items-end justify-between gap-2 h-full">
                {data.map((item, index) => {
                    const barHeight = (item.value / max) * (height - 40);
                    const color = item.color || '#3b82f6';

                    return (
                        <div key={index} className="flex-1 flex flex-col items-center gap-2 group">
                            {/* Value label */}
                            <div className="text-xs font-semibold text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity">
                                {item.value}
                            </div>

                            {/* Bar */}
                            <div
                                className="w-full rounded-t-lg transition-all duration-300 hover:opacity-80 cursor-pointer relative"
                                style={{
                                    height: `${barHeight}px`,
                                    background: `linear-gradient(to top, ${color}, ${color}dd)`,
                                }}
                            >
                                {/* Tooltip on hover */}
                                <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-gray-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                                    {item.value}
                                </div>
                            </div>

                            {/* Label */}
                            <div className="text-xs text-gray-400 text-center max-w-full truncate px-1">
                                {item.label}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
