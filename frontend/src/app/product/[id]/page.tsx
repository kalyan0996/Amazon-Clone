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

function fakePrice(seed: string) {
  let hash = 0;
  for (let i = 0; i < seed.length; i++) hash = seed.charCodeAt(i) + ((hash << 5) - hash);
  return { dollars: 9 + (Math.abs(hash) % 190), cents: (Math.abs(hash) % 100).toString().padStart(2, "0") };
}

export default function ProductPage() {
  const params = useParams();
  const id = params?.id as string;
  const [item, setItem] = useState<GatewayItem | null>(null);

  useEffect(() => {
    apiClient
      .get("/api/v1/gateway/items/")
      .then((res) => {
        const list: GatewayItem[] = res.data.results ?? res.data;
        setItem(list.find((i) => i.id === id) ?? null);
      })
      .catch(() => setItem(null));
  }, [id]);

  const price = fakePrice(id ?? "");

  return (
    <>
      <Header />
      <div className="content">
        <Link href="/">&larr; Back to home</Link>
        <div className="section-block" style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
          <div style={{ width: 280, height: 240 }}>
            <ProductIcon type="generic" />
          </div>
          <div style={{ flex: 1, minWidth: 240 }}>
            <h2>{item ? item.name : "Product not found"}</h2>
            <div className="rating">★★★★☆ 128 ratings</div>
            <div className="price" style={{ fontSize: 26, margin: "12px 0" }}>
              ${price.dollars}.{price.cents}
            </div>
            <p style={{ color: "#565959", fontSize: 13, marginBottom: 16 }}>
              Product details, images, and inventory aren't fully wired to the backend yet —
              this page is a placeholder detail view.
            </p>
            <button style={{ background: "#FFD814", border: "1px solid #FCD200", borderRadius: 20, padding: "10px 24px", cursor: "pointer" }}>
              Add to Cart
            </button>
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
}
