"use client";

import {
  CartesianGrid,
  Line,
  LineChart,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface RevenueTrendChartProps {
  data: Record<string, number>;
}

interface ChartDataPoint {
  month: string;
  revenue: number;
}

function formatCurrency(value: number): string {
  const rupees = value / 100;

  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(rupees);
}

export default function RevenueTrendChart({
  data,
}: RevenueTrendChartProps) {
  const chartData: ChartDataPoint[] = Object.entries(data ?? {})
    .map(([month, revenue]) => ({
      month,
      revenue: Number(revenue),
    }))
    .sort((a, b) => a.month.localeCompare(b.month));

  return (
    <div className="mt-6 w-full overflow-x-auto">
      <p className="mb-3 text-sm text-slate-500">
        Data points: {chartData.length}
      </p>

      <LineChart
        width={800}
        height={256}
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
          tickFormatter={(value) =>
            `₹${Math.round(Number(value) / 10000000)}Cr`
          }
        />

        <Tooltip
          formatter={(value) => [
            formatCurrency(Number(value)),
            "Revenue",
          ]}
          labelFormatter={(label) => `Month: ${label}`}
        />

        <Line
          type="monotone"
          dataKey="revenue"
          stroke="#2563eb"
          strokeWidth={3}
          dot={{ r: 3 }}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </div>
  );
}