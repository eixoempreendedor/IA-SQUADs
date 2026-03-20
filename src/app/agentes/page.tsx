"use client";

import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import { agents, activeAgents, inactiveAgentsList, squadNames } from "@/data/agents";

export default function AgentesPage() {
  const [filter, setFilter] = useState("Todos");
  const [search, setSearch] = useState("");

  const filtered = (filter === "Inativos" ? inactiveAgentsList : activeAgents)
    .filter(a => filter === "Todos" || filter === "Inativos" || a.squadName === filter)
    .filter(a => {
      if (!search) return true;
      const q = search.toLowerCase();
      return a.name.toLowerCase().includes(q) || a.title.toLowerCase().includes(q);
    });

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="ml-56 flex-1 p-8">
        <div className="max-w-6xl">
          <h1 className="text-2xl font-bold mb-1">Catálogo de Agentes</h1>
          <p className="mb-6" style={{ color: "var(--text-secondary)" }}>
            {activeAgents.length} agentes ativos em {squadNames.length} squads
          </p>

          {/* Search */}
          <input
            type="text"
            placeholder="Buscar agente por nome ou especialidade..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full rounded-lg border px-4 py-2.5 text-sm mb-4 outline-none focus:border-orange-500/50"
            style={{ background: "var(--bg-card)", borderColor: "var(--border-card)", color: "var(--text-primary)" }}
          />

          {/* Filters */}
          <div className="flex flex-wrap gap-2 mb-6">
            {["Todos", ...squadNames, "Inativos"].map((s) => (
              <button
                key={s}
                onClick={() => setFilter(s)}
                className={`text-xs px-3 py-1.5 rounded-full border transition-colors ${
                  filter === s
                    ? "bg-orange-500/20 border-orange-500/50 text-orange-400"
                    : "hover:bg-white/5"
                }`}
                style={filter !== s ? { borderColor: "var(--border-card)", color: "var(--text-muted)" } : undefined}
              >
                {s}
              </button>
            ))}
          </div>

          {/* Count */}
          <p className="text-xs mb-4" style={{ color: "var(--text-muted)" }}>
            {filtered.length} agente{filtered.length !== 1 ? "s" : ""}
          </p>

          {/* Agent Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
            {filtered.map((agent) => (
              <a
                key={`${agent.squadId}-${agent.id}`}
                href={`/IA-Squads/agentes/${agent.squadId}/${agent.id}`}
                className={`rounded-lg border p-4 flex items-start gap-3 transition-all hover:shadow-md hover:shadow-black/10 hover:border-orange-500/30 cursor-pointer ${agent.inactive ? "opacity-50" : ""}`}
                style={{ background: "var(--bg-card)", borderColor: "var(--border-card)" }}
              >
                <span className="text-2xl flex-shrink-0 mt-0.5">{agent.icon}</span>
                <div className="min-w-0">
                  <div className="font-medium text-sm">{agent.name}</div>
                  <div className="text-xs mt-0.5 line-clamp-1" style={{ color: "var(--text-secondary)" }}>
                    {agent.title}
                  </div>
                  <div className="text-[10px] mt-1.5 px-1.5 py-0.5 rounded inline-block"
                    style={{ background: "rgba(255,255,255,0.06)", color: "var(--text-muted)" }}>
                    {agent.squadName}
                  </div>
                </div>
              </a>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
