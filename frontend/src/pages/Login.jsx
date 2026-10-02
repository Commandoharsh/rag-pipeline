import { useState } from "react";
import { login } from "../api/auth";

function Login({ onLogin, onCreateAccount }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(event) {
        event.preventDefault();

        try {
            setError("");
            setLoading(true);

            const data = await login(
                email,
                password
            );

            onLogin(data.user);

        } catch (error) {
            setError(
                error.response?.data?.detail ||
                "Login failed."
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="auth-page">

            <div className="auth-card">

                <h1>ResearchRAG</h1>

                <p>
                    Sign in to your research workspace.
                </p>

                <form onSubmit={handleSubmit}>

                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(event) =>
                            setEmail(event.target.value)
                        }
                        required
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(event) =>
                            setPassword(event.target.value)
                        }
                        required
                    />

                    <button
                        type="submit"
                        disabled={loading}
                    >
                        {loading ? "Signing In..." : "Sign In"}
                    </button>

                </form>

                {error && (
                    <p className="error">
                        {error}
                    </p>
                )}

                <div className="auth-switch">

                    <span>
                        Don't have an account?
                    </span>

                    <button
                        type="button"
                        className="auth-link"
                        onClick={onCreateAccount}
                    >
                        Create an account
                    </button>

                </div>

            </div>

        </div>
    );
}

export default Login;