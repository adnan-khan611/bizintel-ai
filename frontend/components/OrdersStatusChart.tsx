"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface OrdersStatusChartProps {
  data: Record<string, number>;
}

interface ChartDataPoint {
  status: string;
  orders: number;
}

function formatStatus(status: string): string {
  return status
    .replace(/_/g, " ")
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

export default function OrdersStatusChart({
  data,
}: OrdersStatusChartProps) {
  const chartData: ChartDataPoint[] = Object.entries(data ?? {})
    .map(([status, orders]) => ({
      status: formatStatus(status),
      orders: Number(orders),
    }))
    .sort((a, b) => b.orders - a.orders);

  return (
    <div className="mt-6 w-full overflow-x-auto">
      <BarChart
        width={600}
        height={280}
        data={chartData}
        margin={{
          top: 10,
          right: 20,
          left: 10,
          bottom: 20,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />

        <XAxis
          dataKey="status"
          tick={{ fontSize: 11 }}
        />

        <YAxis
          tick={{ fontSize: 11 }}
        />

        <Tooltip />

        <Bar
          dataKey="orders"
          fill="#2563eb"
          radius={[4, 4, 0, 0]}
        />
      </BarChart>
    </div>
  );
}