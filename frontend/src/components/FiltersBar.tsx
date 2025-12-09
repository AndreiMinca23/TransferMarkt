import { useEffect, useState } from "react";
import { getCountries, getCompetitions, getClubs } from "../api";
import type { Country, Competition, Club } from "./types";

type Props = {
  selectedCountry: number | "";
  setSelectedCountry: (id: number | "") => void;
  selectedCompetition: number | "";
  setSelectedCompetition: (id: number | "") => void;
  selectedClub: number | "";
  setSelectedClub: (id: number | "") => void;
};

export default function FiltersBar({
  selectedCountry,
  setSelectedCountry,
  selectedCompetition,
  setSelectedCompetition,
  selectedClub,
  setSelectedClub,
}: Props) {
  const [countries, setCountries] = useState<Country[]>([]);
  const [competitions, setCompetitionsState] = useState<Competition[]>([]);
  const [clubs, setClubsState] = useState<Club[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getCountries().then(setCountries).catch(console.error);
  }, []);

  useEffect(() => {
    if (!selectedCountry) {
      setCompetitionsState([]);
      setClubsState([]);
      setSelectedCompetition("");
      setSelectedClub("");
      return;
    }
    setLoading(true);
    getCompetitions(selectedCountry)
      .then((data) => {
        setCompetitionsState(data);
        setClubsState([]);
        setSelectedCompetition("");
        setSelectedClub("");
      })
      .finally(() => setLoading(false));
  }, [selectedCountry]);

  useEffect(() => {
    if (!selectedCompetition) {
      setClubsState([]);
      setSelectedClub("");
      return;
    }
    setLoading(true);
    getClubs(selectedCompetition)
      .then((data) => {
        setClubsState(data);
        setSelectedClub("");
      })
      .finally(() => setLoading(false));
  }, [selectedCompetition]);

  return (
    <div className="filters-bar">
      <div className="filter-group">
        <label className="filter-label">Țară</label>
        <select
          className="filter-select"
          value={selectedCountry}
          onChange={(e) =>
            setSelectedCountry(e.target.value ? Number(e.target.value) : "")
          }
        >
          <option value="">Toate țările</option>
          {countries.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label className="filter-label">Competiție</label>
        <select
          className="filter-select"
          value={selectedCompetition}
          onChange={(e) =>
            setSelectedCompetition(
              e.target.value ? Number(e.target.value) : ""
            )
          }
          disabled={!selectedCountry}
        >
          <option value="">Toate competițiile</option>
          {competitions.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label className="filter-label">Club</label>
        <select
          className="filter-select"
          value={selectedClub}
          onChange={(e) =>
            setSelectedClub(e.target.value ? Number(e.target.value) : "")
          }
          disabled={!selectedCompetition}
        >
          <option value="">Toate cluburile</option>
          {clubs.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      <div className="filters-status">
        {loading ? "Se încarcă..." : "Filtre gata ✅"}
      </div>
    </div>
  );
}
