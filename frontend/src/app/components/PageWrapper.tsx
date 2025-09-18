// src/app/components/PageWrapper.tsx
"use client";

import { useState, useEffect } from "react";
import { usePathname } from "next/navigation";
import styles from "./PageWrapper.module.css";

export default function PageWrapper({ children }: { children: React.ReactNode }) {
  const [loading, setLoading] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    // Whenever pathname changes, show the loading screen briefly
    setLoading(true);
    const timeout = setTimeout(() => setLoading(false), 300); // 300ms minimum
    return () => clearTimeout(timeout);
  }, [pathname]);

  return (
    <>
      {loading && <div className={styles.loadingOverlay}>Loading...</div>}
      {children}
    </>
  );
}
