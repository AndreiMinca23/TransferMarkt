import { useEffect, useState } from "react";
import { getTopClubs, type TopClub } from "../api";

export default function DiscoverTopClubs() {
  const [clubs, setClubs] = useState<TopClub[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const data = await getTopClubs(5);
        setClubs(data);
      } catch (err) {
        console.error("Eroare la încărcarea top clubs", err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <section className="card discover-section">
      <div className="discover-section-header">
        <h2>Top cluburi după valoarea lotului</h2>
        {loading && <span className="discover-badge">Se încarcă...</span>}
      </div>

      {!loading && clubs.length === 0 && (
        <p className="discover-empty">
          Nu există suficiente date pentru a calcula valoarea loturilor.
        </p>
      )}

      <div className="discover-top-clubs-list">
        {clubs.map((c, idx) => (
          <div key={c.club_id} className="top-club-row">
            <div className="top-club-left">
              <div className="top-club-rank">#{idx + 1}</div>
              <div className="top-club-meta">
                <div className="top-club-name">{c.club_name}</div>
                <div className="top-club-sub">
                  {c.player_count} jucător
                  {c.player_count === 1 ? "" : "i"} în lot
                </div>
              </div>
            </div>

            <div className="top-club-value">
              {c.total_value
                ? `${Math.round(c.total_value).toLocaleString()} €`
                : "-"}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
