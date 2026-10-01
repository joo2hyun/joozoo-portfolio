# Portfolio 2017–2023 (H_mix style)

The 2017–2023 print portfolio rebuilt in the H_mix (D × E) layout: 33 pages at 1440×810.
Shaashop is left out of this edition.

- `mock.py` — Instagram, laptop, monitor, print and city-panel mockups → `img/mock-*.jpg`
- `build.py` — page content and layouts → writes `index.html`
- `deck.css` — H_mix tokens and layouts (Space Grotesk, Archivo, Caveat in `fonts/`)
- `img/` — artwork pulled from the original InDesign PDF
- `render.mjs` — prints `portfolio.pdf` with Playwright

```sh
python3 mock.py && python3 build.py
NODE_PATH=$(npm root -g) node render.mjs   # → portfolio.pdf
```
