export const revalidate = 0;
import Link from "next/link"
import styles from "./page.module.css";

export default async function Home() {
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
  const leagueId = process.env.NEXT_PUBLIC_LEAGUE_ID;

  const leagueRes = await fetch(`${backendUrl}/api/league/${leagueId}`, { cache: "no-store" });
  const leagueData = await leagueRes.json();

  const settingsRes = await fetch (`${backendUrl}/api/league/${leagueId}/settings`, {cache: "no-store"})
  const settings = await settingsRes.json()

  return (
    <div className={styles.container}>
      {settings && (
        <div>
          <h2>{settings.league_name}</h2>
        </div>
      )}
      
      <h1 className={styles.title}>Welcome to Fantasy AI Assistant GM</h1>
      <p className={styles.subtitle}>
        Manage your team, analyze stats, and dominate your fantasy league with AI-powered insights.
      </p>

      <div className={styles.grid}>
        <Link href="/teams" className={styles.card}>Manage My Team</Link>
        <Link href="/league" className={styles.card}>View League Stats</Link>
        <Link href="/draft" className={styles.card}>Draft Room</Link>
        <Link href="/settings" className={styles.card}>Settings</Link>
      </div>

    </div>
  );
}
