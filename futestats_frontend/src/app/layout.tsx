import type { Metadata } from "next";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

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
    <html lang="pt-br">
      <body className="flex flex-col min-h-screen">
        <Header />
        <main className="grow px-10 py-14">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
