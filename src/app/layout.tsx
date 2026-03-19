import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "IA SQUADs — Seus squads de agentes IA",
  description: "Visualize e gerencie seus squads de agentes de IA",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className="antialiased">{children}</body>
    </html>
  );
}
