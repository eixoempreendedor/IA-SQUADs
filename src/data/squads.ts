export interface Squad {
  id: string;
  name: string;
  description: string;
  version: string;
  agents: number;
  tasks: number;
  workflows: number;
  tags: string[];
  color: string;
}

export const squads: Squad[] = [
  {
    id: "advisory-board",
    name: "Advisory Board",
    description: "Board de 11 conselheiros estratégicos — Ray Dalio, Charlie Munger, Naval Ravikant, Peter Thiel, Reid Hoffman, Simon Sinek, Brené Brown, e mais.",
    version: "v1.0.0",
    agents: 11,
    tasks: 7,
    workflows: 2,
    tags: ["strategy", "investment", "leadership", "mental-models", "scaling", "purpose", "entrepreneurship"],
    color: "#f59e0b",
  },
  {
    id: "brand-squad",
    name: "Brand Squad",
    description: "O squad definitivo de estratégia de marca — 10 pensadores lendários de branding clonados como agentes de IA, mais 4 especialistas funcionais e 1 orquestrador.",
    version: "v1.0.0",
    agents: 15,
    tasks: 9,
    workflows: 2,
    tags: ["branding", "brand-strategy", "positioning", "identity", "naming", "archetype", "storybrand", "brand-equity", "brand-architecture", "luxury"],
    color: "#ef4444",
  },
  {
    id: "c-level-squad",
    name: "C-Level Squad",
    description: "C-suite virtual de 6 executivos — CEO (Vision Chief), COO, CMO, CTO, CIO, CAIO. Estratégia, operações, marketing, tecnologia, AI.",
    version: "v1.0.0",
    agents: 6,
    tasks: 7,
    workflows: 2,
    tags: ["c-suite", "strategy", "operations", "marketing", "technology", "ai", "leadership"],
    color: "#a855f7",
  },
  {
    id: "claude-code-mastery",
    name: "Claude Code Mastery",
    description: "Squad especialista em todas as dimensões do Claude Code: hooks, skills, subagents, MCP, plugins, agent teams, customização, integração e roadmap tracking.",
    version: "v1.0.0",
    agents: 8,
    tasks: 0,
    workflows: 0,
    tags: ["claude-code", "hooks", "skills", "subagents", "mcp", "plugins", "agent-teams", "customization", "integration", "context-engineering"],
    color: "#3b82f6",
  },
  {
    id: "copy-squad",
    name: "Copy Squad",
    description: "Squad de elite com 23 agentes de copywriting — 22 copywriters lendários + 1 orquestrador. Cobre direct response, email, funis, VSLs, cartas de vendas.",
    version: "v1.0.0",
    agents: 23,
    tasks: 12,
    workflows: 2,
    tags: ["copywriting", "direct-response", "sales-letter", "email", "vsl", "funnel", "headline", "offer", "ad-copy", "launch", "brand-copy"],
    color: "#f97316",
  },
  {
    id: "cybersecurity",
    name: "Cybersecurity Squad",
    description: "Squad de 15 agentes de cibersegurança. Pentest, red team, blue team, AppSec, incident response, recon, exploitation — tudo com framework ético.",
    version: "v1.0.0",
    agents: 15,
    tasks: 9,
    workflows: 2,
    tags: ["pentesting", "red-team", "blue-team", "appsec", "network-security", "vulnerability", "incident-response"],
    color: "#10b981",
  },
  {
    id: "data-squad",
    name: "Data Squad",
    description: "Squad de 7 estrategistas data-driven — analytics (Kaushik), CLV (Fader), growth (Ellis), community (Spinks), customer success (Mehta), audience (Kao).",
    version: "v1.0.0",
    agents: 7,
    tasks: 7,
    workflows: 2,
    tags: ["analytics", "growth", "customer-success", "community", "clv", "metrics", "retention"],
    color: "#8b5cf6",
  },
  {
    id: "design-squad",
    name: "Design Squad",
    description: "Squad de design operations — 3 experts (Brad Frost, Dan Mall, Dave Malouf) + 4 especialistas + 1 orquestrador. Design systems, UX, UI, visual.",
    version: "v1.0.0",
    agents: 8,
    tasks: 8,
    workflows: 2,
    tags: ["design-systems", "ux", "ui", "atomic-design", "components", "design-ops", "visual-design"],
    color: "#06b6d4",
  },
  {
    id: "hormozi-squad",
    name: "Hormozi Squad",
    description: "Squad de 16 agentes implementando os frameworks de Alex Hormozi. Offers, leads, pricing, sales, content, hooks, launch, retention, scaling.",
    version: "v1.0.0",
    agents: 16,
    tasks: 10,
    workflows: 2,
    tags: ["hormozi", "offers", "leads", "pricing", "sales", "scaling", "content", "hooks", "business"],
    color: "#eab308",
  },
  {
    id: "movement",
    name: "Movement Squad",
    description: "Squad de 7 agentes para construção de movimentos. Fenomenologia, identidade, manifestos, ciclos de crescimento, medição de impacto.",
    version: "v1.0.0",
    agents: 7,
    tasks: 7,
    workflows: 1,
    tags: ["movement", "community", "social-impact", "identity", "manifesto", "growth-cycles", "phenomenology"],
    color: "#ec4899",
  },
  {
    id: "storytelling",
    name: "Storytelling Squad",
    description: "Squad de 12 mestres do storytelling. Mitologia, screenwriting, narrativa pessoal, business storytelling, improviso, pitching, movimentos sociais.",
    version: "v1.0.0",
    agents: 12,
    tasks: 8,
    workflows: 2,
    tags: ["storytelling", "narrative", "screenplay", "presentation", "pitch", "improv", "brand-story"],
    color: "#f43f5e",
  },
  {
    id: "traffic-masters",
    name: "Traffic Masters",
    description: "Squad de 16 agentes especialistas em tráfego pago. Facebook, YouTube, Google Ads, media buying, creative analysis, scaling, tracking.",
    version: "v1.0.0",
    agents: 16,
    tasks: 9,
    workflows: 2,
    tags: ["traffic", "ads", "facebook", "google", "youtube", "media-buying", "creative", "scaling", "tracking"],
    color: "#22c55e",
  },
];

export const inactiveSquads: Squad[] = [
  {
    id: "agentes-de-ferias",
    name: "Agentes de Férias",
    description: "Catálogo de agentes conselheiros temporariamente inativos. Pensadores brilhantes cujo expertise não se alinha diretamente com o negócio atual, mas que podem ser reativados.",
    version: "v1.0.0",
    agents: 5,
    tasks: 0,
    workflows: 0,
    tags: ["archive", "inactive", "venture-capital", "scaling", "activism", "vulnerability", "hedge-fund"],
    color: "#6b7280",
  },
];

export const allSquads = [...squads, ...inactiveSquads];

export const totals = {
  squads: squads.length,
  agents: squads.reduce((sum, s) => sum + s.agents, 0),
  tasks: squads.reduce((sum, s) => sum + s.tasks, 0),
  workflows: squads.reduce((sum, s) => sum + s.workflows, 0),
};
