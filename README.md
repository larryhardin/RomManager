# RomManager

Professional local ROM manager with UI, API, and CLI for scanning and matching ROMs against free public databases.

## Free Databases We Use

RomManager matches ROMs primarily via cryptographic hashes (CRC32, MD5, SHA1) against the following freely available DAT sources. These are the industry-standard databases used by most scrapers and ROM managers.

### No-Intro
- **Website / DATs**: [datomatic.no-intro.org](https://datomatic.no-intro.org/)
- **Focus**: Cartridge-based systems (and some disk/tape formats)
- **Supported platforms** (partial list of major ones; hundreds total):
  - Nintendo: NES / Famicom, SNES / Super Famicom, Game Boy, Game Boy Color, Game Boy Advance, Nintendo 64, Nintendo DS, Family Computer Disk System, Virtual Boy, Pokémon Mini, etc.
  - Sega: Master System, Game Gear, Mega Drive / Genesis, 32X, SG-1000
  - Atari: 2600, 5200, 7800, Lynx, Jaguar, 8-bit Family
  - Other consoles/handhelds: ColecoVision, Intellivision, Vectrex, WonderSwan, Neo Geo Pocket, PC Engine / TurboGrafx-16, and many obscure systems
  - Some computer cartridges (e.g. Commodore 64 carts)
- Notes: Parent/clone DATs available. Excellent for reliable hash matching on cartridge ROMs.

### Redump
- **Website / DATs**: [redump.org](http://redump.org/)
- **Focus**: Optical disc systems (CD-ROM, DVD, GD-ROM, etc.)
- **Supported platforms** (partial list):
  - Sony: PlayStation, PlayStation 2, PlayStation Portable, PlayStation 3
  - Sega: Mega-CD / Sega CD, Saturn, Dreamcast
  - Nintendo: GameCube, Wii
  - Microsoft: Xbox, Xbox 360
  - Other: Panasonic 3DO, Neo Geo CD, PC Engine CD, PC-FX, Amiga CD32/CDTV, Philips CD-i, IBM PC CD-ROM, and more
- Notes: Focuses on verified, high-quality dumps. Ideal for disc images (BIN/CUE, ISO, CHD, etc.).

### MAME (and related)
- **Official**: [mamedev.org](https://www.mamedev.org/)
- **DATs**: Available with each MAME release; also via [progetto-SNAPS](https://www.progettosnaps.net/dats/) and mirrors
- **Focus**: Arcade machines + software lists for many home systems
- **Supported platforms**:
  - Arcade (thousands of systems)
  - Software lists covering many consoles, computers, and handhelds (overlapping with No-Intro/Redump in some cases)
- Notes: Supports full set verification (ROMs, CHDs, BIOS, devices). Useful for both matching and checking completeness / missing files.

### TOSEC (optional / complementary)
- **Website**: [tosecdev.org](https://www.tosecdev.org/)
- **Focus**: Broader coverage of vintage computers, early consoles, and software (different naming convention)
- **Supported platforms**: Many home computers (Amiga, Atari ST, Commodore, Apple II, etc.), some consoles, and other media
- Notes: Useful as a secondary source when No-Intro/Redump do not cover a title or dump variant. Different naming style.

### Aggregated / Convenience Sources
- [libretro/libretro-database](https://github.com/libretro/libretro-database) — curated No-Intro, Redump, and other DATs used by RetroArch
- Daily-updated clrmamepro profiles (various community mirrors)

These sources provide free, publicly downloadable DAT files. Matching is done by hash rather than filename for accuracy. Region information is included in the official naming conventions of No-Intro and Redump.
