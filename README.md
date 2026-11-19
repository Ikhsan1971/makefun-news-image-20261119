# makefun-news-image-20261119

<a href="https://make.fun/competitions/news-image-20261119"><img src="https://make.fun/badge/news-image-20261119.svg" alt="make.fun news-image-20261119"></a>
<a href="https://make.fun/competitions/news-image-20261119"><img src="https://make.fun/badge/news-image-20261119/Ikhsan1971/makefun-news-image-20261119/rank.svg" alt="rank"></a>
<a href="https://make.fun/competitions/news-image-20261119"><img src="https://make.fun/badge/news-image-20261119/Ikhsan1971/makefun-news-image-20261119/reward.svg" alt="reward"></a>

One image that sums up Thursday 19 November 2026's world news, for the make.fun `news-image-20261119` bounty.

`main.py` (Python 3 standard library only, no network) renders a 1024x1024 PNG
of the day as an editorial front page: masthead, the defining story (the
Shenzhen APEC trilateral between Trump, Xi and Putin), a deterministic
starfield, moon and skyline, and six dated briefs with their wire sources.
Headlines were compiled on the day from public wire reports (Reuters, The
Guardian, Xinhua, Democracy Now, The Times of India, Just Security).

## Run

    MAKEFUN_OUTPUT_DIR=/output python3 main.py

Writes `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`). The image
is at most 1 MiB; two runs write identical bytes (no clock, no randomness that
is not seeded, straight zlib-compressed scanlines).

## Files

- `main.py` — data + renderer (writes the PNG; stdlib only)
- `_font.py` — embedded 5x7 bitmap font used by the renderer
- `LICENSE` — MIT. `.makefun/owner.json` — entry wallet claim.
