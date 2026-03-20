"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import ReactMarkdown from "react-markdown";
import Sidebar from "@/components/Sidebar";
import { agents } from "@/data/agents";

export default function AgentDetailPage() {
  const params = useParams<{ squadId: string; agentId: string }>();
  const [content, setContent] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const agent = agents.find(
    (a) => a.id === params.agentId && a.squadId === params.squadId
  );

  useEffect(() => {
    fetch(`/IA-Squads/api/agent/${params.squadId}/${params.agentId}`)
      .then((r) => r.json())
      .then((data) => {
        setContent(data.content || data.error || "Conteúdo não encontrado");
        setLoading(false);
      })
      .catch(() => {
        setContent("Erro ao carregar agente");
        setLoading(false);
      });
  }, [params.squadId, params.agentId]);

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="ml-56 flex-1 p-8">
        <div className="max-w-4xl">
          {/* Back button */}
          <a
            href="/IA-Squads/agentes"
            className="inline-flex items-center gap-2 text-sm mb-6 hover:text-orange-400 transition-colors"
            style={{ color: "var(--text-muted)" }}
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
            Voltar para Agentes
          </a>

          {/* Header */}
          {agent && (
            <div className="flex items-start gap-4 mb-8">
              <span className="text-5xl">{agent.icon}</span>
              <div>
                <h1 className="text-2xl font-bold">{agent.name}</h1>
                <p className="text-sm mt-1" style={{ color: "var(--text-secondary)" }}>
                  {agent.title}
                </p>
                <span
                  className="inline-block text-xs mt-2 px-2 py-0.5 rounded"
                  style={{ background: "rgba(255,255,255,0.06)", color: "var(--text-muted)" }}
                >
                  {agent.squadName}
                </span>
              </div>
            </div>
          )}

          {/* Content */}
          {loading ? (
            <div className="flex items-center gap-3 py-12" style={{ color: "var(--text-muted)" }}>
              <div className="w-5 h-5 border-2 border-orange-500/30 border-t-orange-500 rounded-full animate-spin" />
              Carregando configuração do agente...
            </div>
          ) : (
            <div className="prose-agent rounded-xl border p-6 md:p-8"
              style={{ background: "var(--bg-card)", borderColor: "var(--border-card)" }}>
              <ReactMarkdown>{content || ""}</ReactMarkdown>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
