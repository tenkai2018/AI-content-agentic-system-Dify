"use client";

import {Suspense, useCallback, useEffect, useMemo, useState} from "react";
import {useSearchParams} from "next/navigation";
import Link from "next/link";
import styles from "./dashboard.module.css";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

const STEPS = [
  {id: "viral_detection", icon: "R", label: "Viral Detector", desc: "Scan YouTube and calculate outlier score"},
  {id: "script_writing", icon: "S", label: "Script Writer", desc: "Write script with hook structure"},
  {id: "thumbnail_brief", icon: "T", label: "Thumbnail Brief", desc: "Generate thumbnail brief"},
  {id: "asset_generation", icon: "A", label: "Asset Generator", desc: "Generate image and voiceover"},
  {id: "video_render", icon: "V", label: "Video Producer", desc: "Render video with Remotion"},
  {id: "linkedin_repurposing", icon: "L", label: "LinkedIn Repurposer", desc: "Generate 6 LinkedIn formats"},
];

type PipelineStatus =
  | "pending"
  | "awaiting_topic_approval"
  | "awaiting_script_approval"
  | "awaiting_thumbnail_approval"
  | "awaiting_assets_approval"
  | "repurposing"
  | "completed"
  | "failed";

type StepStatus = "completed" | "active" | "pending";

type StatusPayload = {
  task_id: string;
  status: PipelineStatus;
  niche: string;
  language: string;
  error_message?: string | null;
  outputs: {
    viral_detection_result?: unknown;
    selected_topic?: unknown;
    script_result?: unknown;
    thumbnail_brief?: unknown;
    assets_result?: unknown;
    video_result?: unknown;
    linkedin_posts?: unknown;
  };
};

const isRecord = (v: unknown): v is Record<string, unknown> => typeof v === "object" && v !== null;

function statusToStep(status: PipelineStatus, outputs: StatusPayload["outputs"]): string {
  if (status === "awaiting_topic_approval") return "viral_detection";
  if (status === "awaiting_script_approval") return "script_writing";
  if (status === "awaiting_thumbnail_approval") return "thumbnail_brief";
  if (status === "awaiting_assets_approval") return "asset_generation";
  if (status === "repurposing") return "video_render";
  if (status === "completed") return "linkedin_repurposing";
  if (status === "failed") {
    if (outputs.video_result) return "video_render";
    if (outputs.assets_result) return "asset_generation";
    if (outputs.thumbnail_brief) return "thumbnail_brief";
    if (outputs.script_result) return "script_writing";
    return "viral_detection";
  }
  return "viral_detection";
}

function getStepStatus(stepId: string, currentStep: string): StepStatus {
  const order = STEPS.map((s) => s.id);
  const current = order.indexOf(currentStep);
  const idx = order.indexOf(stepId);
  if (idx < current) return "completed";
  if (idx === current) return "active";
  return "pending";
}

function StatusLabel({status}: {status: PipelineStatus}) {
  const map: Record<PipelineStatus, string> = {
    pending: "Initializing",
    awaiting_topic_approval: "Awaiting topic approval",
    awaiting_script_approval: "Awaiting script approval",
    awaiting_thumbnail_approval: "Awaiting thumbnail approval",
    awaiting_assets_approval: "Awaiting assets approval",
    repurposing: "Finalizing outputs",
    completed: "Completed",
    failed: "Failed",
  };
  return <>{map[status]}</>;
}

function DashboardContent() {
  const searchParams = useSearchParams();
  const taskId = searchParams.get("task_id") ?? "";

  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState("");
  const [data, setData] = useState<StatusPayload | null>(null);

  const fetchStatus = useCallback(async () => {
    if (!taskId) return;
    try {
      const res = await fetch(`${API_BASE}/api/status/${taskId}`, {cache: "no-store"});
      const body = await res.json();
      if (!res.ok) throw new Error(body.detail || "Failed to load status");
      setData(body as StatusPayload);
      setError("");
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to load status");
    } finally {
      setLoading(false);
    }
  }, [taskId]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchStatus();
    if (!taskId) return;
    const timer = setInterval(fetchStatus, 4000);
    return () => clearInterval(timer);
  }, [taskId, fetchStatus]);

  const currentStep = useMemo(() => {
    if (!data) return "viral_detection";
    return statusToStep(data.status, data.outputs);
  }, [data]);

  const approveStep = async (step: "topic" | "script" | "thumbnail" | "assets", approved: boolean) => {
    if (!taskId || !data) return;
    setActionLoading(true);
    setError("");

    const payload: {
      task_id: string;
      step: "topic" | "script" | "thumbnail" | "assets";
      approved: boolean;
      selected_item?: unknown;
    } = {task_id: taskId, step, approved};

    if (step === "topic" && approved) {
      const recommended = data.outputs.selected_topic;
      const fallback = isRecord(data.outputs.viral_detection_result)
        ? data.outputs.viral_detection_result.top_recommended_topic
        : undefined;
      payload.selected_item = recommended || fallback || null;
    }

    try {
      const res = await fetch(`${API_BASE}/api/approve`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload),
      });
      const body = await res.json();
      if (!res.ok) throw new Error(body.detail || "Approve request failed");
      await fetchStatus();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Approve request failed");
    } finally {
      setActionLoading(false);
    }
  };

  const renderApprovalActions = () => {
    if (!data) return null;

    if (data.status === "awaiting_topic_approval") {
      return (
        <div className={styles.actionsRow}>
          <button className={`btn btn-primary ${styles.actionBtn}`} disabled={actionLoading} onClick={() => approveStep("topic", true)}>
            Approve Topic
          </button>
          <button className={`btn btn-ghost ${styles.actionBtn}`} disabled={actionLoading} onClick={() => approveStep("topic", false)}>
            Reject
          </button>
        </div>
      );
    }

    if (data.status === "awaiting_script_approval") {
      return (
        <div className={styles.actionsRow}>
          <button className={`btn btn-primary ${styles.actionBtn}`} disabled={actionLoading} onClick={() => approveStep("script", true)}>
            Approve Script
          </button>
          <button className={`btn btn-ghost ${styles.actionBtn}`} disabled={actionLoading} onClick={() => approveStep("script", false)}>
            Reject
          </button>
        </div>
      );
    }

    if (data.status === "awaiting_thumbnail_approval") {
      return (
        <div className={styles.actionsRow}>
          <button className={`btn btn-primary ${styles.actionBtn}`} disabled={actionLoading} onClick={() => approveStep("thumbnail", true)}>
            Approve Thumbnail
          </button>
          <button className={`btn btn-ghost ${styles.actionBtn}`} disabled={actionLoading} onClick={() => approveStep("thumbnail", false)}>
            Reject
          </button>
        </div>
      );
    }

    if (data.status === "awaiting_assets_approval") {
      return (
        <div className={styles.actionsRow}>
          <button className={`btn btn-primary ${styles.actionBtn}`} disabled={actionLoading} onClick={() => approveStep("assets", true)}>
            Approve Assets and Render
          </button>
          <button className={`btn btn-ghost ${styles.actionBtn}`} disabled={actionLoading} onClick={() => approveStep("assets", false)}>
            Reject
          </button>
        </div>
      );
    }

    return null;
  };

  return (
    <main className={styles.main}>
      <header className={styles.header}>
        <Link href="/" id="back-home-link" className={styles.backLink}>
          Back Home
        </Link>
        <div className={styles.headerCenter}>
          <h1 className={styles.headerTitle}>Content Pipeline</h1>
          <span className={styles.taskId} title="Task ID">
            ID: <code>{taskId || "-"}</code>
          </span>
        </div>
        <span
          className={`${styles.statusBadge} ${
            data?.status === "completed"
              ? styles.statusCompleted
              : data?.status === "failed"
              ? styles.statusFailed
              : styles.statusPending
          }`}
        >
          <StatusLabel status={(data?.status || "pending") as PipelineStatus} />
        </span>
      </header>

      <div className={styles.layout}>
        <aside className={styles.stepper} aria-label="Pipeline progress">
          {STEPS.map((step, i) => {
            const stepStatus = getStepStatus(step.id, currentStep);
            return (
              <div key={step.id} className={`${styles.step} ${styles[stepStatus]}`}>
                <div className={styles.stepIndicator}>
                  <span className={styles.stepIcon} aria-hidden>
                    {stepStatus === "completed" ? "V" : step.icon}
                  </span>
                  {i < STEPS.length - 1 && <div className={styles.stepLine} aria-hidden />}
                </div>
                <div className={styles.stepInfo}>
                  <p className={styles.stepLabel}>{step.label}</p>
                  <p className={styles.stepDesc}>{step.desc}</p>
                </div>
              </div>
            );
          })}
        </aside>

        <section className={styles.resultPanel} aria-label="Pipeline results">
          {loading ? (
            <div className={styles.placeholderCard}>
              <h2 className={styles.placeholderTitle}>Loading status...</h2>
              <div className={styles.loadingDots} aria-label="Loading">
                <span />
                <span />
                <span />
              </div>
            </div>
          ) : (
            <div className={styles.resultCard}>
              <h2 className={styles.resultTitle}>Current Step: {currentStep}</h2>
              {error ? <p className={styles.errorText}>{error}</p> : null}
              {data?.error_message ? <p className={styles.errorText}>Pipeline error: {data.error_message}</p> : null}

              {renderApprovalActions()}

              <div className={styles.resultBlock}>
                <h3>Outputs</h3>
                <pre className={styles.resultJson}>{JSON.stringify(data?.outputs ?? {}, null, 2)}</pre>
              </div>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}

export default function DashboardPage() {
  return (
    <Suspense
      fallback={
        <main
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            minHeight: "100vh",
            color: "#9896b8",
            fontFamily: "Inter, sans-serif",
          }}
        >
          Loading...
        </main>
      }
    >
      <DashboardContent />
    </Suspense>
  );
}
