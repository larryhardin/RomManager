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
  - Limited computer cartridges (e.g. some Commodore 64 carts)
- Notes: Parent/clone DATs available. Excellent for reliable hash matching on cartridge ROMs. Computer coverage is thinner than TOSEC or MAME software lists.

### Redump
- **Website / DATs**: [redump.org](http://redump.org/)
- **Focus**: Optical disc systems (CD-ROM, DVD, GD-ROM, etc.)
- **Supported platforms** (partial list):
  - Sony: PlayStation, PlayStation 2, PlayStation Portable, PlayStation 3
  - Sega: Mega-CD / Sega CD, Saturn, Dreamcast
  - Nintendo: GameCube, Wii
  - Microsoft: Xbox, Xbox 360
  - Computer / other optical: Amiga CD32 / CDTV / Amiga CD, IBM PC CD-ROM, Apple Macintosh CD, Philips CD-i, and more
- Notes: Focuses on verified, high-quality dumps. Ideal for disc images (BIN/CUE, ISO, CHD, etc.).

### MAME (and related)
- **Official**: [mamedev.org](https://www.mamedev.org/)
- **DATs**: Available with each MAME release; also via [progetto-SNAPS](https://www.progettosnaps.net/dats/) and mirrors
- **Focus**: Arcade machines + extensive software lists for home systems (including many computers)
- **Supported platforms**:
  - Arcade (thousands of systems)
  - Software lists covering many consoles, computers, and handhelds (strong overlap and unique coverage for computers)
- **Computer examples** (via software lists): Commodore 64 / 128 / Plus-4 / PET / VIC-20, Apple II / IIe / IIGS / Macintosh, Atari 8-bit / ST / Falcon, Amiga, MSX, ZX Spectrum, and many others
- Notes: Supports full set verification (ROMs, CHDs, BIOS, devices). Excellent for checking completeness and missing files on both arcade and computer software.

### TOSEC (optional / complementary)
- **Website**: [tosecdev.org](https://www.tosecdev.org/)
- **Focus**: Broad coverage of vintage computers, early consoles, and software (different naming convention)
- **Supported platforms** (strong on computers):
  - Commodore: Amiga, C64, C128, Plus/4, PET, VIC-20 (disks, tapes, cartridges)
  - Apple: Apple II, IIe, IIGS, Macintosh
  - Atari: 8-bit Family, ST, Falcon, Jaguar
  - Other computers: MSX / MSX2, ZX Spectrum, Amstrad CPC, BBC Micro, Acorn, IBM PC, and many more
  - Also covers some consoles and handhelds
- Notes: Useful as a secondary or primary source for computer software when No-Intro/Redump coverage is limited. Uses its own naming convention. DATs freely available.

### Aggregated / Convenience Sources
- [libretro/libretro-database](https://github.com/libretro/libretro-database) — curated No-Intro, Redump, TOSEC, and other DATs used by RetroArch (includes many computer systems)
- Daily-updated clrmamepro profiles (various community mirrors)

These sources provide free, publicly downloadable DAT files. Matching is done by hash rather than filename for accuracy. Region information is included in the official naming conventions of No-Intro and Redump.

## Computer Systems Coverage Summary

| System Family       | Primary DAT Source(s)          | Notes                                      |
|---------------------|--------------------------------|--------------------------------------------|
| Commodore (C64, Amiga, etc.) | TOSEC, MAME software lists, limited No-Intro | Strong disk/tape coverage in TOSEC/MAME   |
| Apple (II, Macintosh) | TOSEC, MAME software lists, Redump (CD) | Good optical and floppy support            |
| Atari (8-bit, ST, etc.) | No-Intro (8-bit), TOSEC, MAME | Solid multi-source coverage                |
| MSX / ZX Spectrum / Amstrad | TOSEC, MAME software lists     | Primarily computer-focused databases       |
| IBM PC (early software) | TOSEC, Redump (CD-ROM), MAME   | Mix of floppy and optical                  |

For most computer ROMs (especially disk and tape images), TOSEC and MAME software lists are the most complete free sources. No-Intro and Redump remain preferred for pure cartridge and modern optical disc systems.
