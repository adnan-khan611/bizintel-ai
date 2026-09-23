import CustomerOrderDistributionChart from "@/components/CustomerOrderDistributionChart";
import GrowthTrendChart from "@/components/GrowthTrendChart";
import OrdersStatusChart from "@/components/OrdersStatusChart";
import ProductCategoryChart from "@/components/ProductCategoryChart";
import RevenueTrendChart from "@/components/RevenueTrendChart";
import {
  getCustomersAnalytics,
  getForecast,
  getGrowthAnalytics,
  getOrdersAnalytics,
  getProductsAnalytics,
  getRevenueAnalytics,
} from "@/lib/api";

function formatCurrency(minorUnits: number): string {
  const rupees = minorUnits / 100;

  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(rupees);
}

function formatForecastCurrency(value: number): string {
  const crore = value / 10000000;

  return `₹${crore.toFixed(2)} Cr`;
}

function formatForecastMonth(month: string): string {
  const [year, monthNumber] = month.split("-");

  if (!year || !monthNumber) {
    return month;
  }

  const date = new Date(
    Number(year),
    Number(monthNumber) - 1,
    1,
  );

  return new Intl.DateTimeFormat("en-IN", {
    month: "long",
    year: "numeric",
  }).format(date);
}

export default async function Home() {
  const revenue = await getRevenueAnalytics();
  const orders = await getOrdersAnalytics();
  const customers = await getCustomersAnalytics();
  const products = await getProductsAnalytics();
  const growth = await getGrowthAnalytics();
  const forecast = await getForecast();

  const monthlyRevenue = growth.monthly_revenue ?? {};

  const kpiCards = [
    {
      title: "Revenue",
      value: formatCurrency(revenue.merchandise_revenue_minor),
      description: "Total merchandise revenue",
    },
    {
      title: "Orders",
      value: orders.total_orders.toLocaleString("en-IN"),
      description: "Total orders",
    },
    {
      title: "Customers",
      value: customers.unique_customers.toLocaleString("en-IN"),
      description: "Unique customers",
    },
    {
      title: "Products",
      value: products.total_products.toLocaleString("en-IN"),
      description: "Products in catalog",
    },
  ];

  const orderStatusCards = [
    {
      title: "Delivered",
      value: orders.delivered_orders,
    },
    {
      title: "Cancelled",
      value: orders.canceled_orders,
    },
    {
      title: "Unavailable",
      value: orders.unavailable_orders,
    },
  ];

  return (
    <main className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-7xl px-6 py-8 lg:px-8">
        <header className="mb-8">
          <p className="text-sm font-medium text-blue-600">
            Business Intelligence
          </p>

          <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-900">
            BizIntel AI
          </h1>

          <p className="mt-2 max-w-2xl text-slate-600">
            AI-powered business intelligence and decision assistant for
            understanding business performance and making data-driven
            decisions.
          </p>
        </header>

        <section
          aria-label="Business performance indicators"
          className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4"
        >
          {kpiCards.map((card) => (
            <article
              key={card.title}
              className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"
            >
              <p className="text-sm font-medium text-slate-500">
                {card.title}
              </p>

              <p className="mt-3 text-3xl font-bold text-slate-900">
                {card.value}
              </p>

              <p className="mt-2 text-sm text-slate-500">
                {card.description}
              </p>
            </article>
          ))}
        </section>

        <section className="mt-6 grid gap-6 lg:grid-cols-2">
          <article className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">
              Revenue Trend
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Monthly revenue performance over time.
            </p>

            <RevenueTrendChart data={monthlyRevenue} />
          </article>

          <article className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">
              Revenue Forecast
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Forecast for the next available month based on historical
              revenue.
            </p>

            <div className="mt-6 rounded-lg border border-slate-200 bg-slate-50 p-6">
              <p className="text-sm font-medium text-slate-500">
                Forecast Month
              </p>

              <p className="mt-2 text-xl font-semibold text-slate-900">
                {formatForecastMonth(forecast.forecast_month)}
              </p>

              <p className="mt-6 text-sm font-medium text-slate-500">
                Forecast Revenue
              </p>

              <p className="mt-2 text-4xl font-bold text-blue-600">
                {formatForecastCurrency(forecast.forecast_revenue)}
              </p>
            </div>
          </article>
        </section>

        <section className="mt-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">
              Orders Overview
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Order fulfillment and availability breakdown.
            </p>
          </div>

          <div className="mt-6 grid gap-4 sm:grid-cols-3">
            {orderStatusCards.map((card) => (
              <article
                key={card.title}
                className="rounded-lg border border-slate-200 bg-slate-50 p-4"
              >
                <p className="text-sm font-medium text-slate-500">
                  {card.title}
                </p>

                <p className="mt-2 text-2xl font-bold text-slate-900">
                  {card.value.toLocaleString("en-IN")}
                </p>
              </article>
            ))}
          </div>

          <OrdersStatusChart data={orders.orders_by_status} />
        </section>

        <section className="mt-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">
              Customers Overview
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Customer activity and order distribution.
            </p>
          </div>

          <div className="mt-6 grid gap-4 sm:grid-cols-2">
            <article className="rounded-lg border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm font-medium text-slate-500">
                Unique Customers
              </p>

              <p className="mt-2 text-2xl font-bold text-slate-900">
                {customers.unique_customers.toLocaleString("en-IN")}
              </p>
            </article>

            <article className="rounded-lg border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm font-medium text-slate-500">
                Orders per Customer
              </p>

              <p className="mt-2 text-2xl font-bold text-slate-900">
                {customers.orders_per_customer.toFixed(2)}
              </p>
            </article>
          </div>

          <CustomerOrderDistributionChart
            data={customers.customer_order_distribution}
          />
        </section>

        <section className="mt-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">
              Products Overview
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Product catalog and category distribution.
            </p>
          </div>

          <div className="mt-6">
            <article className="rounded-lg border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm font-medium text-slate-500">
                Total Products
              </p>

              <p className="mt-2 text-2xl font-bold text-slate-900">
                {products.total_products.toLocaleString("en-IN")}
              </p>
            </article>
          </div>

          <ProductCategoryChart
            data={products.products_by_category}
          />
        </section>

        <section className="mt-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">
              Growth Overview
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Monthly revenue and order growth compared with the previous
              period.
            </p>
          </div>

          <GrowthTrendChart
            revenueGrowth={growth.revenue_growth}
            orderGrowth={growth.order_growth}
          />
        </section>
      </div>
    </main>
  );
}