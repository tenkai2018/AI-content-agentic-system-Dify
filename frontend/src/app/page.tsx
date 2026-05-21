"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Bot, Zap, Film, Activity, Server, User } from "lucide-react";
import styles from "./page.module.css";

const TABS = [
  {
    id: "dify",
    label: "AI Studio",
    sublabel: "Dify Agents",
    icon: Bot,
    envKey: "NEXT_PUBLIC_DIFY_APP_URL",
    defaultUrl: "http://localhost",
  },
  {
    id: "n8n",
    label: "Automations",
    sublabel: "n8n Flows",
    icon: Zap,
    envKey: "NEXT_PUBLIC_N8N_URL",
    defaultUrl: "http://localhost:5678",
  },
  {
    id: "remotion",
    label: "Video Render",
    sublabel: "Remotion Studio",
    icon: Film,
    envKey: "NEXT_PUBLIC_REMOTION_URL",
    defaultUrl: "http://localhost:3001",
  },
  {
    id: "logs",
    label: "Monitoring",
    sublabel: "System Logs",
    icon: Activity,
    envKey: null,
    defaultUrl: null,
  },
];

type Log = {
  id: number;
  level: "INFO" | "WARNING" | "ERROR";
  source: string;
  message: string;
  created_at: string;
};

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState("dify");
  const [logs, setLogs] = useState<Log[]>([]);
  const [isBackendOnline, setIsBackendOnline] = useState(false);

  const fetchLogs = async () => {
    try {
      const apiUrl =
        process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";
      const res = await fetch(`${apiUrl}/api/logs?limit=50`, {
        cache: "no-store",
      });
      if (res.ok) {
        const data = await res.json();
        setLogs(data);
        setIsBackendOnline(true);
      } else {
        setIsBackendOnline(false);
      }
    } catch {
      setIsBackendOnline(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  useEffect(() => {
    if (activeTab === "logs") {
      fetchLogs();
      const interval = setInterval(fetchLogs, 5000);
      return () => clearInterval(interval);
    }
  }, [activeTab]);

  const activeTabData = TABS.find((t) => t.id === activeTab)!;

  return (
    <div className={styles.dashboardContainer}>
      {/* ─────────── SIDEBAR ─────────── */}
      <aside className={styles.sidebar}>
        {/* Logo */}
        <div className={styles.sidebarHeader}>
          <div className={styles.logoMark}>
            <div className={styles.logoDot} />
            <span className={styles.logo}>Agentic OS</span>
          </div>
          <p className={styles.sidebarSubtitle}>AI Content System</p>
        </div>

        {/* Navigation */}
        <nav className={styles.navSection}>
          <p className={styles.navSectionLabel}>Navigation</p>
          {TABS.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <div
                key={tab.id}
                className={`${styles.navItem} ${isActive ? styles.navItemActive : ""}`}
                onClick={() => setActiveTab(tab.id)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => e.key === "Enter" && setActiveTab(tab.id)}
              >
                {isActive && <span className={styles.navActiveBar} />}
                <Icon className={styles.navIcon} size={18} />
                <span>{tab.label}</span>
              </div>
            );
          })}
        </nav>

        {/* Footer */}
        <div className={styles.sidebarFooter}>
          <p className={styles.sidebarFooterText}>
            v1.0 · Powered by Dify + n8n
          </p>
        </div>
      </aside>

      {/* ─────────── MAIN ─────────── */}
      <main className={styles.mainContent}>
        {/* Top Bar */}
        <header className={styles.topBar}>
          <div>
            <h1 className={styles.pageTitle}>{activeTabData.label}</h1>
          </div>

          <div className={styles.topBarRight}>
            {/* Backend Status */}
            <div className={styles.statusBadge}>
              <Server size={14} />
              <span>API</span>
              <span
                className={`${styles.statusDot} ${
                  isBackendOnline
                    ? styles.statusDotOnline
                    : styles.statusDotOffline
                }`}
              />
            </div>

            {/* User */}
            <div className={styles.statusBadge}>
              <User size={14} />
              <span>Admin</span>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <div className={styles.contentArea}>
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.25, ease: "easeOut" }}
              style={{
                display: "flex",
                flexDirection: "column",
                flex: 1,
                height: "100%",
              }}
            >
              {/* ── Iframe tabs (Dify / n8n / Remotion) ── */}
              {activeTabData.defaultUrl && (
                <div className={styles.iframeWrapper}>
                  <iframe
                    className={styles.iframe}
                    src={activeTabData.defaultUrl}
                    title={activeTabData.sublabel}
                  />
                </div>
              )}

              {/* ── Logs Tab ── */}
              {activeTab === "logs" && (
                <div className={styles.logsWrapper}>
                  <table className={styles.logTable}>
                    <thead>
                      <tr>
                        <th>Timestamp</th>
                        <th>Level</th>
                        <th>Source</th>
                        <th>Message</th>
                      </tr>
                    </thead>
                    <tbody>
                      {logs.length === 0 ? (
                        <tr>
                          <td colSpan={4} className={styles.logEmpty}>
                            {isBackendOnline
                              ? "No logs recorded yet."
                              : "⚠ Cannot reach API. Start the FastAPI backend at port 8080."}
                          </td>
                        </tr>
                      ) : (
                        logs.map((log, i) => (
                          <motion.tr
                            key={log.id}
                            initial={{ opacity: 0, x: -8 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: i * 0.02 }}
                          >
                            <td style={{ fontFamily: "var(--font-mono)", fontSize: "0.8rem" }}>
                              {new Date(log.created_at).toLocaleString("vi-VN")}
                            </td>
                            <td
                              className={
                                log.level === "ERROR"
                                  ? styles.logLevelError
                                  : log.level === "WARNING"
                                  ? styles.logLevelWarn
                                  : styles.logLevelInfo
                              }
                            >
                              {log.level}
                            </td>
                            <td style={{ color: "var(--text-muted)", fontFamily: "var(--font-mono)", fontSize: "0.8rem" }}>
                              {log.source}
                            </td>
                            <td>{log.message}</td>
                          </motion.tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}
