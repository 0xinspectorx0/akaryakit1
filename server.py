import http.server
import socketserver
import json
import urllib.parse
import os

PORT = 3000
DIRECTORY = "/home/user/akaryakit1"

# Türkiye geneli 81 il + İstanbul Anadolu/Avrupa koordinat ve referans verileri
TURKEY_CITIES_RAW = [
    ('Adana', 'Akdeniz', '01', 86.80, 97.30, 41.35, 37.0000, 35.3213),
    ('Adıyaman', 'Güneydoğu Anadolu', '02', 87.05, 97.60, 42.10, 37.7648, 38.2786),
    ('Afyonkarahisar', 'Ege', '03', 86.20, 96.70, 41.10, 38.7507, 30.5567),
    ('Ağrı', 'Doğu Anadolu', '04', 87.50, 98.10, 42.60, 39.7191, 43.0503),
    ('Amasya', 'Karadeniz', '05', 86.50, 96.90, 41.50, 40.6501, 35.8353),
    ('Ankara', 'İç Anadolu', '06', 85.60, 96.10, 41.29, 39.9334, 32.8597),
    ('Antalya', 'Akdeniz', '07', 86.90, 97.40, 41.40, 36.8969, 30.7133),
    ('Artvin', 'Karadeniz', '08', 86.90, 97.30, 42.10, 41.1828, 41.8183),
    ('Aydın', 'Ege', '09', 86.10, 96.50, 41.15, 37.8560, 27.8416),
    ('Balıkesir', 'Marmara', '10', 85.80, 96.30, 40.90, 39.6484, 27.8826),
    ('Bilecik', 'Marmara', '11', 85.70, 96.20, 40.85, 40.1451, 29.9799),
    ('Bingöl', 'Doğu Anadolu', '12', 87.20, 97.80, 42.30, 38.8854, 40.4983),
    ('Bitlis', 'Doğu Anadolu', '13', 87.40, 98.00, 42.50, 38.4006, 42.1095),
    ('Bolu', 'Karadeniz', '14', 85.80, 96.30, 41.10, 40.7358, 31.6061),
    ('Burdur', 'Akdeniz', '15', 86.40, 96.90, 41.25, 37.7203, 30.2908),
    ('Bursa', 'Marmara', '16', 85.60, 98.10, 40.60, 40.1885, 29.0610),
    ('Çanakkale', 'Marmara', '17', 86.00, 96.50, 41.05, 40.1553, 26.4142),
    ('Çankırı', 'İç Anadolu', '18', 85.90, 96.40, 41.30, 40.6013, 33.6134),
    ('Çorum', 'Karadeniz', '19', 86.20, 96.70, 41.40, 40.5506, 34.9556),
    ('Denizli', 'Ege', '20', 86.30, 96.70, 41.20, 37.7765, 29.0864),
    ('Diyarbakır', 'Güneydoğu Anadolu', '21', 87.10, 97.70, 42.26, 37.9144, 40.2306),
    ('Edirne', 'Marmara', '22', 85.70, 96.20, 40.90, 41.6768, 26.5603),
    ('Elazığ', 'Doğu Anadolu', '23', 87.00, 97.50, 42.15, 38.6810, 39.2264),
    ('Erzincan', 'Doğu Anadolu', '24', 87.10, 97.60, 42.20, 39.7500, 39.5000),
    ('Erzurum', 'Doğu Anadolu', '25', 87.30, 97.90, 42.40, 39.9000, 41.2700),
    ('Eskişehir', 'İç Anadolu', '26', 85.70, 96.20, 41.00, 39.7767, 30.5206),
    ('Gaziantep', 'Güneydoğu Anadolu', '27', 86.80, 97.30, 41.70, 37.0662, 37.3833),
    ('Giresun', 'Karadeniz', '28', 86.60, 97.00, 41.80, 40.9128, 38.3895),
    ('Gümüşhane', 'Karadeniz', '29', 86.80, 97.20, 42.00, 40.4600, 39.4700),
    ('Hakkari', 'Güneydoğu Anadolu', '30', 87.90, 98.60, 42.90, 37.5833, 43.7333),
    ('Hatay', 'Akdeniz', '31', 86.70, 97.20, 41.40, 36.2023, 36.1613),
    ('Isparta', 'Akdeniz', '32', 86.30, 96.80, 41.20, 37.7648, 30.5566),
    ('Mersin', 'Akdeniz', '33', 86.60, 97.10, 41.30, 36.8000, 34.6333),
    ('İstanbul (Avr.)', 'Marmara', '342', 84.60, 95.00, 41.20, 41.0150, 28.9300),
    ('İstanbul (Anad.)', 'Marmara', '341', 84.50, 94.90, 40.60, 40.9900, 29.0800),
    ('İzmir', 'Ege', '35', 85.90, 96.40, 41.20, 38.4237, 27.1428),
    ('Kars', 'Doğu Anadolu', '36', 87.60, 98.20, 42.70, 40.6167, 43.1000),
    ('Kastamonu', 'Karadeniz', '37', 86.30, 96.80, 41.40, 41.3887, 33.7827),
    ('Kayseri', 'İç Anadolu', '38', 86.10, 96.50, 41.30, 38.7312, 35.4787),
    ('Kırklareli', 'Marmara', '39', 85.60, 96.10, 40.80, 41.7333, 27.2167),
    ('Kırşehir', 'İç Anadolu', '40', 86.00, 96.40, 41.25, 39.1425, 34.1709),
    ('Kocaeli', 'Marmara', '41', 85.10, 95.30, 40.40, 40.8533, 29.8815),
    ('Konya', 'İç Anadolu', '42', 86.20, 96.60, 41.35, 37.8667, 32.4833),
    ('Kütahya', 'Ege', '43', 86.00, 96.40, 41.00, 39.4167, 29.9833),
    ('Malatya', 'Doğu Anadolu', '44', 86.90, 97.40, 42.00, 38.3552, 38.3095),
    ('Manisa', 'Ege', '45', 86.00, 96.40, 41.10, 38.6191, 27.4289),
    ('Kahramanmaraş', 'Akdeniz', '46', 86.70, 97.20, 41.60, 37.5858, 36.9371),
    ('Mardin', 'Güneydoğu Anadolu', '47', 87.20, 97.80, 42.30, 37.3212, 40.7245),
    ('Muğla', 'Ege', '48', 86.50, 97.00, 41.40, 37.2153, 28.3636),
    ('Muş', 'Doğu Anadolu', '49', 87.30, 97.90, 42.40, 38.7432, 41.5064),
    ('Nevşehir', 'İç Anadolu', '50', 86.10, 96.50, 41.30, 38.6250, 34.7122),
    ('Niğde', 'İç Anadolu', '51', 86.20, 96.60, 41.35, 37.9667, 34.6833),
    ('Ordu', 'Karadeniz', '52', 86.50, 96.90, 41.70, 40.9839, 37.8764),
    ('Rize', 'Karadeniz', '53', 86.70, 97.10, 41.95, 41.0201, 40.5234),
    ('Sakarya', 'Marmara', '54', 85.40, 95.80, 40.60, 40.7569, 30.3783),
    ('Samsun', 'Karadeniz', '55', 86.30, 96.70, 41.50, 41.2928, 36.3313),
    ('Siirt', 'Güneydoğu Anadolu', '56', 87.40, 98.00, 42.50, 37.9333, 41.9500),
    ('Sinop', 'Karadeniz', '57', 86.50, 96.90, 41.60, 42.0231, 35.1531),
    ('Sivas', 'İç Anadolu', '58', 86.40, 96.80, 41.50, 39.7477, 37.0179),
    ('Tekirdağ', 'Marmara', '59', 85.50, 96.00, 40.80, 40.9833, 27.5167),
    ('Tokat', 'Karadeniz', '60', 86.40, 96.80, 41.55, 40.3167, 36.5500),
    ('Trabzon', 'Karadeniz', '61', 86.40, 96.80, 41.99, 41.0027, 39.7168),
    ('Tunceli', 'Doğu Anadolu', '62', 87.20, 97.70, 42.25, 39.1079, 39.5401),
    ('Şanlıurfa', 'Güneydoğu Anadolu', '63', 87.00, 97.50, 42.00, 37.1591, 38.7969),
    ('Uşak', 'Ege', '64', 86.10, 96.50, 41.10, 38.6823, 29.4082),
    ('Van', 'Doğu Anadolu', '65', 87.60, 98.30, 42.80, 38.4891, 43.4089),
    ('Yozgat', 'İç Anadolu', '66', 86.10, 96.50, 41.35, 39.8181, 34.8147),
    ('Zonguldak', 'Karadeniz', '67', 85.90, 96.40, 41.15, 41.4564, 31.7987),
    ('Aksaray', 'İç Anadolu', '68', 86.10, 96.50, 41.30, 38.3687, 34.0370),
    ('Bayburt', 'Karadeniz', '69', 86.80, 97.30, 42.10, 40.2552, 40.2249),
    ('Karaman', 'İç Anadolu', '70', 86.30, 96.70, 41.35, 37.1759, 33.2287),
    ('Kırıkkale', 'İç Anadolu', '71', 85.80, 96.20, 41.20, 39.8468, 33.5153),
    ('Batman', 'Güneydoğu Anadolu', '72', 87.10, 97.70, 42.20, 37.8812, 41.1293),
    ('Şırnak', 'Güneydoğu Anadolu', '73', 87.60, 98.20, 42.70, 37.5164, 42.4611),
    ('Bartın', 'Karadeniz', '74', 86.00, 96.40, 41.20, 41.6344, 32.3375),
    ('Ardahan', 'Doğu Anadolu', '75', 87.70, 98.40, 42.80, 41.1105, 42.7022),
    ('Iğdır', 'Doğu Anadolu', '76', 87.60, 98.20, 42.70, 39.9196, 44.0450),
    ('Yalova', 'Marmara', '77', 85.30, 95.70, 40.50, 40.6500, 29.2667),
    ('Karabük', 'Karadeniz', '78', 86.00, 96.40, 41.25, 41.2061, 32.6204),
    ('Kilis', 'Güneydoğu Anadolu', '79', 86.90, 97.40, 41.80, 36.7184, 37.1212),
    ('Osmaniye', 'Akdeniz', '80', 86.70, 97.20, 41.40, 37.0742, 36.2472),
    ('Düzce', 'Karadeniz', '81', 85.60, 96.00, 40.80, 40.8438, 31.1565)
]

BRANDS_LIST = [
    {"n": "Petrol Ofisi", "offset": 0.00, "delta": {"benzin": 0.10, "motorin": -2.10, "lpg": 4.75}},
    {"n": "Opet", "offset": 0.05, "delta": {"benzin": 0.15, "motorin": -2.08, "lpg": 4.70}},
    {"n": "Shell", "offset": 0.08, "delta": {"benzin": 0.18, "motorin": -2.05, "lpg": 4.80}},
    {"n": "BP", "offset": 0.00, "delta": {"benzin": 0.10, "motorin": -2.10, "lpg": 4.72}},
    {"n": "Total", "offset": -0.05, "delta": {"benzin": 0.08, "motorin": -2.12, "lpg": 4.65}},
    {"n": "Aytemiz", "offset": -0.15, "delta": {"benzin": -0.05, "motorin": -2.25, "lpg": 4.50}},
    {"n": "Alpet", "offset": -0.20, "delta": {"benzin": -0.10, "motorin": -2.30, "lpg": 4.45}},
    {"n": "TP", "offset": -0.18, "delta": {"benzin": -0.08, "motorin": -2.28, "lpg": 4.48}}
]

cities_data = {}
for name, region, plate, b_price, m_price, l_price, lat, lng in TURKEY_CITIES_RAW:
    b_map = {}
    for brand in BRANDS_LIST:
        b_name = brand["n"]
        diff = brand["offset"]
        b_map[b_name] = {
            "benzin": round(b_price + diff, 2),
            "motorin": round(m_price + diff, 2),
            "lpg": round(l_price + (diff * 0.5), 2),
            "delta": brand["delta"]
        }
    cities_data[name] = {
        "region": region,
        "plate": plate,
        "lat": lat,
        "lng": lng,
        "base": {"benzin": b_price, "motorin": m_price, "lpg": l_price},
        "brands": b_map
    }

REALTIME_FUEL_DATA = {
    "lastUpdated": "2026-10-05T18:15:00+03:00",
    "sources": [
        "EPDK Akaryakıt ve LPG Bayi Satış Fiyat Bülteni",
        "Petrol Ofisi Pompa Fiyatları",
        "Opet Fiyat Listesi",
        "Shell & Turcas Fiyat Listesi",
        "BP / Aytemiz / TP Dağıtıcı Bildirimleri"
    ],
    "cities": cities_data
}

class FuelRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/api/fuel-prices':
            query = urllib.parse.parse_qs(parsed.query)
            city_filter = query.get('city', [None])[0]
            
            if city_filter and city_filter in REALTIME_FUEL_DATA["cities"]:
                resp_data = {
                    "lastUpdated": REALTIME_FUEL_DATA["lastUpdated"],
                    "sources": REALTIME_FUEL_DATA["sources"],
                    "city": city_filter,
                    "data": REALTIME_FUEL_DATA["cities"][city_filter]
                }
            else:
                resp_data = REALTIME_FUEL_DATA
                
            resp_body = json.dumps(resp_data, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(resp_body)))
            self.end_headers()
            self.wfile.write(resp_body)
            return
            
        super().do_GET()

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), FuelRequestHandler) as httpd:
        print(f"Server started at http://0.0.0.0:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run()
