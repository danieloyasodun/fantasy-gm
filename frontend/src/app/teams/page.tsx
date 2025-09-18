import Link from "next/link";
import styles from "./teams.module.css";

export const revalidate = 0; // Always fetch fresh data

interface Team {
  team_id: number;
  team_name: string;
  wins: number;
  losses: number;
  final_standing: number;
  roster: string[];
}

export default async function TeamsPage() {
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
  const leagueId = process.env.NEXT_PUBLIC_LEAGUE_ID;

  // Fetch all teams for this league
  const res = await fetch(`${backendUrl}/api/league/${leagueId}`, { cache: "no-store" });
  const teams: Team[] = await res.json();

  if (!Array.isArray(teams)) {
    console.error("Expected an array but got:", teams);
    return <div>Error fetching teams</div>;
  }

  return (
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
  );
}