"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { apiClient } from "@/lib/apiClient";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import ProductIcon from "@/components/ProductIcon";

interface GatewayItem {
  id: string;
  name: string;
  is_active: boolean;
}

export default function CategoryPage() {
  const params = useParams();
  const slug = params?.slug as string;
  const [items, setItems] = useState<GatewayItem[]>([]);

  useEffect(() => {
    apiClient
      .get("/api/v1/gateway/items/")
      .then((res) => setItems(res.data.results ?? res.data))
      .catch(() => setItems([]));
  }, []);

  const label = slug?.replace("-", " & ").replace(/\b\w/g, (c) => c.toUpperCase());

  return (
    <>
      <Header />
      <div className="content">
        <Link href="/">&larr; Back to home</Link>
        <div className="section-block">
          <h2>{label}</h2>
          <p style={{ color: "#565959", marginBottom: 12, fontSize: 13 }}>
            Category filtering isn't wired to the backend yet — showing all available items.
          </p>
          <div className="product-grid">
            {items.map((item) => (
              <Link href={`/product/${item.id}`} key={item.id} className="card-link">
                <div className="product-card">
                  <div className="img-placeholder" style={{ padding: 0, overflow: "hidden" }}>
                    <ProductIcon type="generic" />
                  </div>
                  <div className="name">{item.name}</div>
                  <button onClick={(e) => e.preventDefault()}>Add to Cart</button>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
}
