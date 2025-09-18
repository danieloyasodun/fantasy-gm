"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import styles from "./page.module.css";
import PageWrapper from "./components/PageWrapper";


export default function Home() {
  const [settings, setSettings] = useState<any>(null);

  useEffect(() => {
    // Check if cached data exists
    const cachedSettings = sessionStorage.getItem("settings");
    if (cachedSettings) {
      setSettings(JSON.parse(cachedSettings));
      return;
    }

    // Fetch if not cached
    async function fetchSettings() {
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
      const leagueId = process.env.NEXT_PUBLIC_LEAGUE_ID;
      const res = await fetch(`${backendUrl}/api/league/${leagueId}/settings`);
      const data = await res.json();
      setSettings(data);
      sessionStorage.setItem("settings", JSON.stringify(data)); // cache it
    }

    fetchSettings();
  }, []);

  if (!settings) return <div>Loading...</div>;

return (
    <PageWrapper>
      <div className={styles.container}>
        <h2>{settings.league_name}</h2>
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
    </PageWrapper>
  );
}

