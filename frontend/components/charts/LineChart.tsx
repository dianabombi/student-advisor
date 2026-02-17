'use client';

interface LineChartProps {
    data: { label: string; value: number }[];
    color?: string;
    height?: number;
}

export default function LineChart({ data, color = '#3b82f6', height = 200 }: LineChartProps) {
    const maxValue = Math.max(...data.map((d) => d.value));
    const minValue = Math.min(...data.map((d) => d.value));
    const range = maxValue - minValue;
    const padding = 20;
    const width = 600;
    const chartHeight = height - padding * 2;
    const chartWidth = width - padding * 2;

    // Calculate points for the line
    const points = data.map((item, index) => {
        const x = padding + (index / (data.length - 1)) * chartWidth;
        const y = padding + chartHeight - ((item.value - minValue) / range) * chartHeight;
        return { x, y, value: item.value, label: item.label };
    });

    // Create path for the line
    const linePath = points
        .map((point, index) => `${index === 0 ? 'M' : 'L'} ${point.x} ${point.y}`)
        .join(' ');

    // Create path for the area under the line
    const areaPath = `${linePath} L ${points[points.length - 1].x} ${height - padding} L ${padding} ${height - padding} Z`;

    return (
        <div className="w-full">
            <svg width={width} height={height} className="w-full">
                {/* Grid lines */}
                {[0, 0.25, 0.5, 0.75, 1].map((ratio, index) => {
                    const y = padding + chartHeight * (1 - ratio);
                    return (
                        <g key={index}>
                            <line
                                x1={padding}
                                y1={y}
                                x2={width - padding}
                                y2={y}
                                stroke="#374151"
                                strokeWidth="1"
                                strokeDasharray="4 4"
                            />
                            <text
                                x={padding - 10}
                                y={y + 4}
                                fill="#9ca3af"
                                fontSize="10"
                                textAnchor="end"
                            >
                                {Math.round(minValue + range * ratio)}
                            </text>
                        </g>
                    );
                })}

                {/* Area under the line */}
                <path
                    d={areaPath}
                    fill={`url(#gradient-${color.replace('#', '')})`}
                    opacity="0.2"
                />

                {/* Gradient definition */}
                <defs>
                    <linearGradient
                        id={`gradient-${color.replace('#', '')}`}
                        x1="0"
                        y1="0"
                        x2="0"
                        y2="1"
                    >
                        <stop offset="0%" stopColor={color} stopOpacity="0.8" />
                        <stop offset="100%" stopColor={color} stopOpacity="0" />
                    </linearGradient>
                </defs>

                {/* Line */}
                <path
                    d={linePath}
                    fill="none"
                    stroke={color}
                    strokeWidth="3"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                />

                {/* Data points */}
                {points.map((point, index) => (
                    <g key={index} className="group">
                        <circle
                            cx={point.x}
                            cy={point.y}
                            r="5"
                            fill={color}
                            className="cursor-pointer transition-all hover:r-7"
                        />
                        <circle
                            cx={point.x}
                            cy={point.y}
                            r="8"
                            fill={color}
                            opacity="0"
                            className="group-hover:opacity-30 transition-opacity"
                        />
                        {/* Tooltip */}
                        <g className="opacity-0 group-hover:opacity-100 transition-opacity">
                            <rect
                                x={point.x - 30}
                                y={point.y - 35}
                                width="60"
                                height="25"
                                fill="#1f2937"
                                rx="4"
                            />
                            <text
                                x={point.x}
                                y={point.y - 20}
                                fill="white"
                                fontSize="12"
                                textAnchor="middle"
                                fontWeight="bold"
                            >
                                {point.value}
                            </text>
                        </g>
                    </g>
                ))}

                {/* X-axis labels */}
                {points.map((point, index) => (
                    <text
                        key={index}
                        x={point.x}
                        y={height - 5}
                        fill="#9ca3af"
                        fontSize="10"
                        textAnchor="middle"
                    >
                        {point.label}
                    </text>
                ))}
            </svg>
        </div>
    );
}
