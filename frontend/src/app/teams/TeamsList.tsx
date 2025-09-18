"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import styles from "./teams.module.css";
import PageWrapper from "../components/PageWrapper";

export interface Team {
  team_id: number;
  team_name: string;
  wins: number;
  losses: number;
  final_standing: number;
  roster: string[];
}

interface Props {
  initialTeams?: Team[];
}

export default function TeamsList({ initialTeams }: Props) {
  const [teams, setTeams] = useState<Team[]>(initialTeams || []);
  const [loading, setLoading] = useState(!initialTeams?.length);

  useEffect(() => {
    // If we have cached teams, use them
    const cached = sessionStorage.getItem("teams");
    if (cached) {
      try {
        const parsed = JSON.parse(cached);
        if (Array.isArray(parsed)) {
          setTeams(parsed);
          setLoading(false);
          return;
        }
      } catch {
        sessionStorage.removeItem("teams");
      }
    }

    if (teams.length) return; // Already have initial teams

    async function fetchTeams() {
      try {
        const res = await fetch("/api/teams"); // Proxy route
        const data = await res.json();

        if (Array.isArray(data)) {
          setTeams(data);
          sessionStorage.setItem("teams", JSON.stringify(data));
        } else {
          console.error("Unexpected data format:", data);
        }
      } catch (err) {
        console.error("Error fetching teams:", err);
      } finally {
        setLoading(false);
      }
    }

    fetchTeams();
  }, []);

  if (loading) return <PageWrapper>Loading teams...</PageWrapper>;
  if (!teams.length) return <PageWrapper>No teams found</PageWrapper>;

  return (
    <PageWrapper>
      <div className={styles.container}>
        <h1 className={styles.title}>Teams</h1>
        <ul className={styles.teamList}>
          {teams.map((team) => (
            <li key={team.team_id} className={styles.teamCard}>
              <h2>{team.team_name}</h2>
              <p>Wins: {team.wins} | Losses: {team.losses}</p>
              <Link href={`/teams/${team.team_id}`}>View Roster</Link>
            </li>
          ))}
        </ul>
      </div>
    </PageWrapper>
  );
}

