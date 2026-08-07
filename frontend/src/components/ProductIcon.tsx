"use client";

type IconType = "electronics" | "home" | "fashion" | "books" | "toys" | "beauty" | "generic";

const PALETTE: Record<IconType, [string, string]> = {
  electronics: ["#146EB4", "#2E86C1"],
  home: ["#B12704", "#E67E22"],
  fashion: ["#7D3C98", "#A569BD"],
  books: ["#1E8449", "#28B463"],
  toys: ["#CA6F1E", "#F0B27A"],
  beauty: ["#C2185B", "#EC407A"],
  generic: ["#37475A", "#5D7290"],
};

export default function ProductIcon({ type = "generic" }: { type?: IconType }) {
  const [c1, c2] = PALETTE[type];
  const shapes: Record<IconType, JSX.Element> = {
    electronics: (
      <g>
        <rect x="30" y="20" width="60" height="42" rx="4" fill={c1} />
        <rect x="38" y="28" width="44" height="26" rx="2" fill="white" opacity="0.85" />
        <rect x="50" y="66" width="20" height="6" rx="2" fill={c2} />
        <circle cx="60" cy="41" r="3" fill={c1} />
      </g>
    ),
    home: (
      <g>
        <path d="M35 45 Q35 30 60 30 Q85 30 85 45 L85 70 L35 70 Z" fill={c1} />
        <rect x="45" y="50" width="30" height="20" rx="2" fill="white" opacity="0.85" />
        <circle cx="60" cy="22" r="6" fill={c2} />
      </g>
    ),
    fashion: (
      <g>
        <path d="M45 25 L60 35 L75 25 L88 35 L80 48 L75 44 L75 80 L45 80 L45 44 L40 48 L32 35 Z" fill={c1} />
        <circle cx="60" cy="30" r="4" fill="white" opacity="0.85" />
      </g>
    ),
    books: (
      <g>
        <rect x="32" y="28" width="24" height="52" rx="2" fill={c1} />
        <rect x="58" y="24" width="24" height="56" rx="2" fill={c2} />
        <rect x="37" y="34" width="14" height="3" fill="white" opacity="0.8" />
        <rect x="63" y="32" width="14" height="3" fill="white" opacity="0.8" />
      </g>
    ),
    toys: (
      <g>
        <rect x="32" y="32" width="24" height="24" rx="3" fill={c1} />
        <circle cx="76" cy="44" r="14" fill={c2} />
        <rect x="40" y="60" width="40" height="16" rx="3" fill={c2} opacity="0.7" />
      </g>
    ),
    beauty: (
      <g>
        <rect x="52" y="24" width="16" height="14" rx="2" fill={c2} />
        <path d="M48 38 L72 38 L68 82 Q60 88 52 82 Z" fill={c1} />
        <rect x="54" y="48" width="12" height="6" fill="white" opacity="0.8" />
      </g>
    ),
    generic: (
      <g>
        <path d="M60 22 L92 38 L92 74 L60 90 L28 74 L28 38 Z" fill={c1} />
        <path d="M60 22 L92 38 L60 54 L28 38 Z" fill={c2} />
        <line x1="60" y1="54" x2="60" y2="90" stroke="white" strokeOpacity="0.3" strokeWidth="2" />
      </g>
    ),
  };

  return (
    <svg viewBox="0 0 120 100" className="product-icon" xmlns="http://www.w3.org/2000/svg">
      <rect x="0" y="0" width="120" height="100" rx="6" fill="#F7F8F8" />
      {shapes[type]}
    </svg>
  );
}
