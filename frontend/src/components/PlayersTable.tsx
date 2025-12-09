// frontend/src/components/PlayersTable.tsx
import { useEffect, useState } from "react";
import type { Player } from "../types";
import { getPlayers } from "../api";
type Props = {
  clubId: number | "";
};

export default function PlayersTable({ clubId }: Props) {
  const [players, setPlayers] = useState<Player[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!clubId) {
      setPlayers([]);
      return;
    }

    async function load() {
      try {
        setLoading(true);
        const data = await getPlayers(clubId);
        setPlayers(data);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [clubId]);

  if (!clubId) {
    return (
      <section className="card players-table-wrapper">
        <div className="players-table-header">
          <h2>Jucători</h2>
        </div>
        <p className="players-empty">Niciun club selectat.</p>
      </section>
    );
  }

  return (
    <section className="card players-table-wrapper">
      <div className="players-table-header">
        <h2>Jucători</h2>
        <div className="players-count">
          {players.length} jucător{players.length === 1 ? "" : "i"}
        </div>
      </div>

      <table className="players-table">
        <thead>
          <tr>
            <th className="col-index">#</th>
            <th className="col-player">Jucător</th>
            <th className="col-position">Poziție</th>
            <th className="col-age">Vârstă</th>
            <th className="col-value">Valoare de piață</th>
          </tr>
        </thead>
        <tbody>
          {players.map((p, idx) => {
            const age =
              p.birth_date
                ? new Date().getFullYear() -
                  new Date(p.birth_date).getFullYear()
                : null;

            return (
              <tr key={p.id}>
                <td className="col-index">{idx + 1}</td>
                <td className="col-player">
                  <div className="player-cell">
                    <div className="player-avatar">
                      {p.name.charAt(0).toUpperCase()}
                    </div>
                    <div className="player-meta">
                      <div className="player-name">{p.name}</div>
                      {p.club_name && (
                        <div className="player-club">{p.club_name}</div>
                      )}
                    </div>
                  </div>
                </td>
                <td className="col-position">
                  {p.position_name || "-"}
                </td>
                <td className="col-age">
                  {age !== null ? age : "-"}
                </td>
                <td className="col-value">
                  {p.market_value
                    ? `${Number(p.market_value).toLocaleString()} €`
                    : "-"}
                </td>
              </tr>
            );
          })}

          {!players.length && !loading && (
            <tr>
              <td colSpan={5} className="players-empty">
                Nu există jucători pentru acest club.
              </td>
            </tr>
          )}
        </tbody>
      </table>

      {loading && (
        <div className="players-loading">Se încarcă jucătorii...</div>
      )}
    </section>
  );
}
