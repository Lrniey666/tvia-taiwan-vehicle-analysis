# 貢獻指南

語言：[繁體中文](CONTRIBUTING.md) · [English](docs/CONTRIBUTING.en.md)

這是 2023 課程網站的封存 Showcase Repository。歡迎修文件、補空狀態、改圖表可讀性。請先當歷史作品看，再動手。

## 動工前

1. 讀根目錄 [`README.md`](README.md) 與 [`docs/README.md`](docs/README.md)。
2. 金鑰只放 `.env`。TDX 憑證、Django `SECRET_KEY`、後台帳號都不要進 git。
3. 衝突時：**圖表定義（車輛／收入／學生怎麼算）> Showcase Repository 整理**。整理時可以參數化路由，但不要默默改分析口徑。

## 慣例

| 項目 | 約定 |
| --- | --- |
| 對外說明 | 繁中在 `README.md`；英文在 `docs/README.en.md`，兩邊一起改 |
| 日期 | `YYYY-MM-DD`，台北時間 |
| 變更紀錄 | `CHANGELOG.md` 的 `## [Unreleased]`（Keep a Changelog 2.0.0） |
| 組員具名 | 用 GitHub 帳號：`Lrniey666`、`ejiru4u3`、`zhangkjim` |
| 換行 | LF（`.gitattributes`） |

## 請不要

- 提交 `original-data/`、`.env`、`db.sqlite3`、含學號的簡報或截圖
- 把 TDX `client_id` / `client_secret` 寫回原始碼或資料庫
- 在頁尾或 README 放學號、真實姓名
- 為了「比較現代」重寫分析公式卻聲稱這是 2023 原口徑

不可逆的動作（force push、把原料庫打進歷史）請先問。

## 改完必做

1. Notable 變更寫進 `CHANGELOG.md` → `## [Unreleased]`
2. 動到 Hero／安裝／結構 → 繁中與英文 README 一起改
3. `python manage.py test`
