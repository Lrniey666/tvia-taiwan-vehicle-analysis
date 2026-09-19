# 資料來源

圖表數字來自交通部 [Transport Data eXchange (TDX)](https://tdx.transportdata.tw/) 進階 API「社經資料」。本 Repository 不重新散布 TDX 的原始 JSON；示範 fixture 只含聚合後寫進 SQLite 的列。

## 端點

基底：`https://tdx.transportdata.tw/api/advanced/v1/SocialEconomic`

| 資料集 | 路徑 | 模型 |
| --- | --- | --- |
| 家戶車輛 | `/HouseholdVehicleOwnership/Year/{year}/City/{English}` | `VehicleCount` |
| 家戶收入 | `/HouseholdIncome/Year/{year}/City/{English}` | `HouseholdIncome` |
| 大專學生 | `/StudentStatus/Year/{year}/City/{English}?Type=大專校院` | `StudentStatus` |
| 鄉鎮人口 | `/PopulationStats/Year/{year}/City/{English}/Town` | `PopulationStat` |

驗證：OAuth2 client-credentials，token URL 在 `config.settings.TDX_AUTH_URL`。Client Id / Secret **只**從環境變數讀。

英文縣市名見 `analysis.cities.TDX_CITIES`（例如 `NewTaipei`、`LienchiangCounty`）。

## 單位與口徑

| 欄位 | 單位／定義 |
| --- | --- |
| `VehicleCount.value` | 輛 |
| `HouseholdIncome.total` | 百萬元 |
| 人均月收入 | `total × 1_000_000 / 人口 / 12`，四捨五入到元 |
| 每十萬人車輛 | `車輛 / 人口 × 100000` |
| 學生比例 | 大專學生人數 / 該市人口 |
| 小汽車佔車輛 | `小客車` / 全部車種（不含把小貨車算進分子，除非圖表註明） |

成長圖車輛取每年 **12 月**，以便對上年資料。

## 年份對齊

收入、學生、人口的更新速度不同。六都結構圖取兩邊最新年份的 **較小值**，避免 2022 的車去對 2021 的所得。排行圖不對齊收入，只用車輛表自己的最新年月。

示範 fixture 來自 2023 作業庫（匯入時已去掉 API 表與使用者表）：

| 表 | 約略列數 | 年份 |
| --- | --- | --- |
| 縣市 | 22 | — |
| 車輛 | ~11 000 | 2016–2023 |
| 家戶收入 | ~100 | 2016–2021 |
| 學生 | ~400 | 2020–2022 |
| 人口（鄉鎮） | ~10 000 | 2016–2022 |
