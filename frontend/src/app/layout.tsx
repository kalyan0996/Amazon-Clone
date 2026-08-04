import type { ReactNode } from "react";

export const metadata = {
  title: "Amazon Clone",
  description: "Storefront for the amazon-clone platform",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
