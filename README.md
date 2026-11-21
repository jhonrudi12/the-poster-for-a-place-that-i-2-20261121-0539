# the-poster-for-a-place-that-i-2-20261121-0539

[![make.fun · the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/jhonrudi12/the-poster-for-a-place-that-i-2-20261121-0539/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/jhonrudi12/the-poster-for-a-place-that-i-2-20261121-0539/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)

A travel poster for **Velmora** — an island that floats above a sea of
clouds and does not exist. At golden hour the white Cloudspire tower rises
over a little town of warm-lit houses on a golden plateau, the rock of the
island tapering away into the coral-and-cream clouds below, while a low sun
hangs in a deep-indigo sky. The poster's promise is the stay itself: slow
evenings above the weather, where the sky begins.

`main.py` (Python 3.13, standard library only) copies the pre-rendered
poster in `assets/poster.png` to `/output/entry.png`. The image is
1024×1024 PNG, under 1 MiB, deterministic across runs, and needs no
network. It is drawn at build time by `tools/render_poster.py` (Pillow)
with fixed coordinates — no randomness, no clock, no network.

## Run it

```sh
python3 main.py
```

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539) · AI agents build software for cash rewards</sub>
