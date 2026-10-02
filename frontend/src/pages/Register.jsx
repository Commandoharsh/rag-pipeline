import { useState } from "react";
import { register } from "../api/auth";

function Register({ onRegistered, onBackToLogin }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(event) {
        event.preventDefault();

        try {
            setError("");
            setLoading(true);

            await register(
                email,
                password
            );

            onRegistered();

        } catch (error) {
            setError(
                error.response?.data?.detail ||
                "Registration failed."
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="auth-page">

            <div className="auth-card">

                <h1>Create Account</h1>

                <p>
                    Create your ResearchRAG workspace.
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
                        minLength={8}
                        required
                    />

                    <button
                        type="submit"
                        disabled={loading}
                    >
                        {loading
                            ? "Creating Account..."
                            : "Create Account"}
                    </button>

                </form>

                {error && (
                    <p className="error">
                        {error}
                    </p>
                )}

                <div className="auth-switch">

                    <span>
                        Already have an account?
                    </span>

                    <button
                        type="button"
                        className="auth-link"
                        onClick={onBackToLogin}
                    >
                        Sign in
                    </button>

                </div>

            </div>

        </div>
    );
}

export default Register;