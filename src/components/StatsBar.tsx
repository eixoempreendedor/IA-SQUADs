import { totals } from "@/data/squads";

const stats = [
  { label: "Squads", value: totals.squads, color: "#f59e0b" },
  { label: "Agentes", value: totals.agents, color: "#22c55e" },
  { label: "Tarefas", value: totals.tasks, color: "#a855f7" },
  { label: "Workflows", value: totals.workflows, color: "#eab308" },
];

export default function StatsBar() {
  return (
    <div className="grid grid-cols-4 gap-4 mb-8">
      {stats.map((s) => (
        <div key={s.label} className="rounded-xl border p-5 text-center"
          style={{ background: "var(--bg-card)", borderColor: "var(--border-card)" }}>
          <div className="text-3xl font-bold mb-1" style={{ color: s.color }}>{s.value}</div>
          <div className="text-sm" style={{ color: "var(--text-secondary)" }}>{s.label}</div>
        </div>
      ))}
    </div>
  );
}
