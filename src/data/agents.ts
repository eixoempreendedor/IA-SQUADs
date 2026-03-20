export interface Agent {
  id: string;
  name: string;
  icon: string;
  title: string;
  squadId: string;
  squadName: string;
  inactive?: boolean;
}

export const agents: Agent[] = [
  // advisory-board
  { id: "board-chair", name: "Board Chair", icon: "🏛️", title: "Advisory Board Orchestrator", squadId: "advisory-board", squadName: "Advisory Board" },
  { id: "charlie-munger", name: "Charlie Munger", icon: "🧠", title: "Mental Models & Rational Decision-Making", squadId: "advisory-board", squadName: "Advisory Board" },
  { id: "keith-cunningham", name: "Keith Cunningham", icon: "🎯", title: "Strategic Thinking & Business Mastery", squadId: "advisory-board", squadName: "Advisory Board" },
  { id: "naval-ravikant", name: "Naval Ravikant", icon: "🧘", title: "Wealth, Leverage & Happiness", squadId: "advisory-board", squadName: "Advisory Board" },
  { id: "dan-sullivan", name: "Dan Sullivan", icon: "🚀", title: "Who Not How & 10x Thinking", squadId: "advisory-board", squadName: "Advisory Board" },
  { id: "simon-sinek", name: "Simon Sinek", icon: "⭕", title: "Purpose-Driven Leadership", squadId: "advisory-board", squadName: "Advisory Board" },
  { id: "patrick-lencioni", name: "Patrick Lencioni", icon: "🏗️", title: "Organizational Health & Team Dynamics", squadId: "advisory-board", squadName: "Advisory Board" },
  { id: "marshall-goldsmith", name: "Marshall Goldsmith", icon: "🪞", title: "Behavioral Change in Leaders", squadId: "advisory-board", squadName: "Advisory Board" },
  { id: "bj-fogg", name: "BJ Fogg", icon: "🧬", title: "Tiny Habits & Behavior Design", squadId: "advisory-board", squadName: "Advisory Board" },
  { id: "gino-wickman", name: "Gino Wickman", icon: "⚙️", title: "EOS & Traction Architect", squadId: "advisory-board", squadName: "Advisory Board" },
  { id: "derek-sivers", name: "Derek Sivers", icon: "🎯", title: "Simplicity & Contrarian Entrepreneurship", squadId: "advisory-board", squadName: "Advisory Board" },

  // brand-squad
  { id: "brand-chief", name: "Brand Chief", icon: "🎨", title: "Brand Squad Orchestrator", squadId: "brand-squad", squadName: "Brand Squad" },
  { id: "david-aaker", name: "David Aaker", icon: "👑", title: "Brand Equity & Identity Pioneer", squadId: "brand-squad", squadName: "Brand Squad" },
  { id: "al-ries", name: "Al Ries", icon: "🏔️", title: "Positioning & Category Strategy", squadId: "brand-squad", squadName: "Brand Squad" },
  { id: "marty-neumeier", name: "Marty Neumeier", icon: "⚡", title: "Brand Gap & Radical Differentiation", squadId: "brand-squad", squadName: "Brand Squad" },
  { id: "donald-miller", name: "Donald Miller", icon: "📖", title: "StoryBrand Creator & SB7 Framework", squadId: "brand-squad", squadName: "Brand Squad" },
  { id: "alina-wheeler", name: "Alina Wheeler", icon: "✏️", title: "Brand Identity Authority", squadId: "brand-squad", squadName: "Brand Squad" },
  { id: "archetype-consultant", name: "Archetype Consultant", icon: "🎭", title: "Jungian Archetypes & Tone of Voice", squadId: "brand-squad", squadName: "Brand Squad" },
  { id: "naming-strategist", name: "Naming Strategist", icon: "💎", title: "Brand Naming & Name Architecture", squadId: "brand-squad", squadName: "Brand Squad" },
  { id: "domain-scout", name: "Domain Scout", icon: "🔎", title: "Domain & Handle Strategy", squadId: "brand-squad", squadName: "Brand Squad" },
  { id: "miller-sticky-brand", name: "Miller Sticky Brand", icon: "📋", title: "StoryBrand Implementation Engine", squadId: "brand-squad", squadName: "Brand Squad" },
  { id: "romano-brand", name: "Romano", icon: "✍️", title: "Copy, Sales & Predictable Business", squadId: "brand-squad", squadName: "Brand Squad" },

  // c-level-squad
  { id: "vision-chief", name: "Vision Chief", icon: "👔", title: "Strategic Vision & Executive Leadership", squadId: "c-level-squad", squadName: "C-Level Squad" },
  { id: "coo-orchestrator", name: "COO Orchestrator", icon: "⚙️", title: "Operational Excellence & Scaling", squadId: "c-level-squad", squadName: "C-Level Squad" },
  { id: "cmo-architect", name: "CMO Architect", icon: "📣", title: "Marketing Strategy & Brand Architecture", squadId: "c-level-squad", squadName: "C-Level Squad" },
  { id: "cto-architect", name: "CTO Architect", icon: "🔧", title: "Technology Strategy & Engineering", squadId: "c-level-squad", squadName: "C-Level Squad" },
  { id: "cio-engineer", name: "CIO Engineer", icon: "🖥️", title: "Information Systems & Digital Infrastructure", squadId: "c-level-squad", squadName: "C-Level Squad" },
  { id: "caio-architect", name: "CAIO Architect", icon: "🤖", title: "AI Strategy & Intelligent Systems", squadId: "c-level-squad", squadName: "C-Level Squad" },

  // claude-code-mastery
  { id: "claude-mastery-chief", name: "Orion", icon: "🧠", title: "Claude Code Mastery Orchestrator", squadId: "claude-code-mastery", squadName: "Claude Code Mastery" },
  { id: "hooks-architect", name: "Latch", icon: "🎣", title: "Hooks Architect", squadId: "claude-code-mastery", squadName: "Claude Code Mastery" },
  { id: "skill-craftsman", name: "Anvil", icon: "✨", title: "Skill Craftsman", squadId: "claude-code-mastery", squadName: "Claude Code Mastery" },
  { id: "mcp-integrator", name: "Piper", icon: "🔌", title: "MCP Integration Architect", squadId: "claude-code-mastery", squadName: "Claude Code Mastery" },
  { id: "config-engineer", name: "Sigil", icon: "⚙️", title: "Configuration Engineer", squadId: "claude-code-mastery", squadName: "Claude Code Mastery" },
  { id: "project-integrator", name: "Conduit", icon: "🔧", title: "Project Integration Architect", squadId: "claude-code-mastery", squadName: "Claude Code Mastery" },
  { id: "swarm-orchestrator", name: "Nexus", icon: "🕸️", title: "Multi-Agent Architect", squadId: "claude-code-mastery", squadName: "Claude Code Mastery" },
  { id: "roadmap-sentinel", name: "Vigil", icon: "🧪", title: "Roadmap Sentinel & Strategist", squadId: "claude-code-mastery", squadName: "Claude Code Mastery" },

  // copy-squad
  { id: "copy-chief", name: "Cyrus", icon: "✍️", title: "Copy Chief — Squad Orchestrator", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "eugene-schwartz", name: "Eugene Schwartz", icon: "🧠", title: "Market Awareness & Strategic Copy", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "gary-halbert", name: "Gary Halbert", icon: "🔥", title: "Raw Emotional Storytelling", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "david-ogilvy", name: "David Ogilvy", icon: "🎩", title: "Father of Modern Advertising", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "gary-bencivenga", name: "Gary Bencivenga", icon: "👑", title: "World's Greatest Living Copywriter", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "claude-hopkins", name: "Claude Hopkins", icon: "🔬", title: "Father of Scientific Advertising", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "robert-collier", name: "Robert Collier", icon: "💌", title: "Empathy & the Mental Movie", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "joe-sugarman", name: "Joe Sugarman", icon: "🕶️", title: "Slippery Slide & Psychological Triggers", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "dan-kennedy", name: "Dan Kennedy", icon: "🎯", title: "No B.S. Direct Response", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "john-carlton", name: "John Carlton", icon: "🕵️", title: "The Sales Detective", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "clayton-makepeace", name: "Clayton Makepeace", icon: "💰", title: "Emotional Selling & Four-Legged Stool", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "david-deutsch", name: "David Deutsch", icon: "🧩", title: "Big Ideas & Fascination Master", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "parris-lampropoulos", name: "Parris Lampropoulos", icon: "🎯", title: "Master of Fascinations & Format", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "jim-rutz", name: "Jim Rutz", icon: "📰", title: "Magalog Pioneer & Anti-Bore Crusader", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "jon-benson", name: "Jon Benson", icon: "🎬", title: "VSL Inventor & Billion Dollar Copywriter", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "stefan-georgi", name: "Stefan Georgi", icon: "⚙️", title: "RMBC Architect — $700M in Copy", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "russell-brunson", name: "Russell Brunson", icon: "🔻", title: "Funnel Architect & Value Ladders", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "todd-brown", name: "Todd Brown", icon: "💡", title: "Big Ideas & Unique Mechanisms", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "frank-kern", name: "Frank Kern", icon: "🏄", title: "Intent-Based Branding Pioneer", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "andre-chaperon", name: "Andre Chaperon", icon: "✉️", title: "Email Storytelling & Soap Opera Sequence", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "ben-settle", name: "Ben Settle", icon: "📧", title: "Daily Emails & Personality-First Copy", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "ry-schwartz", name: "Ry Schwartz", icon: "🎭", title: "Belief Transformation & Launch Emails", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "dan-koe", name: "Dan Koe", icon: "🧘", title: "One-Person Business & Creator Economy", squadId: "copy-squad", squadName: "Copy Squad" },
  { id: "romano-copy", name: "Romano", icon: "✍️", title: "Copy, Sales & Predictable Business", squadId: "copy-squad", squadName: "Copy Squad" },

  // cybersecurity
  { id: "cyber-chief", name: "Cyber Chief", icon: "🛡️", title: "Cybersecurity Operations Orchestrator", squadId: "cybersecurity", squadName: "Cybersecurity Squad" },
  { id: "cartographer", name: "Cartographer", icon: "🗺️", title: "Reconnaissance & Attack Surface Mapping", squadId: "cybersecurity", squadName: "Cybersecurity Squad" },
  { id: "shannon-runner", name: "Shannon Runner", icon: "🔎", title: "OSINT Collection & Analysis", squadId: "cybersecurity", squadName: "Cybersecurity Squad" },
  { id: "busterer", name: "Busterer", icon: "🔍", title: "Web Content Discovery & Enumeration", squadId: "cybersecurity", squadName: "Cybersecurity Squad" },
  { id: "dirber", name: "Dirber", icon: "📂", title: "Network Service Enumeration", squadId: "cybersecurity", squadName: "Cybersecurity Squad" },
  { id: "fuzzer", name: "Fuzzer", icon: "🎯", title: "Input Fuzzing & Parameter Manipulation", squadId: "cybersecurity", squadName: "Cybersecurity Squad" },
  { id: "rogue", name: "Rogue", icon: "💀", title: "Exploitation & Post-Exploitation", squadId: "cybersecurity", squadName: "Cybersecurity Squad" },
  { id: "ripper", name: "Ripper", icon: "🔓", title: "Credential Cracking & Password Security", squadId: "cybersecurity", squadName: "Cybersecurity Squad" },
  { id: "command-generator", name: "Command Generator", icon: "⚡", title: "Security Tool Command Specialist", squadId: "cybersecurity", squadName: "Cybersecurity Squad" },
  { id: "peter-kim", name: "Peter Kim", icon: "🏈", title: "Red Team Operations & Pentesting", squadId: "cybersecurity", squadName: "Cybersecurity Squad" },
  { id: "georgia-weidman", name: "Georgia Weidman", icon: "📱", title: "Mobile Security & Exploit Development", squadId: "cybersecurity", squadName: "Cybersecurity Squad" },
  { id: "chris-sanders", name: "Chris Sanders", icon: "📡", title: "Network Security Monitoring", squadId: "cybersecurity", squadName: "Cybersecurity Squad" },
  { id: "jim-manico", name: "Jim Manico", icon: "🔒", title: "AppSec & Secure Coding Expert", squadId: "cybersecurity", squadName: "Cybersecurity Squad" },
  { id: "omar-santos", name: "Omar Santos", icon: "🎖️", title: "Vulnerability Management & Incident Response", squadId: "cybersecurity", squadName: "Cybersecurity Squad" },
  { id: "marcus-carey", name: "Marcus Carey", icon: "🎯", title: "Security Leadership & Threat Intelligence", squadId: "cybersecurity", squadName: "Cybersecurity Squad" },

  // data-squad
  { id: "data-chief", name: "Datum", icon: "📊", title: "Data-Driven Growth Orchestrator", squadId: "data-squad", squadName: "Data Squad" },
  { id: "avinash-kaushik", name: "Avinash Kaushik", icon: "🔍", title: "Web Analytics Authority", squadId: "data-squad", squadName: "Data Squad" },
  { id: "peter-fader", name: "Peter Fader", icon: "💎", title: "Customer Lifetime Value Authority", squadId: "data-squad", squadName: "Data Squad" },
  { id: "sean-ellis", name: "Sean Ellis", icon: "🚀", title: "Growth Hacking Pioneer", squadId: "data-squad", squadName: "Data Squad" },
  { id: "david-spinks", name: "David Spinks", icon: "🤝", title: "Community Strategy Pioneer", squadId: "data-squad", squadName: "Data Squad" },
  { id: "nick-mehta", name: "Nick Mehta", icon: "💚", title: "Customer Success Pioneer", squadId: "data-squad", squadName: "Data Squad" },
  { id: "wes-kao", name: "Wes Kao", icon: "🎓", title: "Audience Building Strategist", squadId: "data-squad", squadName: "Data Squad" },

  // design-squad
  { id: "design-chief", name: "Design Chief", icon: "🎨", title: "Design Operations Orchestrator", squadId: "design-squad", squadName: "Design Squad" },
  { id: "brad-frost", name: "Brad Frost", icon: "⚛️", title: "Atomic Design & Design Systems", squadId: "design-squad", squadName: "Design Squad" },
  { id: "dan-mall", name: "Dan Mall", icon: "🎯", title: "Design Systems at Scale", squadId: "design-squad", squadName: "Design Squad" },
  { id: "dave-malouf", name: "Dave Malouf", icon: "⚙️", title: "DesignOps Pioneer", squadId: "design-squad", squadName: "Design Squad" },
  { id: "design-system-architect", name: "Design System Architect", icon: "🧩", title: "Component Library & Design Tokens", squadId: "design-squad", squadName: "Design Squad" },
  { id: "ux-designer", name: "UX Designer", icon: "👤", title: "User Experience & Interaction Design", squadId: "design-squad", squadName: "Design Squad" },
  { id: "ui-engineer", name: "UI Engineer", icon: "💻", title: "Frontend UI Implementation", squadId: "design-squad", squadName: "Design Squad" },
  { id: "visual-generator", name: "Visual Generator", icon: "🖼️", title: "Visual Asset Creation & AI Prompts", squadId: "design-squad", squadName: "Design Squad" },

  // hormozi-squad
  { id: "hormozi-chief", name: "Hormozi Chief", icon: "🐝", title: "Hormozi Squad Orchestrator", squadId: "hormozi-squad", squadName: "Hormozi Squad" },
  { id: "hormozi-offers", name: "Hormozi Offers", icon: "🎰", title: "Grand Slam Offer Architect", squadId: "hormozi-squad", squadName: "Hormozi Squad" },
  { id: "hormozi-leads", name: "Hormozi Leads", icon: "🧲", title: "$100M Leads — Core 4 Lead Gen", squadId: "hormozi-squad", squadName: "Hormozi Squad" },
  { id: "hormozi-pricing", name: "Hormozi Pricing", icon: "💎", title: "Value-Based Pricing Strategist", squadId: "hormozi-squad", squadName: "Hormozi Squad" },
  { id: "hormozi-closer", name: "Hormozi Closer", icon: "🤝", title: "CLOSER Framework & Sales Process", squadId: "hormozi-squad", squadName: "Hormozi Squad" },
  { id: "hormozi-content", name: "Hormozi Content", icon: "📱", title: "Content Machine & Organic Strategy", squadId: "hormozi-squad", squadName: "Hormozi Squad" },
  { id: "hormozi-hooks", name: "Hormozi Hooks", icon: "🪝", title: "Hook Creation & Attention Capture", squadId: "hormozi-squad", squadName: "Hormozi Squad" },
  { id: "hormozi-copy", name: "Hormozi Copy", icon: "✍️", title: "Hormozi-Style Copywriting", squadId: "hormozi-squad", squadName: "Hormozi Squad" },
  { id: "hormozi-ads", name: "Hormozi Ads", icon: "📢", title: "Paid Advertising Strategy", squadId: "hormozi-squad", squadName: "Hormozi Squad" },
  { id: "hormozi-launch", name: "Hormozi Launch", icon: "🚀", title: "Launch Strategy & Market Entry", squadId: "hormozi-squad", squadName: "Hormozi Squad" },
  { id: "hormozi-retention", name: "Hormozi Retention", icon: "🔄", title: "Churn Reduction & LTV Max", squadId: "hormozi-squad", squadName: "Hormozi Squad" },
  { id: "hormozi-scale", name: "Hormozi Scale", icon: "📈", title: "Business Scaling & Systems", squadId: "hormozi-squad", squadName: "Hormozi Squad" },
  { id: "hormozi-models", name: "Hormozi Models", icon: "🏗️", title: "Business Model Design", squadId: "hormozi-squad", squadName: "Hormozi Squad" },
  { id: "hormozi-audit", name: "Hormozi Audit", icon: "🔍", title: "Business Evaluation & Diagnostics", squadId: "hormozi-squad", squadName: "Hormozi Squad" },
  { id: "hormozi-advisor", name: "Hormozi Advisor", icon: "🦁", title: "Strategic Business Advisor", squadId: "hormozi-squad", squadName: "Hormozi Squad" },
  { id: "hormozi-workshop", name: "Hormozi Workshop", icon: "🎓", title: "Workshop Design & Delivery", squadId: "hormozi-squad", squadName: "Hormozi Squad" },

  // movement
  { id: "movement-chief", name: "Movement Chief", icon: "✊", title: "Movement Building Orchestrator", squadId: "movement", squadName: "Movement Squad" },
  { id: "movement-architect", name: "Movement Architect", icon: "🏗️", title: "Movement Architecture & Community Design", squadId: "movement", squadName: "Movement Squad" },
  { id: "fenomenologo", name: "Fenomenólogo", icon: "🔮", title: "Phenomenological Analysis", squadId: "movement", squadName: "Movement Squad" },
  { id: "identitario", name: "Identitário", icon: "🛡️", title: "Identity Architecture & Tribal Formation", squadId: "movement", squadName: "Movement Squad" },
  { id: "manifestador", name: "Manifestador", icon: "📜", title: "Manifesto Creation & Narrative", squadId: "movement", squadName: "Movement Squad" },
  { id: "estrategista-de-ciclo", name: "Estrategista de Ciclo", icon: "🔄", title: "Growth Cycle Strategy", squadId: "movement", squadName: "Movement Squad" },
  { id: "analista-de-impacto", name: "Analista de Impacto", icon: "📊", title: "Impact Measurement & Movement Health", squadId: "movement", squadName: "Movement Squad" },

  // storytelling
  { id: "story-chief", name: "Story Chief", icon: "📖", title: "Storytelling Squad Orchestrator", squadId: "storytelling", squadName: "Storytelling Squad" },
  { id: "joseph-campbell", name: "Joseph Campbell", icon: "🏛️", title: "Hero's Journey & Comparative Mythology", squadId: "storytelling", squadName: "Storytelling Squad" },
  { id: "blake-snyder", name: "Blake Snyder", icon: "🎬", title: "Save the Cat Beat Sheet", squadId: "storytelling", squadName: "Storytelling Squad" },
  { id: "dan-harmon", name: "Dan Harmon", icon: "🔄", title: "Story Circle & TV Writing", squadId: "storytelling", squadName: "Storytelling Squad" },
  { id: "shawn-coyne", name: "Shawn Coyne", icon: "📊", title: "Story Grid & Editorial Diagnostics", squadId: "storytelling", squadName: "Storytelling Squad" },
  { id: "nancy-duarte", name: "Nancy Duarte", icon: "📊", title: "Presentation Storytelling & Sparkline", squadId: "storytelling", squadName: "Storytelling Squad" },
  { id: "oren-klaff", name: "Oren Klaff", icon: "🎲", title: "Pitch Anything & Frame Control", squadId: "storytelling", squadName: "Storytelling Squad" },
  { id: "kindra-hall", name: "Kindra Hall", icon: "💎", title: "Business Storytelling & 4 Stories", squadId: "storytelling", squadName: "Storytelling Squad" },
  { id: "matthew-dicks", name: "Matthew Dicks", icon: "🎤", title: "Personal Storytelling & Moth Champion", squadId: "storytelling", squadName: "Storytelling Squad" },
  { id: "keith-johnstone", name: "Keith Johnstone", icon: "🎭", title: "Impro, Status & Spontaneity", squadId: "storytelling", squadName: "Storytelling Squad" },
  { id: "marshall-ganz", name: "Marshall Ganz", icon: "✊", title: "Public Narrative & Movement Storytelling", squadId: "storytelling", squadName: "Storytelling Squad" },
  { id: "park-howell", name: "Park Howell", icon: "🎯", title: "ABT & Business Storytelling", squadId: "storytelling", squadName: "Storytelling Squad" },

  // traffic-masters
  { id: "traffic-chief", name: "Traffic Chief", icon: "🎯", title: "Traffic Masters Orchestrator", squadId: "traffic-masters", squadName: "Traffic Masters" },
  { id: "depesh-mandalia", name: "Depesh Mandalia", icon: "📐", title: "BPM Method & Facebook Scaling", squadId: "traffic-masters", squadName: "Traffic Masters" },
  { id: "molly-pittman", name: "Molly Pittman", icon: "👑", title: "Facebook Ads & Traffic Systems", squadId: "traffic-masters", squadName: "Traffic Masters" },
  { id: "nicholas-kusmich", name: "Nicholas Kusmich", icon: "🎯", title: "High-ROI Facebook Strategist", squadId: "traffic-masters", squadName: "Traffic Masters" },
  { id: "pedro-sobral", name: "Pedro Sobral", icon: "🥷", title: "O Ninja Supremo do Tráfego", squadId: "traffic-masters", squadName: "Traffic Masters" },
  { id: "kasim-aslam", name: "Kasim Aslam", icon: "🔍", title: "Google Ads Authority", squadId: "traffic-masters", squadName: "Traffic Masters" },
  { id: "tom-breeze", name: "Tom Breeze", icon: "🎬", title: "YouTube Ads & ADUCATE Formula", squadId: "traffic-masters", squadName: "Traffic Masters" },
  { id: "ralph-burns", name: "Ralph Burns", icon: "🎙️", title: "Performance Marketing Pioneer", squadId: "traffic-masters", squadName: "Traffic Masters" },
  { id: "media-buyer", name: "Media Buyer", icon: "🖥️", title: "Cross-Platform Media Buying", squadId: "traffic-masters", squadName: "Traffic Masters" },
  { id: "ad-midas", name: "Ad Midas", icon: "✨", title: "Ad Creative Strategy", squadId: "traffic-masters", squadName: "Traffic Masters" },
  { id: "creative-analyst", name: "Creative Analyst", icon: "🔬", title: "Ad Creative Performance Analysis", squadId: "traffic-masters", squadName: "Traffic Masters" },
  { id: "ads-analyst", name: "Ads Analyst", icon: "🔎", title: "Ad Account Audit & Optimization", squadId: "traffic-masters", squadName: "Traffic Masters" },
  { id: "performance-analyst", name: "Performance Analyst", icon: "📊", title: "Campaign Data & Reporting", squadId: "traffic-masters", squadName: "Traffic Masters" },
  { id: "pixel-specialist", name: "Pixel Specialist", icon: "🔌", title: "Tracking, Pixels & Attribution", squadId: "traffic-masters", squadName: "Traffic Masters" },
  { id: "scale-optimizer", name: "Scale Optimizer", icon: "🚀", title: "Campaign Scaling & Efficiency", squadId: "traffic-masters", squadName: "Traffic Masters" },
  { id: "fiscal", name: "Fiscal", icon: "💰", title: "Ad Budget & Financial Management", squadId: "traffic-masters", squadName: "Traffic Masters" },

  // agentes-de-ferias (inactive)
  { id: "peter-thiel", name: "Peter Thiel", icon: "♟️", title: "Monopoly, Secrets & Zero-to-One", squadId: "agentes-de-ferias", squadName: "Agentes de Férias", inactive: true },
  { id: "reid-hoffman", name: "Reid Hoffman", icon: "🔗", title: "Networks & Blitzscaling", squadId: "agentes-de-ferias", squadName: "Agentes de Férias", inactive: true },
  { id: "ray-dalio", name: "Ray Dalio", icon: "📐", title: "Principles & Systematic Decision-Making", squadId: "agentes-de-ferias", squadName: "Agentes de Férias", inactive: true },
  { id: "yvon-chouinard", name: "Yvon Chouinard", icon: "🏔️", title: "Purpose, Planet & Anti-Growth", squadId: "agentes-de-ferias", squadName: "Agentes de Férias", inactive: true },
  { id: "brene-brown", name: "Brené Brown", icon: "💛", title: "Vulnerability, Courage & Empathic Leadership", squadId: "agentes-de-ferias", squadName: "Agentes de Férias", inactive: true },
  { id: "byron-sharp", name: "Byron Sharp", icon: "🔬", title: "Evidence-Based Brand Growth", squadId: "agentes-de-ferias", squadName: "Agentes de Férias", inactive: true },
  { id: "denise-yohn", name: "Denise Lee Yohn", icon: "🔗", title: "Brand-Culture Fusion Expert", squadId: "agentes-de-ferias", squadName: "Agentes de Férias", inactive: true },
  { id: "emily-heyward", name: "Emily Heyward", icon: "🚀", title: "Startup Brand Architect", squadId: "agentes-de-ferias", squadName: "Agentes de Férias", inactive: true },
  { id: "jean-noel-kapferer", name: "Jean-Noël Kapferer", icon: "💠", title: "Brand Identity Prism & Luxury Management", squadId: "agentes-de-ferias", squadName: "Agentes de Férias", inactive: true },
  { id: "kevin-keller", name: "Kevin Lane Keller", icon: "📐", title: "CBBE Pyramid & Brand Equity", squadId: "agentes-de-ferias", squadName: "Agentes de Férias", inactive: true },
];

export const activeAgents = agents.filter(a => !a.inactive);
export const inactiveAgentsList = agents.filter(a => a.inactive);
export const squadNames = [...new Set(agents.filter(a => !a.inactive).map(a => a.squadName))];
