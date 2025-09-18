import TeamsList, { Team } from "./TeamsList";
import PageWrapper from "../components/PageWrapper";

export default async function TeamsPage() {
  // Fetch via your own API route (proxy)
  const res = await fetch("http://localhost:3000/api/teams", { cache: "no-store" });
  const teams: Team[] = await res.json();

  return (
    <PageWrapper>
      <TeamsList initialTeams={teams} />
    </PageWrapper>
  );
}



