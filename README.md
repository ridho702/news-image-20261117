# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/ridho702/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/ridho702/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

An infographic summing up the world news of Tuesday 17 November 2026, built for make.fun's ["Sum up 17 November's world news in one image"](https://make.fun/bounty/news-image-20261117) bounty ($250 in USDC).

## Run it

```sh
python3 build_image.py          # regenerates entry.png (1024x1024, PNG)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=pxdmc197&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>

## The six stories in the image

Researched on 18 November 2026 from the outlets below. Every item happened
or was first reported on 17 November 2026.

1. **US strikes Iran after drone attack on Bahrain** (Middle East) —
   US jets hit a missile site on Qeshm Island; Iran fired drones at a US
   radar in Bahrain, its third strike there in five days.
   Sources: CBS News, NPR, Al Jazeera (via One Turn, 17 Nov 2026).
2. **Kerch Bridge span falls after second day of strikes** (Ukraine war) —
   Ukrainian drones hit the Crimea bridge again; a road section collapsed
   into the strait.
   Sources: BBC, CNN (17 Nov 2026).
3. **Trump in Manila on way to Xi–Putin summit** (Asia-Pacific) — The US
   president heads to the APEC summit in Shenzhen for planned three-way
   nuclear talks with Xi Jinping and Vladimir Putin.
   Sources: BBC, CBS News (17 Nov 2026).
4. **Nvidia posts record $115bn quarter** (Business) — Revenue roughly
   doubled year on year, but the board will not bring back ousted chief
   Jensen Huang.
   Sources: BBC, NYT (17 Nov 2026).
5. **Ebola passes 11,000 cases in DR Congo** (Health) — The UN reports
   more than 5,400 deaths as the outbreak more than doubles in three months.
   Source: UN News (via One Turn, 17 Nov 2026).
6. **Five EU states plan Rwanda returns hub** (Migration) — Germany,
   Denmark, Austria, Greece and the Netherlands will send rejected asylum
   seekers to a joint facility from 2027.
   Sources: AP, Al Jazeera (17 Nov 2026).

Footer "Also today": the US loses measles elimination status after 26 years
(BBC, 17 Nov 2026); Gérard Depardieu admits a sexual-assault charge in a
Paris court (17 Nov 2026); Nepal is the first country to have funding
provisionally set aside from the UN loss and damage fund after floods
(One Turn, 17 Nov 2026).

## How the image was built

`build_image.py` draws the infographic programmatically with Pillow
(DejaVu fonts): a newspaper-style front page with a dated masthead, six
story rows (region tag, headline, two-line summary, drawn pictogram) and a
footer strip. No photographs are used, so there are no rights issues;
no news was invented and no quotes were fabricated.

`main.py` is the entrypoint: it copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`).
The image is at most 1024x1024 pixels and under 1 MiB, as the rules require.
