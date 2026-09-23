"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface CustomerOrderDistributionChartProps {
  data: Record<string, number>;
}

interface ChartDataPoint {
  orders: string;
  customers: number;
}

function formatOrdersLabel(value: string): string {
  if (value === "1") {
    return "1 order";
  }

  return `${value} orders`;
}

export default function CustomerOrderDistributionChart({
  data,
}: CustomerOrderDistributionChartProps) {
  const chartData: ChartDataPoint[] = Object.entries(data ?? {})
    .map(([orders, customers]) => ({
      orders: formatOrdersLabel(orders),
      customers: Number(customers),
    }))
    .sort((a, b) => {
      const aOrders = Number.parseInt(a.orders, 10);
      const bOrders = Number.parseInt(b.orders, 10);

      return aOrders - bOrders;
    });

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
          dataKey="orders"
          tick={{ fontSize: 11 }}
        />

        <YAxis
          tick={{ fontSize: 11 }}
        />

        <Tooltip />

        <Bar
          dataKey="customers"
          fill="#2563eb"
          radius={[4, 4, 0, 0]}
        />
      </BarChart>
    </div>
  );
}