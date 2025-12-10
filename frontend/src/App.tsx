import { useEffect, useState } from "react";
import Layout from "./components/Layout";
import LandingPage from "./components/LandingPage";
import LoginPage from "./components/LoginPage";
import FiltersBar from "./components/FiltersBar";
import PlayersTable from "./components/PlayersTable";
import MainTabs, { MainTab } from "./components/MainTabs";
import PlayerDetailsCard from "./components/PlayerDetailsCard";
import DiscoverTopPlayers from "./components/DiscoverTopPlayers";
import DiscoverTopClubs from "./components/DiscoverTopClubs";
import DiscoverRecommended from "./components/DiscoverRecommended";
import { addToHistory } from "./history";

import {
  getHealth,
  getUser,
  clearAuth,
  searchEntities,
  type PlayerDetails,
} from "./api";

export type AuthMode = "login" | "register";
type AuthStep = "landing" | "auth";

type View = "market" | "player" | "club";

type SearchedClub = {
  id: number;
  name: string;
};

function App() {
  // --------- AUTH STATE ----------
  const [loggedIn, setLoggedIn] = useState(() => !!getUser());
  const [authStep, setAuthStep] = useState<AuthStep>("landing");
  const [authMode, setAuthMode] = useState<AuthMode>("login");

  // --------- FILTERS / DATA ----------
  const [selectedCountry, setSelectedCountry] = useState<number | "">("");
  const [selectedCompetition, setSelectedCompetition] = useState<number | "">(
    ""
  );
  const [selectedClub, setSelectedClub] = useState<number | "">("");

  const [backendStatus, setBackendStatus] = useState<string | null>(null);

  // --------- MAIN TABS ----------
  const [mainTab, setMainTab] = useState<MainTab>("squads");

  // --------- VIEW / SEARCH STATE ----------
  const [view, setView] = useState<View>("market");

  const [searchedPlayer, setSearchedPlayer] = useState<PlayerDetails | null>(
    null
  );

  const [searchedClub, setSearchedClub] = useState<SearchedClub | null>(null);
  const [searchedClubPlayers, setSearchedClubPlayers] = useState<
    PlayerDetails[]
  >([]);

  // --------- HEALTH CHECK ----------
  useEffect(() => {
    getHealth()
      .then((d) => setBackendStatus(d.status))
      .catch(() => setBackendStatus("error"));
  }, []);

  // --------- LOGOUT ----------
  const handleLogout = () => {
    clearAuth();
    setLoggedIn(false);
    setAuthStep("landing");
    setAuthMode("login");
    setMainTab("squads");
    setView("market");
    setSearchedPlayer(null);
    setSearchedClub(null);
    setSearchedClubPlayers([]);
    setSelectedCountry("");
    setSelectedCompetition("");
    setSelectedClub("");
  };

  // --------- SEARCH ----------
  const handleSearch = async (query: string) => {
    try {
      const res = await searchEntities(query);
      console.log("searchEntities result:", res); 

      if (res.type === "club") {
        // “pagina” pentru club
        setView("club");
        setMainTab("squads");
        setSearchedClub(res.club);
        setSearchedClubPlayers(res.players);
        setSelectedClub(res.club.id);
        setSearchedPlayer(null);

        // salvăm clubul în istoric (fără poziție)
        
      } else {
        // “pagina” pentru jucător
        setView("player");
        setMainTab("squads");
        setSearchedPlayer(res.player);
        setSearchedClub(null);
        setSearchedClubPlayers([]);

        // salvăm jucătorul în istoric (cu poziție)
        addToHistory({
          id: res.player.id,
          name: res.player.name,
          type: "player",
          position: res.player.position_name || undefined,
          league: res.player.competition_name || undefined,
        });
      }
    } catch (err) {
      console.error(err);
      alert("Nu am găsit niciun club sau jucător pentru căutarea introdusă.");
    }
  };

  // ============================================================
  //                     AUTH FLOW (NELOGAT)
  // ============================================================

  if (!loggedIn) {
    if (authStep === "landing") {
      return (
        <LandingPage
          onChoose={(mode) => {
            setAuthMode(mode);
            setAuthStep("auth");
          }}
        />
      );
    }

    return (
      <LoginPage
        initialMode={authMode}
        onLoginSuccess={() => {
          setLoggedIn(true);
          setMainTab("squads");
          setView("market");
        }}
        onBackToLanding={() => setAuthStep("landing")}
      />
    );
  }

  // ============================================================
  //              CONTENT LOGGED-IN (VIEWS + LAYOUT)
  // ============================================================

  const marketplaceElement = (
    <>
      {/* Bara cu tab-uri gen Transfermarkt */}
      <MainTabs selected={mainTab} onChange={setMainTab} />

      {/* Header-ul de pagină doar la tab-ul Squads */}
      {mainTab === "squads" && (
        <div className="page-header">
          <div>
            <h1>Marketplace-ul tău de transferuri</h1>
            <p>
              Filtrează după țară, competiție și club pentru a vedea jucătorii
              din baza ta de date.
            </p>
          </div>
          <div className="status-pill">
            Backend:{" "}
            <span
              className={
                backendStatus === "ok"
                  ? "status-dot status-dot-ok"
                  : "status-dot status-dot-bad"
              }
            />
            <span className="status-text">
              {backendStatus === "ok"
                ? "online"
                : backendStatus === "error"
                ? "eroare"
                : "se verifică..."}
            </span>
          </div>
        </div>
      )}

      {mainTab === "squads" && (
        <>
          <FiltersBar
            selectedCountry={selectedCountry}
            setSelectedCountry={setSelectedCountry}
            selectedCompetition={selectedCompetition}
            setSelectedCompetition={setSelectedCompetition}
            selectedClub={selectedClub}
            setSelectedClub={setSelectedClub}
          />
          <PlayersTable clubId={selectedClub} />
        </>
      )}

      {mainTab !== "squads" && (
        <>
          {mainTab === "discover" && (
            <>
              <section className="page-header">
                <div>
                  <h1>Discover</h1>
                  <p>
                    Explorează cei mai valoroși jucători și cele mai puternice
                    loturi din baza ta de date.
                  </p>
                </div>
              </section>

              {/* Pasul 1 – Top jucători */}
              <DiscoverTopPlayers />

              {/* Pasul 2 – Top cluburi */}
              <DiscoverTopClubs />

              {/* Pasul 3 – Recommended for you (după ultima căutare) */}
              <DiscoverRecommended />
            </>
          )}

          {mainTab !== "discover" && (
            <section className="card main-tab-placeholder">
              <h2>
                {mainTab === "transfers" && "Transfers & Rumours"}
                {mainTab === "values" && "Market Values"}
                {mainTab === "competitions" && "Competitions"}
                {mainTab === "stats" && "Statistics"}
              </h2>
              <p>
                Secțiunea aceasta încă nu este implementată. Poți extinde aici
                pagini dedicate pentru transferuri, valori de piață, statistici
                și competiții, asemănător cu Transfermarkt.
              </p>
            </section>
          )}
        </>
      )}
    </>
  );

  return (
    <Layout onLogout={handleLogout} onSearch={handleSearch}>
      {/* VIEW: marketplace clasic */}
      {view === "market" && marketplaceElement}

      {/* VIEW: detalii jucător */}
      {view === "player" && searchedPlayer && (
        <div className="p-8">
          <button
            className="btn-back"
            onClick={() => {
              setView("market");
              setSearchedPlayer(null);
            }}
          >
            Înapoi la marketplace
          </button>

          <PlayerDetailsCard player={searchedPlayer} />
        </div>
      )}

      {/* VIEW: detalii club */}
      {view === "club" && searchedClub && (
        <div className="p-8 text-white">
          <button
            className="btn-back"
            onClick={() => {
              setView("market");
              setSearchedClub(null);
              setSearchedClubPlayers([]);
            }}
          >
            Înapoi la marketplace
          </button>

          <div className="page-header">
            <div>
              <h1>{searchedClub.name}</h1>
              <p>Lotul actual al clubului din baza ta de date.</p>
            </div>
          </div>

          <div className="card">
            <table className="players-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Jucător</th>
                  <th>Poziție</th>
                  <th>Vârstă</th>
                  <th>Valoare de piață</th>
                </tr>
              </thead>
              <tbody>
                {searchedClubPlayers.map((p, idx) => (
                  <tr key={p.id}>
                    <td>{idx + 1}</td>
                    <td>{p.name}</td>
                    <td>{p.position_name || "-"}</td>
                    <td>
                      {p.birth_date
                        ? new Date().getFullYear() -
                          new Date(p.birth_date).getFullYear()
                        : "-"}
                    </td>
                    <td>
                      {p.market_value
                        ? `${Number(p.market_value).toLocaleString()} €`
                        : "-"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </Layout>
  );
}

export default App;
