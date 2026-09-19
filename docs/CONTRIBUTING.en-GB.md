# Contributing

Languages: [繁體中文](../CONTRIBUTING.md) · [English (UK)](CONTRIBUTING.en-GB.md)

This is an archived 2023 coursework site. Fixes to docs, empty states, and chart readability are welcome. Treat it as a historical artefact first.

## Before you start

1. Read the root [`README.md`](../README.md) and [`docs/README.md`](README.md).
2. Secrets live in `.env` only. TDX credentials, the Django secret key, and admin passwords must not enter git.
3. On conflicts: **chart definitions (how vehicles, income, and students are counted) beat showcase tidy-ups**. Routes may be parameterised; the 2023 formulae should not change quietly.

## Conventions

| Item | Rule |
| --- | --- |
| Public docs | Traditional Chinese in `README.md`; British English in `docs/README.en-GB.md`. Change both. |
| Dates | `YYYY-MM-DD`, Taipei time |
| Changelog | `CHANGELOG.md` → `## [Unreleased]` (Keep a Changelog 2.0.0) |
| Credits | GitHub handles only: `Lrniey666`, `ejiru4u3`, `zhangkjim` |
| Line endings | LF (`.gitattributes`) |

## Please do not

- Commit `original-data/`, `.env`, `db.sqlite3`, or slides/screenshots that show student numbers
- Put TDX `client_id` / `client_secret` back into source or the database
- Put student numbers or legal names in the footer or README
- Rewrite the analysis formulae for fashion and then call it the 2023 method

Ask first before irreversible git history edits.

## After a change

1. Note it under `CHANGELOG.md` → `## [Unreleased]`
2. If Hero, install, or structure moved, update both READMEs
3. Run `python manage.py test`
