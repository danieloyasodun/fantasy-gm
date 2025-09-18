import Link from "next/link";
import styles from "./NavBar.module.css";

export default function NavBar() {
  return (
    <nav className={styles.navbar}>
      <div className={styles.logo}>Fantasy AI GM</div>
      <ul className={styles.links}>
        <li><Link href="/">Home</Link></li>
        <li><Link href="/teams">Teams</Link></li>
        <li><Link href="/league">League</Link></li>
        <li><Link href="/draft">Draft</Link></li>
        <li><Link href="/free-agents">Free Agents</Link></li>
      </ul>
    </nav>
  );
}

