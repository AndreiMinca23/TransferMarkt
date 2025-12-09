import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import type { PlayerDetails } from "../api";
import { getPlayerById } from "../api";

export default function PlayerPage() {
  const { id } = useParams<{ id: string }>();
  const [player, setPlayer] = useState<PlayerDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;

    async function load() {
      try {
        setLoading(true);
        const data = await getPlayerById(Number(id));
        setPlayer(data);
      } catch (err: any) {
        setError(err.message || "Eroare la încărcarea jucătorului.");
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [id]);

  if (loading) return <div className="p-8 text-white">Se încarcă...</div>;
  if (error) return <div className="p-8 text-red-400">{error}</div>;
  if (!player) return <div className="p-8 text-white">Jucătorul nu există.</div>;

  return (
    <div className="p-8 text-white">
      <h1 className="text-3xl font-bold mb-6">{player.name}</h1>

      <div className="flex flex-wrap gap-10 mb-10">
        <div>
          <div className="text-xs text-gray-400 uppercase">Club</div>
          <div className="text-lg">{player.club_name || "-"}</div>
        </div>
        <div>
          <div className="text-xs text-gray-400 uppercase">Poziție</div>
          <div className="text-lg">{player.position_name || "-"}</div>
        </div>
        <div>
          <div className="text-xs text-gray-400 uppercase">Naționalitate</div>
          <div className="text-lg">{player.nationality || "-"}</div>
        </div>
        <div>
          <div className="text-xs text-gray-400 uppercase">Dată naștere</div>
          <div className="text-lg">
            {player.birth_date
              ? new Date(player.birth_date).toLocaleDateString()
              : "-"}
          </div>
        </div>
        <div>
          <div className="text-xs text-gray-400 uppercase">Valoare de piață</div>
          <div className="text-lg font-semibold text-green-400">
            {player.market_value
              ? `${Number(player.market_value).toLocaleString()} €`
              : "-"}
          </div>
        </div>
      </div>
    </div>
  );
}
