"use client";

export default function Footer() {
  return (
    <footer className="site-footer">
      <button
        className="back-to-top"
        onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
      >
        Back to top
      </button>
      <div className="footer-columns">
        <div className="footer-col">
          <h4>Get to Know Us</h4>
          <a>About Us</a>
          <a>Careers</a>
          <a>Press Releases</a>
        </div>
        <div className="footer-col">
          <h4>Make Money with Us</h4>
          <a>Sell products</a>
          <a>Become an Affiliate</a>
          <a>Advertise Your Products</a>
        </div>
        <div className="footer-col">
          <h4>Payment Products</h4>
          <a>Business Card</a>
          <a>Shop with Points</a>
          <a>Reload Your Balance</a>
        </div>
        <div className="footer-col">
          <h4>Let Us Help You</h4>
          <a>Your Account</a>
          <a>Your Orders</a>
          <a>Shipping Rates &amp; Policies</a>
          <a>Returns &amp; Replacements</a>
        </div>
      </div>
      <div className="footer-bottom">
        <div className="logo">amazon</div>
        <p>© {new Date().getFullYear()} Amazon Clone. Not affiliated with Amazon.com, Inc.</p>
      </div>
    </footer>
  );
}
