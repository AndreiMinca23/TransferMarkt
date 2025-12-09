import { useEffect, useState } from "react";
import { getTopPlayers, type PlayerDetails } from "../api";

export default function DiscoverTopPlayers() {
  const [players, setPlayers] = useState<PlayerDetails[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const data = await getTopPlayers(10);
        setPlayers(data);
      } catch (err) {
        console.error("Eroare la încărcarea top players", err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <section className="card discover-section">
      <div className="discover-section-header">
        <h2>Top 10 cei mai valoroși jucători</h2>
        {loading && <span className="discover-badge">Se încarcă...</span>}
      </div>

      {!loading && players.length === 0 && (
        <p className="discover-empty">
          Nu există jucători cu valoare de piață setată în baza de date.
        </p>
      )}

      <div className="discover-top-players-grid">
        {players.map((p, idx) => (
          <div key={p.id} className="top-player-card">
            <div className="top-player-rank">#{idx + 1}</div>

            <div className="top-player-main">
              <div className="player-avatar big">
                {p.name.charAt(0).toUpperCase()}
              </div>
              <div className="top-player-meta">
                <div className="top-player-name">{p.name}</div>
                <div className="top-player-sub">
                  {p.club_name || "Fără club"}{" "}
                  {p.position_name ? ` • ${p.position_name}` : ""}
                </div>
              </div>
            </div>

            <div className="top-player-value">
              {p.market_value
                ? `${Number(p.market_value).toLocaleString()} €`
                : "-"}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
