# MAME DAT files

Best source for current MAME DATs: **progetto-SNAPS**

- Main page: https://www.progettosnaps.net/dats/MAME/
- Latest pack (0.289): https://www.progettosnaps.net/download/?tipo=dat_mame&file=/dats/MAME/packs/MAME_Dats_289.7z

These DATs are generated from official MAME releases and are the standard used by clrmamepro and most ROM managers for arcade set verification.

## How to get the files

Run the fetch script:

```bash
bash data/MAME/fetch_dat.sh
```

It will download the latest pack and extract it into this directory.

Official MAME source: https://www.mamedev.org/ (you can also generate a DAT with `mame -listxml > mame.xml`).
