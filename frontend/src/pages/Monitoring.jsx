import { useEffect, useState } from "react";
import {
    Activity,
    Database,
    Server,
    Cpu,
    Bot,
    RefreshCw,
    CheckCircle,
    AlertTriangle,
} from "lucide-react";

import apiClient from "../api/client";

const icons = {
    sqlite: Database,
    qdrant: Server,
    embeddings: Cpu,
    ollama: Bot,
};

function ServiceCard({
    name,
    service,
}) {
    const Icon =
        icons[name] || Activity;

    const healthy =
        service?.status ===
        "healthy";

    return (
        <div className="service-card">
            <div className="service-card-top">
                <div className="service-icon">
                    <Icon size={20} />
                </div>

                {healthy ? (
                    <CheckCircle
                        size={18}
                        className="healthy-icon"
                    />
                ) : (
                    <AlertTriangle
                        size={18}
                        className="warning-icon"
                    />
                )}
            </div>

            <h3>
                {name.charAt(0).toUpperCase() +
                    name.slice(1)}
            </h3>

            <div
                className={`service-status ${
                    healthy
                        ? "healthy"
                        : "unhealthy"
                }`}
            >
                {service?.status ||
                    "unknown"}
            </div>

            {service?.latency_ms !==
                undefined && (
                <div className="service-latency">
                    {service.latency_ms} ms
                </div>
            )}

            {service?.error && (
                <div className="service-error">
                    {service.error}
                </div>
            )}
        </div>
    );
}

function Monitoring() {
    const [health, setHealth] =
        useState(null);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState("");

    async function loadHealth() {
        try {
            setLoading(true);
            setError("");

            const response =
                await apiClient.get(
                    "/health"
                );

            setHealth(response.data);
        } catch (error) {
            console.error(error);

            setError(
                error.response?.data
                    ?.detail ||
                    "Unable to reach the health endpoint."
            );
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadHealth();

        const interval =
            setInterval(
                loadHealth,
                30000
            );

        return () =>
            clearInterval(
                interval
            );
    }, []);

    return (
        <div className="monitoring-page">
            <div className="monitoring-header">
                <div>
                    <h1>
                        System Monitoring
                    </h1>

                    <p>
                        Monitor the ResearchRAG
                        backend services.
                    </p>
                </div>

                <button
                    className="refresh-button"
                    onClick={
                        loadHealth
                    }
                    disabled={loading}
                >
                    <RefreshCw
                        size={17}
                        className={
                            loading
                                ? "spin"
                                : ""
                        }
                    />

                    Refresh
                </button>
            </div>

            {error && (
                <div className="monitoring-error">
                    {error}
                </div>
            )}

            {health && (
                <>
                    <div className="overall-health">
                        <div>
                            <span>
                                Overall Status
                            </span>

                            <strong>
                                {
                                    health.status
                                }
                            </strong>
                        </div>

                        <div
                            className={`health-indicator ${
                                health.status ===
                                "healthy"
                                    ? "healthy"
                                    : "degraded"
                            }`}
                        >
                            {health.status}
                        </div>
                    </div>

                    <div className="services-grid">
                        {Object.entries(
                            health.services ||
                                {}
                        ).map(
                            ([
                                name,
                                service,
                            ]) => (
                                <ServiceCard
                                    key={
                                        name
                                    }
                                    name={
                                        name
                                    }
                                    service={
                                        service
                                    }
                                />
                            )
                        )}
                    </div>
                </>
            )}
        </div>
    );
}

export default Monitoring;