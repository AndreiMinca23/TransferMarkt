import { useState } from "react";
import { loginRequest, registerRequest } from "../api";
import type { AuthMode } from "../App";

type Props = {
  onLoginSuccess: () => void;
  initialMode?: AuthMode;
  onBackToLanding?: () => void;
};

export default function LoginPage({
  onLoginSuccess,
  initialMode = "login",
  onBackToLanding,
}: Props) {
  const [mode, setMode] = useState<AuthMode>(initialMode);

  // LOGIN state
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [loginShowPassword, setLoginShowPassword] = useState(false);
  const [loginError, setLoginError] = useState<string | null>(null);
  const [loginLoading, setLoginLoading] = useState(false);

  // REGISTER state
  const [regName, setRegName] = useState("");
  const [regEmail, setRegEmail] = useState("");
  const [regPhone, setRegPhone] = useState("");
  const [regPassword, setRegPassword] = useState("");
  const [regConfirmPassword, setRegConfirmPassword] = useState("");
  const [regShowPassword, setRegShowPassword] = useState(false);
  const [regError, setRegError] = useState<string | null>(null);
  const [regLoading, setRegLoading] = useState(false);

  const switchMode = (newMode: AuthMode) => {
    setMode(newMode);
    setLoginError(null);
    setRegError(null);
  };

  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError(null);
    setLoginLoading(true);
    try {
      await loginRequest(loginEmail, loginPassword);
      onLoginSuccess();
    } catch (err: any) {
      setLoginError(err.message || "Autentificare eșuată.");
    } finally {
      setLoginLoading(false);
    }
  };

  const handleRegisterSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setRegError(null);
    setRegLoading(true);

    try {
      await registerRequest({
        full_name: regName,
        email: regEmail,
        phone: regPhone,
        password: regPassword,
        confirm_password: regConfirmPassword,
      });

      await loginRequest(regEmail, regPassword);
      onLoginSuccess();
    } catch (err: any) {
      setRegError(err.message || "Înregistrare eșuată.");
    } finally {
      setRegLoading(false);
    }
  };

  return (
    <div className="auth-container">
      {/* CARD STÂNGA */}
      <div className="auth-card">
        <div className="auth-header-row">
          <div className="auth-logo">TransferHub</div>
          {onBackToLanding && (
            <button
              type="button"
              className="auth-link-btn"
              onClick={onBackToLanding}
            >
              &larr; Înapoi
            </button>
          )}
        </div>

        <div style={{ display: "flex", gap: "0.75rem", marginBottom: "1.5rem" }}>
          <button
            type="button"
            className={
              "auth-tab-btn " +
              (mode === "login" ? "auth-tab-btn-active" : "")
            }
            onClick={() => switchMode("login")}
          >
            Login
          </button>
          <button
            type="button"
            className={
              "auth-tab-btn " +
              (mode === "register" ? "auth-tab-btn-active" : "")
            }
            onClick={() => switchMode("register")}
          >
            Creare cont
          </button>
        </div>

        {mode === "login" ? (
          <>
            <h1 className="auth-title">Autentificare</h1>
            <p className="auth-subtitle">
              Introdu datele contului tău pentru a accesa aplicația.
            </p>

            <form className="auth-form" onSubmit={handleLoginSubmit}>
              <label className="auth-label">
                Email
                <input
                  type="email"
                  className="auth-input"
                  placeholder="you@example.com"
                  value={loginEmail}
                  onChange={(e) => setLoginEmail(e.target.value)}
                  required
                  pattern="^[^\s@]+@[^\s@]+\.[^\s@]+$"
                  title="Introdu un email valid, de forma nume@domeniu.com"
                />
              </label>

              <label className="auth-label">
                Parolă
                <div className="auth-password-wrapper">
                  <input
                    type={loginShowPassword ? "text" : "password"}
                    className="auth-input"
                    placeholder="Parola ta"
                    value={loginPassword}
                    onChange={(e) => setLoginPassword(e.target.value)}
                    required
                  />
                  <button
                    type="button"
                    className="auth-show-btn"
                    onClick={() => setLoginShowPassword((s) => !s)}
                  >
                    {loginShowPassword ? "Hide" : "Show"}
                  </button>
                </div>
              </label>

              {loginError && <div className="auth-error">{loginError}</div>}

              <button className="auth-submit" type="submit" disabled={loginLoading}>
                {loginLoading ? "Se conectează..." : "Login"}
              </button>
            </form>
          </>
        ) : (
          <>
            <h1 className="auth-title">Creare cont</h1>
            <p className="auth-subtitle">
              Completează datele de mai jos pentru a-ți crea un cont.
            </p>

            <form className="auth-form" onSubmit={handleRegisterSubmit}>
              <label className="auth-label">
                Nume complet
                <input
                  type="text"
                  className="auth-input"
                  placeholder="Nume și prenume"
                  value={regName}
                  onChange={(e) => setRegName(e.target.value)}
                  required
                />
              </label>

              <label className="auth-label">
                Email
                <input
                  type="email"
                  className="auth-input"
                  placeholder="you@example.com"
                  value={regEmail}
                  onChange={(e) => setRegEmail(e.target.value)}
                  required
                  pattern="^[^\s@]+@[^\s@]+\.[^\s@]+$"
                  title="Introdu un email valid, de forma nume@domeniu.com"
                />
              </label>

              <label className="auth-label">
                Telefon
                <input
                  type="tel"
                  className="auth-input"
                  placeholder="07xxxxxxxx sau +407xxxxxxxx"
                  value={regPhone}
                  onChange={(e) => setRegPhone(e.target.value)}
                  required
                  pattern="^(\+4)?0[0-9]{9}$"
                  title="Introdu un număr valid: 07xxxxxxxx sau +407xxxxxxxx"
                />
              </label>

              <label className="auth-label">
                Parolă
                <div className="auth-password-wrapper">
                  <input
                    type={regShowPassword ? "text" : "password"}
                    className="auth-input"
                    placeholder="Minim 6 caractere, o literă mare și o cifră"
                    value={regPassword}
                    onChange={(e) => setRegPassword(e.target.value)}
                    required
                    pattern="^(?=.*[A-Z])(?=.*\d).{6,}$"
                    title="Parola trebuie să aibă minim 6 caractere, o literă mare și o cifră."
                  />
                </div>
              </label>

              <label className="auth-label">
                Confirmă parola
                <input
                  type={regShowPassword ? "text" : "password"}
                  className="auth-input"
                  placeholder="Reintrodu parola"
                  value={regConfirmPassword}
                  onChange={(e) => setRegConfirmPassword(e.target.value)}
                  required
                />
              </label>

              <label
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "0.35rem",
                  fontSize: "0.8rem",
                  color: "#9ca3af",
                }}
              >
                <input
                  type="checkbox"
                  checked={regShowPassword}
                  onChange={() => setRegShowPassword((s) => !s)}
                />
                Arată parola
              </label>

              {regError && <div className="auth-error">{regError}</div>}

              <button className="auth-submit" type="submit" disabled={regLoading}>
                {regLoading ? "Se creează contul..." : "Crează cont"}
              </button>
            </form>
          </>
        )}

        <div className="auth-footer">
          {mode === "login" ? (
            <span>
              Nu ai cont?{" "}
              <button
                type="button"
                className="auth-link-btn"
                onClick={() => switchMode("register")}
              >
                Crează unul nou.
              </button>
            </span>
          ) : (
            <span>
              Ai deja cont?{" "}
              <button
                type="button"
                className="auth-link-btn"
                onClick={() => switchMode("login")}
              >
                Mergi la login.
              </button>
            </span>
          )}
        </div>
      </div>

      {/* PANOU DREAPTA */}
      <div className="auth-side-panel">
        <div className="auth-gradient" />
        <div className="auth-side-content">
          <h2>Transferuri. Statistici. Insight-uri.</h2>
          <p>
            Explorează jucători, cluburi și competiții într-o interfață
            construită pentru utilizare reală, nu doar demo.
          </p>
        </div>
      </div>
    </div>
  );
}
