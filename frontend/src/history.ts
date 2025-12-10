// frontend/src/history.ts
export type SearchItemType = "player" | "club";

export type SearchHistoryItem = {
  id: number;
  name: string;
  type: SearchItemType;
  position?: string;
  league?: string; // ex: "Defender", "Midfielder"
  timestamp: number;
};

const STORAGE_KEY = "transferhub_search_history";
const MAX_ITEMS = 20;

export function loadHistory(): SearchHistoryItem[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    return JSON.parse(raw) as SearchHistoryItem[];
  } catch {
    return [];
  }
}

export function saveHistory(items: SearchHistoryItem[]) {
  if (typeof window === "undefined") return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items.slice(0, MAX_ITEMS)));
}

export function addToHistory(item: Omit<SearchHistoryItem, "timestamp">) {
  const current = loadHistory();

  // nu adăugăm de 2 ori la rând exact același item
  if (current[0] && current[0].id === item.id && current[0].type === item.type) {
    return;
  }

  const next: SearchHistoryItem[] = [
    { ...item, timestamp: Date.now() },
    ...current,
  ];

  saveHistory(next);
}
