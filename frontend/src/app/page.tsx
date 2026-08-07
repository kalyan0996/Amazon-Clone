"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiClient } from "@/lib/apiClient";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import ProductIcon from "@/components/ProductIcon";

interface GatewayItem {
  id: string;
  name: string;
  is_active: boolean;
}

const CATEGORIES: { name: string; slug: string; icon: "electronics" | "home" | "fashion" | "books" | "toys" | "beauty" }[] = [
  { name: "Electronics", slug: "electronics", icon: "electronics" },
  { name: "Home & Kitchen", slug: "home-kitchen", icon: "home" },
  { name: "Fashion", slug: "fashion", icon: "fashion" },
  { name: "Books", slug: "books", icon: "books" },
  { name: "Toys & Games", slug: "toys-games", icon: "toys" },
  { name: "Beauty", slug: "beauty", icon: "beauty" },
];

const ICON_TYPES = ["electronics", "home", "fashion", "books", "toys", "beauty", "generic"] as const;

function fakePrice(seed: string) {
  let hash = 0;
  for (let i = 0; i < seed.length; i++) hash = seed.charCodeAt(i) + ((hash << 5) - hash);
  const dollars = 9 + (Math.abs(hash) % 190);
  const cents = Math.abs(hash) % 100;
  return { dollars, cents: cents.toString().padStart(2, "0") };
}

function iconFor(seed: string) {
  let hash = 0;
  for (let i = 0; i < seed.length; i++) hash = seed.charCodeAt(i) + ((hash << 5) - hash);
  return ICON_TYPES[Math.abs(hash) % ICON_TYPES.length];
}

export default function HomePage() {
  const [items, setItems] = useState<GatewayItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [slide, setSlide] = useState(0);

  useEffect(() => {
    apiClient
      .get("/api/v1/gateway/items/")
      .then((res) => setItems(res.data.results ?? res.data))
      .catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    const t = setInterval(() => setSlide((s) => (s + 1) % 3), 4000);
    return () => clearInterval(t);
  }, []);

  return (
    <>
      <Header />

      <div className="hero-carousel">
        <div className={`hero-slide s1 ${slide === 0 ? "active" : ""}`}>Welcome to Amazon Clone</div>
        <div className={`hero-slide s2 ${slide === 1 ? "active" : ""}`}>Big Savings, Every Day</div>
        <div className={`hero-slide s3 ${slide === 2 ? "active" : ""}`}>New Arrivals Just In</div>
        <div className="hero-fade" />
      </div>

      <div className="content">
        <Link href="/status">
          <button className="status-btn">View All Services</button>
        </Link>

        <div className="section-block">
          <h2>Shop by Category</h2>
          <div className="category-grid">
            {CATEGORIES.map((cat) => (
              <Link href={`/category/${cat.slug}`} key={cat.slug} className="card-link">
                <div className="category-tile">
                  <div className="img-placeholder" style={{ padding: 0, overflow: "hidden" }}>
                    <ProductIcon type={cat.icon} />
                  </div>
                  <div className="label">{cat.name}</div>
                  <div className="shop-now">Shop now</div>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {items.length > 0 && (
          <div className="section-block">
            <h2>Today's Deals</h2>
            <div className="deals-row">
              {items.map((item) => {
                const price = fakePrice(item.id);
                const was = price.dollars + 20;
                return (
                  <Link href={`/product/${item.id}`} key={item.id} className="card-link">
                    <div className="deal-card">
                      <span className="deal-badge">DEAL</span>
                      <div className="img-placeholder" style={{ padding: 0, overflow: "hidden" }}>
                        <ProductIcon type={iconFor(item.id)} />
                      </div>
                      <div className="name">{item.name}</div>
                      <span className="price">${price.dollars}.{price.cents}</span>
                      <span className="was-price">${was}.00</span>
                    </div>
                  </Link>
                );
              })}
            </div>
          </div>
        )}

        <div className="section-block">
          <h2>Recommended for You</h2>
          {error && <p style={{ color: "red" }}>Error: {error}</p>}
          {!error && items.length === 0 && (
            <div className="empty-state">
              <p>No products yet. Check back soon.</p>
            </div>
          )}
          <div className="product-grid">
            {items.map((item) => {
              const price = fakePrice(item.id);
              return (
                <Link href={`/product/${item.id}`} key={item.id} className="card-link">
                  <div className="product-card">
                    <div className="img-placeholder" style={{ padding: 0, overflow: "hidden" }}>
                      <ProductIcon type={iconFor(item.id)} />
                    </div>
                    <div className="name">{item.name}</div>
                    <div className="rating">★★★★☆ 128</div>
                    <div className="price">
                      <span style={{ fontSize: 12 }}>$</span>
                      {price.dollars}
                      <span className="cents">{price.cents}</span>
                    </div>
                    <button onClick={(e) => e.preventDefault()}>Add to Cart</button>
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      </div>

      <Footer />
    </>
  );
}
