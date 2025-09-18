interface Team {
  team_id: number;
  team_name: string;
  wins: number;
  losses: number;
  final_standing: number;
  roster: string[];
}

interface PageProps {
  params: { team_id: string };
}

export default async function TeamPage(props: PageProps) {
  const { team_id } = await props.params;
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
  const leagueId = process.env.NEXT_PUBLIC_LEAGUE_ID;

  try {
    const res = await fetch(`${backendUrl}/api/league/${leagueId}/team/${team_id}`, { cache: "no-store" });

    if (!res.ok) {
      console.error("Failed to fetch team:", await res.text());
      return <div>Team not found</div>;
    }

    const team: Team = await res.json();

    return (
      <div>
        <h1>{team.team_name}</h1>
        <p>Wins: {team.wins} | Losses: {team.losses}</p>
        <h2>Roster</h2>
        <ul>
          {team.roster?.map((player, i) => (
            <li key={i}>{player}</li>
          ))}
        </ul>
      </div>
    );
  } catch (err) {
    console.error("Error fetching team:", err);
    return <div>Error loading team</div>;
  }
}

