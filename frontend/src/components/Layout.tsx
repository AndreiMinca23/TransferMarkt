import { ReactNode, useState } from "react";
import { getUser } from "../api";

type Props = {
  children: ReactNode;
  onLogout?: () => void;
  onSearch?: (q: string) => void;
};

export default function Layout({ children, onLogout, onSearch }: Props) {
  const user = getUser();
  const fullName = user?.full_name || "Utilizator";
  const firstLetter = fullName.charAt(0).toUpperCase();

  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="app-shell">
      {/* HEADER */}
      <header className="app-header">
        {/* Logo stânga */}
        <div className="app-logo">
          <span style={{ color: "#38bdf8" }}>Transfer</span>
          <span>Hub</span>
          <span className="app-logo-pill">LIVE</span>
        </div>

        {/* Search la mijloc */}
        <div className="header-search">
          <input
            className="header-search-input"
            placeholder="Caută jucător, club sau competiție..."
            onKeyDown={(e) => {
              if (e.key === "Enter" && onSearch) {
                const value = (e.target as HTMLInputElement).value;
                if (value.trim()) {
                  onSearch(value.trim());
                }
              }
            }}
          />
        </div>

        {/* User dreapta */}
        <div className="header-user">
          <div className="header-user-avatar">{firstLetter}</div>
          <div className="header-user-info">
            <div className="header-user-name">{fullName}</div>
            {user?.email && (
              <div className="header-user-email">{user.email}</div>
            )}
          </div>

          {/* buton mic pentru meniul userului */}
          {onLogout && (
            <button
              type="button"
              className="header-user-toggle"
              onClick={() => setMenuOpen((o) => !o)}
            >
              ▾
            </button>
          )}

          {/* dropdown Logout */}
          {menuOpen && onLogout && (
            <div
              className="header-user-menu"
              onClick={(e) => {
                e.stopPropagation();
                setMenuOpen(false);
                onLogout();
              }}
            >
              Logout
            </div>
          )}
        </div>
      </header>

      {/* MAIN AREA – fără sidebar, doar conținut */}
      <div className="app-main">
        <main className="app-content">{children}</main>
      </div>
    </div>
  );
}
