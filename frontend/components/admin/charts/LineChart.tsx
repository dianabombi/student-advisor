'use client';

import { LineChart as RechartsLineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface DataPoint {
    [key: string]: string | number | undefined;
}

interface LineChartProps {
    data: DataPoint[];
    lines: {
        dataKey: string;
        stroke: string;
        name?: string;
    }[];
    xAxisKey: string;
    height?: number;
}

export default function LineChart({ data, lines, xAxisKey, height = 300 }: LineChartProps) {
    return (
        <ResponsiveContainer width="100%" height={height}>
            <RechartsLineChart
                data={data}
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis
                    dataKey={xAxisKey}
                    stroke="#9CA3AF"
                    style={{ fontSize: '12px' }}
                />
                <YAxis
                    stroke="#9CA3AF"
                    style={{ fontSize: '12px' }}
                />
                <Tooltip
                    contentStyle={{
                        backgroundColor: '#1F2937',
                        border: '1px solid #374151',
                        borderRadius: '8px',
                        color: '#F3F4F6'
                    }}
                    labelStyle={{ color: '#9CA3AF' }}
                />
                <Legend
                    wrapperStyle={{ color: '#9CA3AF' }}
                    iconType="line"
                />
                {lines.map((line, index) => (
                    <Line
                        key={index}
                        type="monotone"
                        dataKey={line.dataKey}
                        stroke={line.stroke}
                        name={line.name || line.dataKey}
                        strokeWidth={2}
                        dot={{ fill: line.stroke, r: 4 }}
                        activeDot={{ r: 6 }}
                    />
                ))}
            </RechartsLineChart>
        </ResponsiveContainer>
    );
}
