import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FuteStats BR",
  description: "Site de estatísticas e rankings do Futebol Brasileiro",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
