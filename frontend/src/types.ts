export type Country = {
  id: number;
  name: string;
};

export type Competition = {
  id: number;
  name: string;
  country_id: number;
};

export type Club = {
  id: number;
  name: string;
  competition_id: number;
};

export type Player = {
  id: number;
  name: string;
  birth_date: string | null;
  nationality: string | null;
  position_name: string | null;   // <--- asta folosim în tabel
  club_name: string | null;       // opțional dar acum vine din backend
  market_value: string | null;
};
