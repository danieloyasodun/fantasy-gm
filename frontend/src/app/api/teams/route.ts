// src/app/api/teams/route.ts
import { NextResponse } from "next/server";

export async function GET() {
  try {
    const backendUrl = process.env.BACKEND_URL;
    const leagueId = process.env.LEAGUE_ID;

    if (!backendUrl || !leagueId) {
      throw new Error("BACKEND_URL or LEAGUE_ID is not defined");
    }

    const res = await fetch(`${backendUrl}/api/league/${leagueId}`);

    if (!res.ok) {
      return NextResponse.json({ error: "Failed to fetch teams" }, { status: res.status });
    }

    const data = await res.json();
    return NextResponse.json(data);
  } catch (err) {
    console.error("Error fetching teams in proxy:", err);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}

