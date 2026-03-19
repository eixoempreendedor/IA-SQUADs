import Sidebar from "@/components/Sidebar";
import StatsBar from "@/components/StatsBar";
import SquadCard from "@/components/SquadCard";
import { squads, totals } from "@/data/squads";

export default function Home() {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="ml-56 flex-1 p-8">
        <div className="max-w-6xl">
          {/* Header */}
          <h1 className="text-2xl font-bold mb-1">Catálogo de Squads</h1>
          <p className="mb-6" style={{ color: "var(--text-secondary)" }}>
            Navegue e ative seus squads de agentes
          </p>

          {/* Summary line */}
          <p className="text-sm mb-6" style={{ color: "var(--text-muted)" }}>
            {totals.squads} squads disponíveis com {totals.agents} agentes, {totals.tasks} tarefas e {totals.workflows} workflows
          </p>

          {/* Stats */}
          <StatsBar />

          {/* Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
            {squads.map((squad) => (
              <SquadCard key={squad.id} squad={squad} />
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
