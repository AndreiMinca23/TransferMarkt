// src/components/MainTabs.tsx
export type MainTab =
  | "discover"
  | "transfers"
  | "values"
  | "competitions"
  | "stats"
  | "squads";

type Props = {
  selected: MainTab;
  onChange: (tab: MainTab) => void;
};

const TABS: { key: MainTab; label: string }[] = [
  { key: "discover", label: "Discover" },
  { key: "transfers", label: "Transfers & Rumours" },
  { key: "values", label: "Market Values" },
  { key: "competitions", label: "Competitions" },
  { key: "stats", label: "Statistics" },
  { key: "squads", label: "Squads / Line-ups" },
];

export default function MainTabs({ selected, onChange }: Props) {
  return (
    <nav className="main-tabs-bar">
      <ul className="main-tabs-list">
        {TABS.map((tab) => (
          <li key={tab.key}>
            <button
              type="button"
              className={
                tab.key === selected
                  ? "main-tab-btn main-tab-btn-active"
                  : "main-tab-btn"
              }
              onClick={() => onChange(tab.key)}
            >
              {tab.label}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
}
