"""Taiwan city names used by TDX URLs and the six-municipality charts."""

TDX_CITIES = [
    ("Taipei", "臺北市"),
    ("NewTaipei", "新北市"),
    ("Taoyuan", "桃園市"),
    ("Taichung", "臺中市"),
    ("Tainan", "臺南市"),
    ("Kaohsiung", "高雄市"),
    ("Keelung", "基隆市"),
    ("Hsinchu", "新竹市"),
    ("HsinchuCounty", "新竹縣"),
    ("MiaoliCounty", "苗栗縣"),
    ("ChanghuaCounty", "彰化縣"),
    ("NantouCounty", "南投縣"),
    ("YunlinCounty", "雲林縣"),
    ("Chiayi", "嘉義市"),
    ("ChiayiCounty", "嘉義縣"),
    ("PingtungCounty", "屏東縣"),
    ("YilanCounty", "宜蘭縣"),
    ("HualienCounty", "花蓮縣"),
    ("TaitungCounty", "臺東縣"),
    ("PenghuCounty", "澎湖縣"),
    ("KinmenCounty", "金門縣"),
    ("LienchiangCounty", "連江縣"),
]

SIX_CITIES = ["臺北市", "新北市", "桃園市", "臺中市", "臺南市", "高雄市"]

CITY_SLUGS = {
    "taipei": "臺北市",
    "new-taipei": "新北市",
    "taoyuan": "桃園市",
    "taichung": "臺中市",
    "tainan": "臺南市",
    "kaohsiung": "高雄市",
}

SLUG_BY_CITY = {name: slug for slug, name in CITY_SLUGS.items()}
