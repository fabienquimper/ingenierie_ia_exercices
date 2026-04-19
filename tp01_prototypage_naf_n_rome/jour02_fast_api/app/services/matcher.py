import pandas as pd
import re
from pathlib import Path
from typing import Optional
import structlog

logger = structlog.get_logger()


class NafRomeMatcher:
    """Service de correspondance NAF <-> ROME basé sur les données prétraitées."""

    def __init__(self, naf_path: Path, rome_path: Path, matching_path: Path):
        self.df: Optional[pd.DataFrame] = None
        self._load_data(naf_path, rome_path, matching_path)

    def _load_data(self, naf_path: Path, rome_path: Path, matching_path: Path) -> None:
        """Charge les 3 CSV et assigne le type selon la source."""
        sources = [
            (naf_path, "naf"),
            (rome_path, "rome"),
            (matching_path, "matching"),
        ]
        frames = []
        for path, type_label in sources:
            try:
                df = pd.read_csv(path, dtype=str).fillna("")
                df["type"] = type_label
                frames.append(df)
                logger.info("data_loaded", path=str(path), type=type_label, records=len(df))
            except FileNotFoundError:
                logger.error("data_file_not_found", path=str(path))

        if frames:
            self.df = pd.concat(frames, ignore_index=True).fillna("")
        else:
            self.df = pd.DataFrame(columns=["code_naf", "code_rome", "name", "desc", "type"])

    @property
    def record_count(self) -> int:
        return len(self.df) if self.df is not None else 0

    def get_naf_count(self) -> int:
        return int((self.df["type"] == "naf").sum())

    def get_rome_count(self) -> int:
        return int((self.df["type"] == "rome").sum())

    def get_matching_count(self) -> int:
        return int((self.df["type"] == "matching").sum())

    def get_naf_entries(self, limit: int = 100, offset: int = 0) -> list[dict]:
        """Retourne les entrées NAF paginées."""
        df = self.df[self.df["type"] == "naf"].iloc[offset : offset + limit]
        return df.to_dict("records")

    def get_rome_entries(self, limit: int = 100, offset: int = 0) -> list[dict]:
        """Retourne les entrées ROME paginées."""
        df = self.df[self.df["type"] == "rome"].iloc[offset : offset + limit]
        return df.to_dict("records")

    def get_matching_entries(self, limit: int = 100, offset: int = 0) -> list[dict]:
        """Retourne les correspondances NAF↔ROME paginées."""
        df = self.df[self.df["type"] == "matching"].iloc[offset : offset + limit]
        return df.to_dict("records")

    def get_all_entries(self) -> list[dict]:
        """Retourne tous les enregistrements (usage frontend SPA)."""
        return self.df.to_dict("records")

    def get_rome_by_code(self, code_rome: str) -> Optional[dict]:
        """Retourne une entrée ROME par son code."""
        result = self.df[self.df["code_rome"].str.upper() == code_rome.upper()]
        if result.empty:
            return None
        return result.iloc[0].to_dict()

    def get_naf_by_code(self, code_naf: str) -> Optional[dict]:
        """Retourne une entrée NAF par son code."""
        # Normalise le code (avec ou sans point)
        normalized = code_naf.upper().replace(".", "")
        result = self.df[self.df["code_naf"].str.upper().str.replace(".", "", regex=False) == normalized]
        if result.empty:
            return None
        return result.iloc[0].to_dict()

    def get_naf_for_rome(self, code_rome: str) -> list[dict]:
        """Trouve les codes NAF correspondant à un code ROME via les lignes matching."""
        result = self.df[
            (self.df["code_rome"].str.upper() == code_rome.upper()) &
            (self.df["type"] == "matching")
        ]
        return result.to_dict("records")

    def get_rome_for_naf(self, code_naf: str) -> list[dict]:
        """Trouve les codes ROME correspondant à un code NAF via les lignes matching."""
        normalized = code_naf.upper().replace(".", "")
        result = self.df[
            (self.df["code_naf"].str.upper().str.replace(".", "", regex=False) == normalized) &
            (self.df["type"] == "matching")
        ]
        return result.to_dict("records")

    def keyword_search(self, query: str, limit: int = 10) -> list[dict]:
        """Recherche par mots-clés dans name et desc."""
        if self.df is None or self.df.empty:
            return []

        # Normalise la requête
        query_lower = query.lower()
        words = [w for w in re.split(r"\s+", query_lower) if len(w) > 2]

        if not words:
            return []

        # Score: nombre de mots trouvés dans name + desc
        def score_row(row: pd.Series) -> float:
            text = f"{row['name']} {row['desc']}".lower()
            return sum(1.0 for w in words if w in text) / len(words)

        scores = self.df.apply(score_row, axis=1)
        mask = scores > 0
        results = self.df[mask].copy()
        results["score"] = scores[mask]
        results = results.sort_values("score", ascending=False).head(limit)

        return results.to_dict("records")


# Singleton - chargé au démarrage de l'app
_matcher: Optional[NafRomeMatcher] = None


def get_matcher() -> NafRomeMatcher:
    global _matcher
    if _matcher is None:
        raise RuntimeError("Matcher non initialisé. Appelez init_matcher() d'abord.")
    return _matcher


def init_matcher(naf_path: Path, rome_path: Path, matching_path: Path) -> NafRomeMatcher:
    global _matcher
    _matcher = NafRomeMatcher(naf_path, rome_path, matching_path)
    return _matcher
