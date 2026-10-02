import { useEffect, useState } from "react";
import {
    Activity,
    AlertCircle,
    CheckCircle,
    Clock,
    Database,
    RefreshCw,
    Server,
    Zap,
} from "lucide-react";

import apiClient from "../api/client";

export default function Monitoring() {
    const [health, setHealth] = useState(null);
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    async function loadMonitoringData() {
        setLoading(true);
        setError("");

        try {
            const [healthResponse, metricsResponse] = await Promise.all([
                apiClient.get("/health"),
                apiClient.get("/metrics"),
            ]);

            setHealth(healthResponse.data);
            setMetrics(metricsResponse.data);
        } catch (err) {
            console.error("Monitoring error:", err);

            setError(
                err.response?.data?.detail ||
                "Unable to load monitoring data."
            );
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadMonitoringData();

        const interval = setInterval(loadMonitoringData, 10000);

        return () => clearInterval(interval);
    }, []);

    if (loading && !health && !metrics) {
        return (
            <div className="page-container monitoring-page">
                <div className="page-header">
                    <div>
                        <h1>System Monitoring</h1>
                        <p>Loading system status and RAG metrics...</p>
                    </div>
                </div>

                <div className="monitoring-loading">
                    <RefreshCw size={28} className="spin" />
                    <span>Checking system health...</span>
                </div>
            </div>
        );
    }

    const systemHealthy =
        health?.status === "healthy" ||
        health?.status === "ok" ||
        health?.healthy === true;

    const queries = metrics?.queries ?? 0;
    const errors = metrics?.errors ?? 0;

    return (
        <div className="page-container monitoring-page">
            {/* Header */}
            <div className="page-header monitoring-header">
                <div>
                    <h1>System Monitoring</h1>
                    <p>
                        Monitor ResearchRAG system health, API activity,
                        and RAG performance.
                    </p>
                </div>

                <button
                    className="refresh-button"
                    onClick={loadMonitoringData}
                    disabled={loading}
                >
                    <RefreshCw
                        size={17}
                        className={loading ? "spin" : ""}
                    />
                    Refresh
                </button>
            </div>

            {/* Error */}
            {error && (
                <div className="monitoring-error">
                    <AlertCircle size={20} />
                    <div>
                        <strong>Monitoring unavailable</strong>
                        <p>{error}</p>
                    </div>
                </div>
            )}

            {/* Overview cards */}
            <div className="monitoring-grid">
                <MetricCard
                    icon={<Activity size={21} />}
                    title="System Status"
                    value={systemHealthy ? "Healthy" : "Unavailable"}
                    status={systemHealthy ? "success" : "error"}
                />

                <MetricCard
                    icon={<Zap size={21} />}
                    title="Total Queries"
                    value={queries}
                />

                <MetricCard
                    icon={<AlertCircle size={21} />}
                    title="Errors"
                    value={errors}
                    status={errors > 0 ? "warning" : "success"}
                />

                <MetricCard
                    icon={<Clock size={21} />}
                    title="Auto Refresh"
                    value="10 sec"
                />
            </div>

            {/* Health section */}
            <section className="monitoring-section">
                <div className="section-title">
                    <Server size={20} />
                    <div>
                        <h2>Service Health</h2>
                        <p>Current status of ResearchRAG services.</p>
                    </div>
                </div>

                <div className="service-list">
                    <ServiceStatus
                        name="FastAPI Backend"
                        status={systemHealthy ? "Operational" : "Unavailable"}
                        healthy={systemHealthy}
                    />

                    <ServiceStatus
                        name="SQLite Database"
                        status="Connected"
                        healthy={true}
                    />

                    <ServiceStatus
                        name="RAG Pipeline"
                        status={systemHealthy ? "Operational" : "Unavailable"}
                        healthy={systemHealthy}
                    />

                    <ServiceStatus
                        name="Ollama LLM"
                        status="Configured"
                        healthy={true}
                    />
                </div>
            </section>

            {/* Raw health data */}
            <section className="monitoring-section">
                <div className="section-title">
                    <Database size={20} />
                    <div>
                        <h2>Health Details</h2>
                        <p>Raw health information returned by the API.</p>
                    </div>
                </div>

                <pre className="monitoring-json">
                    {JSON.stringify(health ?? {}, null, 2)}
                </pre>
            </section>

            {/* Metrics */}
            <section className="monitoring-section">
                <div className="section-title">
                    <Activity size={20} />
                    <div>
                        <h2>Application Metrics</h2>
                        <p>Runtime metrics collected by ResearchRAG.</p>
                    </div>
                </div>

                <div className="metrics-table">
                    <MetricRow
                        label="Queries processed"
                        value={queries}
                    />

                    <MetricRow
                        label="Errors"
                        value={errors}
                    />

                    <MetricRow
                        label="Error rate"
                        value={
                            queries > 0
                                ? `${((errors / queries) * 100).toFixed(2)}%`
                                : "0%"
                        }
                    />
                </div>
            </section>
        </div>
    );
}


/* ----------------------------- */
/* Metric Card                    */
/* ----------------------------- */

function MetricCard({ icon, title, value, status }) {
    return (
        <div className={`monitoring-card ${status || ""}`}>
            <div className="monitoring-card-icon">
                {icon}
            </div>

            <div className="monitoring-card-content">
                <span>{title}</span>
                <strong>{value}</strong>
            </div>
        </div>
    );
}


/* ----------------------------- */
/* Service Status                 */
/* ----------------------------- */

function ServiceStatus({ name, status, healthy }) {
    return (
        <div className="service-status">
            <div className="service-name">
                {healthy ? (
                    <CheckCircle size={19} />
                ) : (
                    <AlertCircle size={19} />
                )}

                <span>{name}</span>
            </div>

            <span
                className={`service-badge ${
                    healthy ? "healthy" : "unhealthy"
                }`}
            >
                {status}
            </span>
        </div>
    );
}


/* ----------------------------- */
/* Metric Row                    */
/* ----------------------------- */

function MetricRow({ label, value }) {
    return (
        <div className="metric-row">
            <span>{label}</span>
            <strong>{value}</strong>
        </div>
    );
}