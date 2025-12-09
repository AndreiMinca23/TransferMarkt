import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import type { ClubDetails } from "./components/api";
import { getClubById } from "./components/api";

export default function ClubPage() {
  const { id } = useParams<{ id: string }>();
  const [club, setClub] = useState<ClubDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;

    async function load() {
      try {
        setLoading(true);
        const data = await getClubById(Number(id));
        setClub(data);
      } catch (err: any) {
        setError(err.message || "Eroare la încărcarea clubului.");
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [id]);

  if (loading) return <div className="p-8 text-white">Se încarcă...</div>;
  if (error) return <div className="p-8 text-red-400">{error}</div>;
  if (!club) return <div className="p-8 text-white">Clubul nu există.</div>;

  return (
    <div className="p-8 text-white">
      <h1 className="text-3xl font-bold mb-6">{club.name}</h1>

      <div className="flex gap-10 mb-10">
        <div>
          <div className="text-xs text-gray-400 uppercase">Țară</div>
          <div className="text-lg">{club.country_name || "-"}</div>
        </div>
        <div>
          <div className="text-xs text-gray-400 uppercase">Competiție</div>
          <div className="text-lg">{club.competition_name || "-"}</div>
        </div>
      </div>
    </div>
  );
}
