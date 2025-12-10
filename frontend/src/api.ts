// frontend/src/api.ts
import type { Country, Competition, Club, Player } from "./types";

// ----------------- CONFIG API -----------------

// dacă VITE_API_URL nu e setat, folosim http://localhost:5001
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5001";

// ----------------- AUTH LOCALSTORAGE -----------------

const TOKEN_KEY = "tm_token";
const USER_KEY = "tm_user";

export function saveAuth(token: string, user: any) {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function getUser(): any | null {
  const raw = localStorage.getItem(USER_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

// ----------------- HELPER PT GET CU FETCH -----------------

async function apiGet<T>(
  path: string,
  params?: Record<string, any>
): Promise<T> {
  const url = new URL(path, API_URL);
  if (params) {
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== "") {
        url.searchParams.append(k, String(v));
      }
    });
  }

  const headers: HeadersInit = {};
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(url.toString(), { headers });
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

// ----------------- ENDPOINT-URI SIMPLE -----------------

export function getHealth() {
  return apiGet<{ status: string }>("/api/health");
}

export function getCountries() {
  return apiGet<Country[]>("/api/countries");
}

export function getCompetitions(countryId?: number | "") {
  return apiGet<Competition[]>("/api/competitions", {
    country_id: countryId || undefined,
  });
}

export function getClubs(competitionId?: number | "") {
  return apiGet<Club[]>("/api/clubs", {
    competition_id: competitionId || undefined,
  });
}

export function getPlayers(clubId?: number | "") {
  return apiGet<Player[]>("/api/players", {
    club_id: clubId || undefined,
  });
}

// ----------------- REGISTER / LOGIN -----------------

export async function registerRequest(payload: {
  full_name: string;
  email: string;
  phone: string;
  password: string;
  confirm_password: string;
}) {
  const res = await fetch(`${API_URL}/api/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    let message = "Nu s-a putut crea contul.";
    try {
      const data = await res.json();
      // FastAPI / Pydantic 422 -> { detail: [ { msg, loc, type, ... }, ... ] }
      if (data?.detail) {
        if (typeof data.detail === "string") {
          message = data.detail;
        } else if (Array.isArray(data.detail)) {
          const msgs = data.detail
            .map((e: any) => e.msg || e.detail || "")
            .filter(Boolean);
          if (msgs.length) {
            message = msgs.join(" | ");
          }
        }
      }
    } catch {
      // ignorăm parse error, păstrăm mesajul default
    }
    throw new Error(message);
  }

  return res.json();
}

export async function loginRequest(email: string, password: string) {
  const res = await fetch(`${API_URL}/api/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!res.ok) {
    let message = "Login eșuat.";
    try {
      const data = await res.json();
      if (data?.detail) {
        if (typeof data.detail === "string") {
          message = data.detail;
        } else if (Array.isArray(data.detail)) {
          const msgs = data.detail
            .map((e: any) => e.msg || e.detail || "")
            .filter(Boolean);
          if (msgs.length) {
            message = msgs.join(" | ");
          }
        }
      }
    } catch {
      // lăsăm mesajul default
    }
    throw new Error(message);
  }

  const data = await res.json();
  // backend-ul tău ar trebui să întoarcă: { access_token, user }
  saveAuth(data.access_token, data.user);
  return data;
}

// ----------------- TIPURI PENTRU SEARCH -----------------

export type PlayerDetails = {
  id: number;
  name: string;
  birth_date: string | null;
  nationality: string | null;
  position_name: string | null;
  club_name: string | null;
  market_value: string | null;
  competition_name: string | null; s
};

export type SearchClubResponse = {
  type: "club";
  club: { id: number; name: string };
  players: PlayerDetails[];
};

export type SearchPlayerResponse = {
  type: "player";
  player: PlayerDetails;
};

export type TopClub = {
  club_id: number;
  club_name: string;
  total_value: number;
  player_count: number;
};


export type SearchResponse = SearchClubResponse | SearchPlayerResponse;

// ----------------- SEARCH /api/search -----------------

export async function searchEntities(query: string): Promise<SearchResponse> {
  // folosim helper-ul apiGet bazat pe fetch
  return apiGet<SearchResponse>("/api/search", { q: query });
}

// ----------------- DETALII JUCĂTOR / CLUB -----------------

export function getTopClubs(limit: number = 5) {
  return apiGet<TopClub[]>("/api/top-clubs", { limit });
}

export function getTopPlayers(limit: number = 10) {
  return apiGet<PlayerDetails[]>("/api/top-players", { limit });
}

export function getPlayerById(id: number) {
  return apiGet<PlayerDetails>(`"/api/players/${id}"`.replace('"', "").replace('"', ""));
}

export type ClubDetails = {
  id: number;
  name: string;
  country_name: string | null;
  competition_name: string | null;
};

export function getClubById(id: number) {
  return apiGet<ClubDetails>(`/api/clubs/${id}`);
}
