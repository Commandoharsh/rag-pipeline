import { useState } from "react";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Chat from "./pages/Chat";

import { getToken } from "./api/auth";

function App() {
    const [authenticated, setAuthenticated] =
        useState(Boolean(getToken()));

    const [showRegister, setShowRegister] =
        useState(false);

    const [user, setUser] =
        useState(null);

    if (!authenticated) {
        if (showRegister) {
            return (
                <Register
                    onRegistered={() => {
                        setShowRegister(false);
                    }}
                    onBackToLogin={() => {
                        setShowRegister(false);
                    }}
                />
            );
        }

        return (
            <Login
                onLogin={(loggedInUser) => {
                    setUser(loggedInUser);
                    setAuthenticated(true);
                }}
                onCreateAccount={() => {
                    setShowRegister(true);
                }}
            />
        );
    }

    return (
        <Chat
            user={user}
            onLogout={() => {
                setAuthenticated(false);
                setUser(null);
            }}
        />
    );
}

export default App;