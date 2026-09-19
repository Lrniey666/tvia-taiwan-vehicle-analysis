# 架構

語言：[繁體中文](architecture.md) · [English (UK)](README.en-GB.md)

## 模組

```text
browser  →  dashboard.views  →  analysis.*  →  dashboard.models  →  SQLite
manage.py fetch_tdx  →  fetchers.datasets  →  fetchers.tdx  →  TDX
                                          ↘  dashboard.models
```

- `config.settings` 是唯一讀 `.env` 的地方（Django 密鑰、DEBUG、ALLOWED_HOSTS）。TDX 憑證由 `fetchers.tdx` 直接讀環境變數，**模型裡沒有 API key 欄位**。
- `analysis` 只在請求週期內跑 ORM。2023 版每個 `.py` 開頭 `sys.path.append('C:\\python-10')` 再 `django.setup()`，展示倉拿掉了。
- 四個圖表族各一個 view + 一個模板。城市與車種走 URL 參數，不再有 `vehicle_growing_up_TP.html` 到 `_KH.html` 七份拷貝。

## 路由

| 名稱 | 路徑 | 聚合 |
| --- | --- | --- |
| `index` | `/` | 無 |
| `ranking` | `/rankings/`、`/rankings/<kind>/` | `analysis.vehicles.ranking` |
| `growth` | `/growth/`、`/growth/<city>/` | `totals_by_year` + `income_totals_by_year` |
| `income` | `/income/`、`/income/<kind>/` | `per_100k_vehicles` + `monthly_pci` |
| `students` | `/students/<kind>/` | `vehicle_share` + `student_share` |

`kind`：`all` / `car` / `scooter` / `truck` / `bus`（視圖表族而定）。  
`city`：`taipei`、`new-taipei`、`taoyuan`、`taichung`、`tainan`、`kaohsiung`。

## 相對 2023 繳交檔

| 2023 | 2026 展示倉 |
| --- | --- |
| 專案名 `python10`、app `mysite` | `config`、`dashboard` |
| TDX key 寫在 fetcher 與 `Tdx_api` 表 | `.env` → `fetchers.tdx` |
| `Data_masage`（拼字） | `analysis` |
| 17 張幾乎一樣的 chart HTML | 4 張 |
| `ALLOWED_HOSTS = ['*']`、DEBUG 永遠開 | `.env` |
| 選單有「管理後台」 | 拿掉 |
| Footer 學號與姓名 | GitHub 帳號 |
| `requirements.txt` 是 Anaconda dump | Django + dotenv + requests |

分析公式（誰算小汽車、收入單位、對齊較舊年份）沒有改。
