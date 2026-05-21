import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Agentic OS — AI Content Admin Dashboard",
  description: "Trung tâm điều khiển hệ thống AI Content. Quản trị Agents (Dify), tự động hoá (n8n), render video (Remotion) và giám sát hệ thống trong một giao diện duy nhất.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
