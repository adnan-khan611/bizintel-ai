"use client";

import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface GrowthTrendChartProps {
  revenueGrowth: Record<string, number>;
  orderGrowth: Record<string, number>;
}

interface ChartDataPoint {
  month: string;
  revenueGrowth: number;
  orderGrowth: number;
}

export default function GrowthTrendChart({
  revenueGrowth,
  orderGrowth,
}: GrowthTrendChartProps) {
  const months = new Set([
    ...Object.keys(revenueGrowth ?? {}),
    ...Object.keys(orderGrowth ?? {}),
  ]);

  const chartData: ChartDataPoint[] = Array.from(months)
    .map((month) => ({
      month,
      revenueGrowth: Number(revenueGrowth?.[month] ?? 0),
      orderGrowth: Number(orderGrowth?.[month] ?? 0),
    }))
    .sort((a, b) => a.month.localeCompare(b.month));

  return (
    <div className="mt-6 w-full overflow-x-auto">
      <LineChart
        width={800}
        height={320}
        data={chartData}
        margin={{
          top: 10,
          right: 30,
          left: 20,
          bottom: 20,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />

        <XAxis
          dataKey="month"
          tick={{ fontSize: 11 }}
          interval="preserveStartEnd"
        />

        <YAxis
          tick={{ fontSize: 11 }}
          tickFormatter={(value) => `${Number(value).toFixed(0)}%`}
        />

        <Tooltip
          formatter={(value) => [
            `${Number(value).toFixed(2)}%`,
          ]}
        />

        <Legend />

        <Line
          type="monotone"
          dataKey="revenueGrowth"
          name="Revenue Growth"
          stroke="#2563eb"
          strokeWidth={3}
          dot={{ r: 3 }}
          activeDot={{ r: 6 }}
        />

        <Line
          type="monotone"
          dataKey="orderGrowth"
          name="Order Growth"
          stroke="#16a34a"
          strokeWidth={3}
          dot={{ r: 3 }}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </div>
  );
}