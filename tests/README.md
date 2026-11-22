# Tests

## Sample Match Cases

`sample_matches.json` contains reference cases — one representative known-good hash per major database / platform combination.

Each case is designed so that a correct matcher (hash lookup against the corresponding DAT) returns **exactly 1 result**.

### Current coverage
- **No-Intro**: NES, SNES, Game Boy
- **Redump**: PlayStation, Saturn
- **MAME**: Arcade (Pac-Man example)
- **TOSEC**: Commodore 64 (example)

### Running the tests

```bash
pip install -r requirements.txt
pytest
```

`test_sample_matches.py` loads every case into a `RomMatcher` and asserts that looking up its hash(es) returns exactly one match with the expected metadata.

### How the cases are meant to be used long-term
1. Load the relevant DAT file(s) for the platform.
2. Look up the provided CRC32 / MD5 / SHA1.
3. Assert that exactly one game entry is returned and that the name matches (or is a known variant).

These are starting points. Expand the file with additional platforms as the matcher is implemented. Full per-platform coverage of every No-Intro / Redump / MAME / TOSEC system is not practical in a single static file; these samples cover the primary databases and major system families listed in the main README.
