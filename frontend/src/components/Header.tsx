"use client";

import Link from "next/link";
import { useAuth } from "@/context/AuthContext";

export default function Header() {
  const { user, logout } = useAuth();

  return (
    <>
      <header className="topnav">
        <Link href="/" className="logo">amazon</Link>
        <div className="searchbar">
          <input placeholder="Search Amazon Clone" />
          <button>🔍</button>
        </div>
        {user ? (
          <div className="navlink" onClick={logout} style={{ cursor: "pointer" }}>
            <span className="top">Hello, {user.first_name || user.email}</span>
            <span className="bottom">Sign out</span>
          </div>
        ) : (
          <Link href="/login" className="navlink">
            <span className="top">Hello, sign in</span>
            <span className="bottom">Account &amp; Lists</span>
          </Link>
        )}
        <div className="navlink">
          <span className="top">Returns</span>
          <span className="bottom">&amp; Orders</span>
        </div>
        <div className="navlink">🛒 Cart</div>
      </header>
      <nav className="subnav">
        <a>All</a>
        <a>Today's Deals</a>
        <a>Customer Service</a>
        <a>Registry</a>
        <a>Gift Cards</a>
        <a>Sell</a>
      </nav>
    </>
  );
}
