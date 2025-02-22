from typing import Iterator, List, Union

from rapidfuzz import process

from commondata_languages.data import languages


class Language:
    """Represents a language with ISO 639 (1/2B/2T/3) codes"""

    def __init__(
        self,
        name: str,
        iso1: str,
        iso2b: str,
        iso2t: str,
        iso3: str,
        scope: str,
        type: str,
    ):
        self.name = name
        self.iso1 = iso1
        self.iso2b = iso2b
        self.iso2t = iso2t
        self.iso3 = iso3
        self.scope = scope
        self.type = type

    def __repr__(self):
        return f"Language(name='{self.name}', iso1={f"'{self.iso1}'" if self.iso1 else None}, iso2b={f"'{self.iso2b}'" if self.iso2b else None}, iso2t={f"'{self.iso2t}'" if self.iso2t else None}, iso3={f"'{self.iso3}'" if self.iso3 else None}, scope='{self.scope}', type='{self.type}')"


class LanguageData:
    """Main API for accessing language data."""

    def __init__(self):
        self._languages = self._load_languages()
        self._index = {c.iso1.upper(): c for c in self._languages if c.iso1 is not None}
        self._index.update(
            {c.iso2b.upper(): c for c in self._languages if c.iso2b is not None}
        )
        self._index.update(
            {c.iso2t.upper(): c for c in self._languages if c.iso2t is not None}
        )
        self._index.update(
            {c.iso3.upper(): c for c in self._languages if c.iso3 is not None}
        )
        self._index.update({c.name.lower(): c for c in self._languages})

    def _load_languages(self) -> List[Language]:
        """Loads language data from a static JSON file."""
        return [
            Language(
                d["name"],
                d["iso1"],
                d["iso2b"],
                d["iso2t"],
                d["iso3"],
                d["scope"],
                d["type"],
            )
            for d in languages
        ]

    def all(self) -> List[Language]:
        """Returns a list of all languages."""
        return self._languages

    def __iter__(self) -> Iterator[Language]:
        """Allows iteration over all languages."""
        return iter(self._languages)

    def __getitem__(self, key: Union[str, int]) -> Union[Language, None]:
        """Lookup language by ISO 1, ISO 2B, ISO 2T, ISO 3, or name (case insensitive, with fuzzy search)."""
        if isinstance(key, int):
            key = str(key)

        key_upper = key.upper()
        key_lower = key.lower()

        if key_upper in self._index:
            return self._index[key_upper]
        if key_lower in self._index:
            return self._index[key_lower]

        # Fuzzy search with rapidfuzz
        language_names = list(self._index.keys())
        closest_match = process.extractOne(key_lower, language_names)

        if closest_match and closest_match[1] > 75:  # Threshold for similarity
            return self._index[closest_match[0]]

        raise KeyError(f"Language '{key}' not found.")
