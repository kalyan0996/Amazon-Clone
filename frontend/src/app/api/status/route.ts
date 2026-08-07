import { NextResponse } from "next/server";

const SERVICES: { name: string; host: string; port: number }[] = [
  { name: "api-gateway", host: "api-gateway", port: 8000 },
  { name: "auth-service", host: "auth-service", port: 8001 },
  { name: "user-service", host: "user-service", port: 8002 },
  { name: "product-service", host: "product-service", port: 8003 },
  { name: "catalog-service", host: "catalog-service", port: 8004 },
  { name: "inventory-service", host: "inventory-service", port: 8005 },
  { name: "cart-service", host: "cart-service", port: 8006 },
  { name: "order-service", host: "order-service", port: 8007 },
  { name: "payment-service", host: "payment-service", port: 8008 },
  { name: "shipping-service", host: "shipping-service", port: 8009 },
  { name: "review-service", host: "review-service", port: 8010 },
  { name: "rating-service", host: "rating-service", port: 8011 },
  { name: "recommendation-service", host: "recommendation-service", port: 8012 },
  { name: "search-service", host: "search-service", port: 8013 },
  { name: "notification-service", host: "notification-service", port: 8014 },
  { name: "wishlist-service", host: "wishlist-service", port: 8015 },
  { name: "seller-service", host: "seller-service", port: 8016 },
  { name: "pricing-service", host: "pricing-service", port: 8017 },
  { name: "analytics-service", host: "analytics-service", port: 8018 },
  { name: "admin-service", host: "admin-service", port: 8019 },
];

async function checkService(svc: { name: string; host: string; port: number }) {
  const url = `http://${svc.host}:${svc.port}/healthz/`;
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 3000);
    const res = await fetch(url, { signal: controller.signal, cache: "no-store" });
    clearTimeout(timeout);
    return { name: svc.name, status: res.ok ? "healthy" : "unhealthy", code: res.status };
  } catch {
    return { name: svc.name, status: "unreachable", code: null };
  }
}

export async function GET() {
  const results = await Promise.all(SERVICES.map(checkService));
  return NextResponse.json(results);
}
