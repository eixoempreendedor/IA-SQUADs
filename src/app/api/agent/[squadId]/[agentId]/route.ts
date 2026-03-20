import { NextResponse } from "next/server";
import { readFile } from "fs/promises";
import path from "path";

const SQUADS_BASE = "C:\\Users\\luizf\\aios-core\\.aios-core\\squads";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ squadId: string; agentId: string }> }
) {
  const { squadId, agentId } = await params;

  // Sanitize to prevent path traversal
  const safeSquad = squadId.replace(/[^a-z0-9-]/gi, "");
  const safeAgent = agentId.replace(/[^a-z0-9-]/gi, "");

  const filePath = path.join(SQUADS_BASE, safeSquad, "agents", `${safeAgent}.md`);

  try {
    const content = await readFile(filePath, "utf-8");
    return NextResponse.json({ content });
  } catch {
    return NextResponse.json({ error: "Agent not found" }, { status: 404 });
  }
}
