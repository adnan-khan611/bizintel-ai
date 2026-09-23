"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface ProductCategoryChartProps {
  data: Record<string, number>;
}

interface ChartDataPoint {
  category: string;
  products: number;
}

function formatCategory(category: string): string {
  return category
    .replace(/_/g, " ")
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

export default function ProductCategoryChart({
  data,
}: ProductCategoryChartProps) {
  const chartData: ChartDataPoint[] = Object.entries(data ?? {})
    .map(([category, products]) => ({
      category: formatCategory(category),
      products: Number(products),
    }))
    .sort((a, b) => b.products - a.products);

  return (
    <div className="mt-6 w-full overflow-x-auto">
      <BarChart
        width={700}
        height={300}
        data={chartData}
        margin={{
          top: 10,
          right: 20,
          left: 10,
          bottom: 40,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />

        <XAxis
          dataKey="category"
          angle={-35}
          textAnchor="end"
          interval={0}
          height={80}
          tick={{ fontSize: 10 }}
        />

        <YAxis
          tick={{ fontSize: 11 }}
        />

        <Tooltip />

        <Bar
          dataKey="products"
          fill="#2563eb"
          radius={[4, 4, 0, 0]}
        />
      </BarChart>
    </div>
  );
}