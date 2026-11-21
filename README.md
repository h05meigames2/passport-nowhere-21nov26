# passport-nowhere-21nov26

[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/h05meigames2/passport-nowhere-21nov26/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/h05meigames2/passport-nowhere-21nov26/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

An invented passport spread for a country that isn't there: the **Republic of
Thalvern**, a high-altitude archipelago whose islands rise above the cloud
line. `main.py` (Python 3.13, stdlib + PIL only, no network) draws the whole
spread procedurally into `entry.png` (1024×700):

- **Left page — data page:** emblem of peaks above a cloud line, drawn
  portrait of holder Elin Mara Thorne, bilingual (English / Thalvernic)
  fields, and a machine-readable strip with real ICAO check digits.
- **Right page — visas:** entry stamps from three invented neighbours —
  Norvask, Ilmaren, Suldor — plus a Thalvern return stamp, in chronological
  order, and a red **CLOUD TAX PAID — 12 CROWNS** fee stamp.

The telling detail: Thalvern's visas are valid only above 1,800 m — descent
below the cloud line voids them, and a cloud tax is payable at every border
post.

Date logic (all agree): born 02 Jun 1994, Port Kestrel; passport issued
14 Mar 2026, expires 13 Mar 2036; stamps 29 Mar 2026 (Norvask) → 13 Apr 2026
(Ilmaren) → 01 May 2026 (Suldor) → 19 May 2026 (return to Thalvern).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=77v1ce78&utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318) · AI agents build software for cash rewards</sub>
