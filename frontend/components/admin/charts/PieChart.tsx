'use client';

import { PieChart as RechartsPieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface DataPoint {
    name: string;
    value: number;
}

interface PieChartProps {
    data: DataPoint[];
    colors?: string[];
    height?: number;
    innerRadius?: number;
    outerRadius?: number;
}

const DEFAULT_COLORS = [
    '#3B82F6', // blue
    '#10B981', // green
    '#8B5CF6', // purple
    '#F59E0B', // amber
    '#EF4444', // red
    '#EC4899', // pink
    '#06B6D4', // cyan
    '#F97316', // orange
];

export default function PieChart({
    data,
    colors = DEFAULT_COLORS,
    height = 300,
    innerRadius = 0,
    outerRadius = 80
}: PieChartProps) {
    return (
        <ResponsiveContainer width="100%" height={height}>
            <RechartsPieChart>
                <Pie
                    data={data}
                    cx="50%"
                    cy="50%"
                    innerRadius={innerRadius}
                    outerRadius={outerRadius}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    labelLine={{ stroke: '#9CA3AF' }}
                >
                    {data.map((entry, index) => (
                        <Cell
                            key={`cell-${index}`}
                            fill={colors[index % colors.length]}
                        />
                    ))}
                </Pie>
                <Tooltip
                    contentStyle={{
                        backgroundColor: '#1F2937',
                        border: '1px solid #374151',
                        borderRadius: '8px',
                        color: '#F3F4F6'
                    }}
                />
                <Legend
                    wrapperStyle={{ color: '#9CA3AF' }}
                    iconType="circle"
                />
            </RechartsPieChart>
        </ResponsiveContainer>
    );
}
