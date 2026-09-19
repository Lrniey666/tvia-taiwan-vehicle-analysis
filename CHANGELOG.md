# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- GitHub showcase tree at the repository root: Django project `config/`, app `dashboard/`, analysis helpers, TDX fetchers, bilingual README (zh-Hant / en).
- Environment-based secrets (`.env.example`): Django secret key, allowed hosts, TDX client id/secret. Extra TDX apps rotate via `TDX_CLIENT_ID_2` and onwards.
- Management commands `fetch_tdx` and `import_legacy`. Secret-free demo fixture `data/fixtures/demo.json.gz`.
- Parameterised chart routes (one view/template per family instead of a page per city).
- MIT licence, contributing guide, architecture and data-source notes.

### Changed

- TDX credentials are no longer read from the database or hard-coded in fetchers.
- Public navigation no longer links to `/admin/`.
- Team credits use GitHub handles only.

### Removed

- Student numbers, Django admin passwords, ChatGPT transcripts, draft slides, nested `mysite/mysite`, `__pycache__`, and the Anaconda dump `requirements.txt`.
- Working copy `original-data/` is gitignored.

## [1.0.0] - 2023-06-18

### Added

- Course hand-in for NKUST *Python 資料分析實務*, group 10.
- Django 4.2 site with Chart.js: national vehicle rankings, six-municipality growth versus household income, per-capita income versus vehicles, and student share versus car/scooter mix.
- TDX ingest for household vehicles, household income, university student status, and town-level population.
