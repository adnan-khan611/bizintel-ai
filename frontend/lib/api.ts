const API_BASE_URL = "http://127.0.0.1:8000";

export interface HealthResponse {
  status: string;
}

export interface RevenueResponse {
  merchandise_revenue_minor: number;
  freight_value_minor: number;
  payment_value_minor: number;
}

export interface OrdersResponse {
  total_orders: number;
  delivered_orders: number;
  canceled_orders: number;
  unavailable_orders: number;
  orders_by_status: Record<string, number>;
}

export interface CustomersResponse {
  unique_customers: number;
  orders_per_customer: number;
  customer_order_counts: Record<string, number>;
  customer_order_distribution: Record<string, number>;
}

export interface ProductsResponse {
  total_products: number;
  products_by_category: Record<string, number>;
  product_revenue: Record<string, number>;
  product_order_items: Record<string, number>;
}

export interface GrowthResponse {
  monthly_revenue: Record<string, number>;
  monthly_orders: Record<string, number>;
  monthly_unique_customers: Record<string, number>;
  revenue_growth: Record<string, number>;
  order_growth: Record<string, number>;
}

export interface ForecastResponse {
  forecast_month: string;
  forecast_revenue: number;
}

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}

export async function getRevenueAnalytics(): Promise<RevenueResponse> {
  const response = await fetch(`${API_BASE_URL}/analytics/revenue`);

  if (!response.ok) {
    throw new Error(`Revenue API request failed: ${response.status}`);
  }

  return response.json();
}

export async function getOrdersAnalytics(): Promise<OrdersResponse> {
  const response = await fetch(`${API_BASE_URL}/analytics/orders`);

  if (!response.ok) {
    throw new Error(`Orders API request failed: ${response.status}`);
  }

  return response.json();
}

export async function getCustomersAnalytics(): Promise<CustomersResponse> {
  const response = await fetch(`${API_BASE_URL}/analytics/customers`);

  if (!response.ok) {
    throw new Error(`Customers API request failed: ${response.status}`);
  }

  return response.json();
}

export async function getProductsAnalytics(): Promise<ProductsResponse> {
  const response = await fetch(`${API_BASE_URL}/analytics/products`);

  if (!response.ok) {
    throw new Error(`Products API request failed: ${response.status}`);
  }

  return response.json();
}

export async function getGrowthAnalytics(): Promise<GrowthResponse> {
  const response = await fetch(`${API_BASE_URL}/analytics/growth`);

  if (!response.ok) {
    throw new Error(`Growth API request failed: ${response.status}`);
  }

  return response.json();
}

export async function getForecast(): Promise<ForecastResponse> {
  const response = await fetch(`${API_BASE_URL}/analytics/forecast`);

  if (!response.ok) {
    throw new Error(`Forecast API request failed: ${response.status}`);
  }

  return response.json();
}