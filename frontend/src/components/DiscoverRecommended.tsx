import { useEffect, useState } from "react";
import { loadHistory, type SearchHistoryItem } from "../history";
import {
  getTopPlayers,
  getPlayerById,
  type PlayerDetails,
} from "../api";
import PlayerDetailsCard from "./PlayerDetailsCard";

type RecommendationMode = "combo" | "position" | "none";

type RecommendationInfo = {
  mode: RecommendationMode;
  position?: string;
  league?: string;
};

// helper pentru comparație string (ignoram case + spații)
function normalize(str: string | null | undefined): string {
  return (str || "").toLowerCase().trim();
}

export default function DiscoverRecommended() {
  const [history, setHistory] = useState<SearchHistoryItem[]>([]);
  const [lastItem, setLastItem] = useState<SearchHistoryItem | null>(null);
  const [info, setInfo] = useState<RecommendationInfo>({ mode: "none" });
  const [allPlayers, setAllPlayers] = useState<PlayerDetails[]>([]);
  const [recommended, setRecommended] = useState<PlayerDetails[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingLeague, setLoadingLeague] = useState(false);

  // 1. încărcăm istoricul și ultima căutare
  useEffect(() => {
    const h = loadHistory();
    console.log("Search history:", h);
    setHistory(h);

    if (h.length === 0) {
      setLastItem(null);
      setInfo({ mode: "none" });
      return;
    }

    const last = h[0];
    setLastItem(last);

    const position = last.position;
    const league = last.league;

    if (position && league) {
      setInfo({ mode: "combo", position, league });
    } else if (position) {
      setInfo({ mode: "position", position });
    } else {
      setInfo({ mode: "none" });
    }
  }, []);

  // 2. dacă ultima căutare e player și nu avem ligă, o luăm din backend cu getPlayerById
  useEffect(() => {
    if (!lastItem) return;
    if (lastItem.type !== "player") return;
    if (lastItem.league) return;
    if (!lastItem.position) return;

    async function fetchLeague() {
      try {
        setLoadingLeague(true);
        const player = await getPlayerById(lastItem.id);
        console.log("Fetched player for league:", player);

        if (player.competition_name) {
          setInfo({
            mode: "combo",
            position: lastItem.position!,
            league: player.competition_name,
          });
        } else {
          setInfo({
            mode: "position",
            position: lastItem.position!,
          });
        }
      } catch (e) {
        console.error("Eroare la getPlayerById pentru ligă:", e);
      } finally {
        setLoadingLeague(false);
      }
    }

    fetchLeague();
  }, [lastItem]);

  // 3. luăm cât mai mulți jucători ca bază pentru recomandări
  useEffect(() => {
    async function loadPlayers() {
      setLoading(true);
      try {
        // CREȘTEM LIMITA ca să prindem și LaLiga etc.
        const players = await getTopPlayers(500);
        console.log("Top players (sample):", players.slice(0, 5));
        setAllPlayers(players);
      } catch (e) {
        console.error("Eroare getTopPlayers:", e);
      } finally {
        setLoading(false);
      }
    }
    loadPlayers();
  }, []);

  // 4. filtrăm recomandările după poziție + ligă, cu fallback pe doar poziție
  useEffect(() => {
    if (info.mode === "none" || !info.position || allPlayers.length === 0) {
      setRecommended([]);
      return;
    }

    const wantedPos = normalize(info.position);
    const wantedLeague = normalize(info.league);

    let comboFiltered: PlayerDetails[] = [];
    let posFiltered: PlayerDetails[] = [];

    // doar poziție
    posFiltered = allPlayers.filter(
      (p) => normalize(p.position_name) === wantedPos
    );

    // poziție + ligă (dacă avem ligă)
    if (info.mode === "combo" && info.league) {
      comboFiltered = allPlayers.filter((p) => {
        const posOk = normalize(p.position_name) === wantedPos;
        const leagueOk = normalize(p.competition_name) === wantedLeague;
        return posOk && leagueOk;
      });
    }

    let finalList: PlayerDetails[] = [];

    if (comboFiltered.length > 0) {
      // ideal: poziție + ligă (ex: fundași din LaLiga)
      finalList = comboFiltered;
    } else {
      // fallback: doar poziție (ex: fundași din toate ligile)
      finalList = posFiltered;
    }

    finalList = finalList
      .sort(
        (a, b) =>
          (Number(b.market_value) || 0) - (Number(a.market_value) || 0)
      )
      .slice(0, 8);

    console.log("Recommendation info:", info);
    console.log("Recommended players:", finalList);

    setRecommended(finalList);
  }, [info, allPlayers]);

  const hasHistory = history.length > 0;
  const hasRecommendations = recommended.length > 0;

  let title = "Recommended for you";
  if ((info.mode === "combo" || info.mode === "position") && info.position) {
    if (info.mode === "combo" && info.league) {
      title = `${info.position} din ${info.league} pe care i-ai putea urmări`;
    } else {
      title = `${info.position} pe care i-ai putea urmări`;
    }
  }

  return (
    <section className="card" style={{ marginTop: "2rem" }}>
      <div className="page-header">
        <div>
          <h2>{title}</h2>
          <p>
            Bazat pe <strong>ultima ta căutare</strong> de jucător
            (istoricul este salvat doar în browserul tău).
          </p>
        </div>
      </div>

      <div style={{ fontSize: "0.8rem", opacity: 0.7, marginBottom: "0.75rem" }}>
        <div>
          <strong>Debug:</strong>{" "}
          mode=<code>{info.mode}</code>, position=<code>{info.position || "∅"}</code>, league=
          <code>{info.league || "∅"}</code>{" "}
          {loadingLeague && <span>(fetching league...)</span>}
        </div>
      </div>

      {!hasHistory && (
        <p>
          Nu avem încă istoric de căutări. Caută un jucător (de exemplu un
          fundaș din LaLiga) și apoi revino pe această pagină.
        </p>
      )}

      {hasHistory && !hasRecommendations && !loading && (
        <p>
          Pentru ultima ta căutare nu am găsit încă jucători recomandați în top.
          Vezi mai jos istoricul căutărilor.
        </p>
      )}

      {loading && (
        <p>Încărcăm recomandările...</p>
      )}

      {hasRecommendations && (
        <div className="players-grid">
          {recommended.map((p) => (
            <PlayerDetailsCard key={p.id} player={p} />
          ))}
        </div>
      )}

      {hasHistory && (
        <div style={{ marginTop: "1rem" }}>
          <h3>Ultimele căutări</h3>
          <div className="history-chips">
            {history.slice(0, 10).map((item) => (
              <span
                key={`${item.type}-${item.id}-${item.timestamp}`}
                className="chip"
              >
                {item.type === "player" ? "👤" : "🏟️"} {item.name}
                {item.position ? ` (${item.position})` : ""}
                {item.league ? ` – ${item.league}` : ""}
              </span>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
