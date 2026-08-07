"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

interface ServiceStatus {
  name: string;
  status: "healthy" | "unhealthy" | "unreachable";
  code: number | null;
}

export default function StatusPage() {
  const [services, setServices] = useState<ServiceStatus[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/status")
      .then((res) => res.json())
      .then((data) => {
        setServices(data);
        setLoading(false);
      });
  }, []);

  const color = (status: string) =>
    status === "healthy" ? "#4CAF50" : status === "unhealthy" ? "#FF9900" : "#D9534F";

  return (
    <>
      <Header />
      <div className="status-page">
        <Link href="/">&larr; Back to store</Link>
        <h1 style={{ marginTop: 12 }}>Service Status</h1>
        {loading && <p>Checking services...</p>}
        <ul className="status-list">
          {services.map((svc) => (
            <li key={svc.name}>
              <span className="dot" style={{ backgroundColor: color(svc.status) }} />
              <strong>{svc.name}</strong>
              <span style={{ marginLeft: "auto", color: "#565959" }}>
                {svc.status} {svc.code ? `(${svc.code})` : ""}
              </span>
            </li>
          ))}
        </ul>
      </div>
      <Footer />
    </>
  );
}
