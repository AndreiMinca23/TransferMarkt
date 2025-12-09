import type { AuthMode } from "./components/App";

type Props = {
  onChoose: (mode: AuthMode) => void;
};

export default function LandingPage({ onChoose }: Props) {
  return (
    <div className="landing-container">
      <div className="landing-content">
        <div className="landing-left">
          <div className="auth-logo">TransferHub</div>
          <h1>Platformă de transferuri și statistici fotbalistice</h1>
          <p>
            Gestionează jucători, cluburi și competiții într-o interfață
            modernă, inspirată de Transfermarkt și gata pentru producție.
          </p>

          <div className="landing-actions">
            <button
              className="landing-btn primary"
              onClick={() => onChoose("login")}
            >
              Login
            </button>
            <button
              className="landing-btn secondary"
              onClick={() => onChoose("register")}
            >
              Crează cont
            </button>
          </div>

          <p className="landing-note">
            Ai deja cont în sistem? Alege Login. Dacă nu, îți poți crea unul nou
            în câteva secunde.
          </p>
        </div>

        <div className="landing-right">
          <div className="auth-gradient" />
          <div className="landing-right-inner">
            <h2>Date reale. Decizii mai bune.</h2>
            <p>
              Centralizează informațiile despre jucători, urmărește
              transferurile și analizează loturile cluburilor din diferite
              competiții europene.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
