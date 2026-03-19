import type { Squad } from "@/data/squads";

const MAX_TAGS = 4;

export default function SquadCard({ squad }: { squad: Squad }) {
  const visibleTags = squad.tags.slice(0, MAX_TAGS);
  const remaining = squad.tags.length - MAX_TAGS;

  return (
    <div className="rounded-xl border overflow-hidden transition-shadow hover:shadow-lg hover:shadow-black/20 group"
      style={{ background: "var(--bg-card)", borderColor: "var(--border-card)" }}>
      {/* Color accent top border */}
      <div className="h-[3px]" style={{ background: squad.color }} />

      <div className="p-5">
        {/* Header */}
        <div className="flex items-start justify-between mb-3">
          <h3 className="font-semibold text-base">{squad.name}</h3>
          <span className="text-xs px-2 py-0.5 rounded-full border"
            style={{ color: "var(--text-muted)", borderColor: "var(--border-card)" }}>
            {squad.version}
          </span>
        </div>

        {/* Description */}
        <p className="text-sm leading-relaxed mb-4 line-clamp-2" style={{ color: "var(--text-secondary)" }}>
          {squad.description}
        </p>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-2 mb-4">
          {[
            { label: "AGENTES", value: squad.agents, color: squad.color },
            { label: "TAREFAS", value: squad.tasks, color: "#22c55e" },
            { label: "WORKFLOWS", value: squad.workflows, color: "#a855f7" },
          ].map((stat) => (
            <div key={stat.label} className="rounded-lg p-2.5 text-center"
              style={{ background: "var(--bg-stat)" }}>
              <div className="text-lg font-bold" style={{ color: stat.color }}>{stat.value}</div>
              <div className="text-[10px] tracking-wider" style={{ color: "var(--text-muted)" }}>{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-1.5">
          {visibleTags.map((tag) => (
            <span key={tag} className="text-xs px-2 py-1 rounded-md"
              style={{ background: "rgba(255,255,255,0.06)", color: "var(--text-muted)" }}>
              {tag}
            </span>
          ))}
          {remaining > 0 && (
            <span className="text-xs px-2 py-1 rounded-md"
              style={{ background: "rgba(255,255,255,0.06)", color: "var(--text-muted)" }}>
              +{remaining}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
