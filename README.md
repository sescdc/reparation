# NEGRO RESEARCH INSTITUTE Reparations Website

City-by-city reparations research archive and United States summary dossier for Black people in the United States.

## Run Locally

```bash
npm install
npm run prepare:data
npm run dev
```

The site runs at `http://127.0.0.1:5173/`.

## Build

```bash
npm run build
```

## Contents

- `public/reports/` contains the 36 city/regional PDFs plus the generated national United States breakdown PDF.
- `output/pdf/` contains the generated national PDF source artifact.
- `scripts/build_content.py` copies report PDFs, extracts city totals, writes `src/data/reports.json`, and generates the national PDF.
