import type { PlayerDetails } from "../api";

type Props = {
  player: PlayerDetails;
};

export default function PlayerDetailsCard({ player }: Props) {
  return (
    <section className="card player-details-card">
      <h2>{player.name}</h2>
      <div className="player-details-grid">
        {player.club_name && (
          <div>
            <span className="label">Club</span>
            <span>{player.club_name}</span>
          </div>
        )}
        {player.position_name && (
          <div>
            <span className="label">Poziție</span>
            <span>{player.position_name}</span>
          </div>
        )}
        {player.nationality && (
          <div>
            <span className="label">Naționalitate</span>
            <span>{player.nationality}</span>
          </div>
        )}
        {player.birth_date && (
          <div>
            <span className="label">Data nașterii</span>
            <span>{player.birth_date}</span>
          </div>
        )}
        {player.market_value && (
          <div>
            <span className="label">Valoare de piață</span>
            <span>{player.market_value} €</span>
          </div>
        )}
      </div>
    </section>
  );
}
