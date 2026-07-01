# -*- coding: utf-8 -*-
"""
Distance calculator from Eagle Environmental office.
Office: 16 Woodland St W, Boylston, MA
Coordinates: 42.3473, -71.7162
Usage:
  python ma_towns.py "Worcester"        → prints miles
  python ma_towns.py --ring "Worcester" → prints ring label
"""
import math, sys

OFFICE = (42.3473, -71.7162)  # Boylston, MA

def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8  # Earth radius in miles
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def miles_from_office(lat, lon):
    return haversine(OFFICE[0], OFFICE[1], lat, lon)

def ring_label(miles):
    if miles <= 20:  return "0–20 miles"
    if miles <= 35:  return "20–35 miles"
    if miles <= 50:  return "35–50 miles"
    return "50+ miles"

# (lat, lon) for MA towns and common surrounding areas
TOWNS = {
    # --- Core / near office ---
    "Boylston":          (42.3473, -71.7162),
    "West Boylston":     (42.3637, -71.7801),
    "Worcester":         (42.2626, -71.8023),
    "Shrewsbury":        (42.2959, -71.7190),
    "Northborough":      (42.3190, -71.6454),
    "Westborough":       (42.2695, -71.6162),
    "Southborough":      (42.3048, -71.5237),
    "Grafton":           (42.2068, -71.6829),
    "Millbury":          (42.1934, -71.7679),
    "Auburn":            (42.1984, -71.8354),
    "Holden":            (42.3548, -71.8573),
    "Paxton":            (42.3126, -71.9298),
    "Sterling":          (42.4337, -71.7718),
    "Clinton":           (42.4154, -71.6829),
    "Berlin":            (42.3812, -71.6373),
    "Princeton":         (42.4484, -71.8768),
    "Rutland":           (42.3773, -71.9590),
    "Barre":             (42.4229, -72.1073),
    "Hardwick":          (42.3548, -72.1862),
    "Hubbardston":       (42.4848, -71.9818),
    "New Braintree":     (42.3237, -72.1318),
    # --- 20-35 mile ring ---
    "Marlborough":       (42.3487, -71.5523),
    "Hudson":            (42.3923, -71.5662),
    "Stow":              (42.4312, -71.5048),
    "Acton":             (42.4848, -71.4329),
    "Maynard":           (42.4312, -71.4579),
    "Framingham":        (42.2793, -71.4162),
    "Natick":            (42.2837, -71.3468),
    "Ashland":           (42.2612, -71.4637),
    "Hopkinton":         (42.2287, -71.5273),
    "Holliston":         (42.2009, -71.4245),
    "Milford":           (42.1398, -71.5134),
    "Medway":            (42.1548, -71.3940),
    "Millis":            (42.1673, -71.3579),
    "Medfield":          (42.1868, -71.3062),
    "Walpole":           (42.1573, -71.2495),
    "Leominster":        (42.5251, -71.7600),
    "Fitchburg":         (42.5834, -71.8023),
    "Gardner":           (42.5751, -71.9984),
    "Westminster":       (42.5487, -71.9062),
    "Townsend":          (42.6737, -71.7079),
    "Lunenburg":         (42.5834, -71.7218),
    "Ayer":              (42.5612, -71.5940),
    "Groton":            (42.6112, -71.5773),
    "Pepperell":         (42.6673, -71.5884),
    "Shirley":           (42.5451, -71.6454),
    "Lancaster":         (42.4534, -71.6818),
    "Concord":           (42.4604, -71.3495),
    "Sudbury":           (42.3837, -71.4162),
    "Wayland":           (42.3612, -71.3607),
    "Weston":            (42.3668, -71.3023),
    "Wellesley":         (42.2968, -71.2929),
    "Needham":           (42.2793, -71.2340),
    "Upton":             (42.1762, -71.5984),
    "Mendon":            (42.1009, -71.5523),
    "Hopedale":          (42.1298, -71.5523),
    "Uxbridge":          (42.0762, -71.6329),
    "Douglas":           (42.0523, -71.7468),
    "Sutton":            (42.1423, -71.7607),
    "Oxford":            (42.1184, -71.8634),
    "Charlton":          (42.1348, -71.9718),
    "Sturbridge":        (42.1023, -72.0795),
    "Webster":           (42.0523, -71.8773),
    "Dudley":            (42.0437, -71.9256),
    "Southbridge":       (42.0751, -72.0334),
    "Spencer":           (42.2437, -71.9929),
    "Northbridge":       (42.1512, -71.6579),
    # --- 35-50 mile ring ---
    "Waltham":           (42.3765, -71.2356),
    "Watertown":         (42.3668, -71.1829),
    "Belmont":           (42.3957, -71.1784),
    "Lexington":         (42.4473, -71.2245),
    "Arlington":         (42.4154, -71.1565),
    "Winchester":        (42.4523, -71.1384),
    "Woburn":            (42.4793, -71.1523),
    "Burlington":        (42.5048, -71.1954),
    "Billerica":         (42.5587, -71.2690),
    "Chelmsford":        (42.5998, -71.3673),
    "North Chelmsford":  (42.6312, -71.3890),
    "Lowell":            (42.6334, -71.3162),
    "Tewksbury":         (42.6112, -71.2340),
    "Wilmington":        (42.5451, -71.1662),
    "Reading":           (42.5257, -71.0954),
    "Wakefield":         (42.5062, -71.0723),
    "Stoneham":          (42.4812, -71.0995),
    "Malden":            (42.4251, -71.0662),
    "Medford":           (42.4195, -71.1062),
    "Somerville":        (42.3876, -71.0995),
    "Cambridge":         (42.3736, -71.1097),
    "Boston":            (42.3601, -71.0589),
    "Brookline":         (42.3318, -71.1212),
    "Newton":            (42.3370, -71.2092),
    "Dedham":            (42.2429, -71.1662),
    "Westwood":          (42.2168, -71.2134),
    "Norwood":           (42.1945, -71.1995),
    "Canton":            (42.1612, -71.1440),
    "Stoughton":         (42.1251, -71.1023),
    "Randolph":          (42.1623, -71.0440),
    "Milton":            (42.2512, -71.0662),
    "Quincy":            (42.2529, -71.0023),
    "Braintree":         (42.2040, -71.0023),
    "Weymouth":          (42.2212, -70.9440),
    "Hingham":           (42.2423, -70.8901),
    "Norwell":           (42.1623, -70.8729),
    "Hanover":           (42.1123, -70.8134),
    "Pembroke":          (42.0662, -70.7984),
    "Cohasset":          (42.2401, -70.8051),
    "Scituate":          (42.1973, -70.7273),
    "Marshfield":        (42.0912, -70.7062),
    "Holbrook":          (42.1487, -71.0134),
    "Avon":              (42.1262, -71.0329),
    "Abington":          (42.1048, -70.9440),
    "Rockland":          (42.1287, -70.9162),
    "Brockton":          (42.0834, -71.0184),
    "Easton":            (42.0262, -71.1245),
    "Attleboro":         (41.9445, -71.2856),
    "North Attleboro":   (41.9762, -71.3273),
    "Plainville":        (42.0173, -71.3329),
    "Norton":            (41.9723, -71.1856),
    "Mansfield":         (42.0312, -71.2190),
    "Foxborough":        (42.0651, -71.2440),
    "Wrentham":          (42.0548, -71.3495),
    "Franklin":          (42.0834, -71.3968),
    "Bellingham":        (42.0848, -71.4718),
    "Milford":           (42.1398, -71.5134),
    "Chestnut Hill":     (42.3237, -71.1662),
    "Jamaica Plain":     (42.3073, -71.1134),
    "Melrose":           (42.4562, -71.0607),
    "Chelsea":           (42.3918, -71.0329),
    "Revere":            (42.4084, -71.0118),
    "Winthrop":          (42.3737, -70.9801),
    "Everett":           (42.4084, -71.0534),
    # --- 50+ mile ring ---
    "Lynn":              (42.4668, -70.9495),
    "Salem":             (42.5195, -70.8967),
    "Beverly":           (42.5584, -70.8801),
    "Peabody":           (42.5279, -70.9290),
    "Danvers":           (42.5751, -70.9301),
    "Marblehead":        (42.4998, -70.8579),
    "Swampscott":        (42.4751, -70.9084),
    "Gloucester":        (42.6154, -70.6606),
    "Rockport":          (42.6556, -70.6201),
    "Ipswich":           (42.6793, -70.8418),
    "Newburyport":       (42.8126, -70.8773),
    "Amesbury":          (42.8584, -70.9301),
    "Salisbury":         (42.8401, -70.8606),
    "Haverhill":         (42.7762, -71.0773),
    "Lawrence":          (42.7070, -71.1634),
    "Methuen":           (42.7262, -71.1912),
    "Andover":           (42.6584, -71.1384),
    "North Andover":     (42.6987, -71.1329),
    "Bradford":          (42.7648, -71.0773),
    "Georgetown":        (42.7237, -71.0001),
    "Groveland":         (42.7612, -71.0329),
    "Newbury":           (42.7762, -70.8773),
    "Rowley":            (42.7237, -70.8773),
    "Topsfield":         (42.6384, -70.9440),
    "Boxford":           (42.6884, -71.0001),
    "Middleton":         (42.5959, -71.0107),
    "Hamilton":          (42.6173, -70.8690),
    "Wenham":            (42.6034, -70.8884),
    "West Newbury":      (42.8012, -71.1329),
    "Merrimac":          (42.8362, -71.0023),
    "Byfield":           (42.7512, -70.9301),
    "Duxbury":           (42.0423, -70.6690),
    "Kingston":          (41.9837, -70.7229),
    "Plymouth":          (41.9584, -70.6673),
    "Wareham":           (41.7623, -70.7134),
    "Middleborough":     (41.8887, -70.9162),
    "Lakeville":         (41.8412, -70.9551),
    "Halifax":           (41.9912, -70.8579),
    "Hanson":            (42.0423, -70.8690),
    "Whitman":           (42.0812, -70.9301),
    "Pembroke":          (42.0662, -70.7984),
    "Bourne":            (41.7437, -70.5551),
    "Sandwich":          (41.7598, -70.4940),
    "Mashpee":           (41.6337, -70.4801),
    "Falmouth":          (41.5512, -70.6134),
    "Barnstable":        (41.7001, -70.2995),
    "Hyannis":           (41.6512, -70.2801),
    "Yarmouth":          (41.7062, -70.2301),
    "Dennis":            (41.7337, -70.1940),
    "Harwich":           (41.6887, -70.0634),
    "Chatham":           (41.6784, -69.9612),
    "Orleans":           (41.7887, -69.9912),
    "Eastham":           (41.8337, -69.9762),
    "Wellfleet":         (41.9262, -70.0273),
    "Truro":             (42.0162, -70.0551),
    "Provincetown":      (42.0512, -70.1856),
    "Brewster":          (41.7587, -70.0801),
    "Mashpee":           (41.6337, -70.4801),
    # --- NH / RI ---
    "Richmond":          (41.4823, -71.6412),  # RI
    "Nashua":            (42.7654, -71.4676),  # NH
    "Manchester":        (42.9956, -71.4548),  # NH
}

def get_ring(town_name):
    """Return (miles, ring_label) for a town name. Case-insensitive."""
    key = town_name.strip().title()
    # Try exact match first, then partial
    if key in TOWNS:
        lat, lon = TOWNS[key]
    else:
        # Try case-insensitive search
        matches = [k for k in TOWNS if k.lower() == town_name.lower().strip()]
        if matches:
            lat, lon = TOWNS[matches[0]]
        else:
            return None, "Unknown"
    m = miles_from_office(lat, lon)
    return round(m, 1), ring_label(m)

if __name__ == "__main__":
    mode = "--ring" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        town = " ".join(args)
        miles, ring = get_ring(town)
        if miles:
            print(f"{town}: {miles} miles → {ring}")
        else:
            print(f"{town}: not found")
    else:
        # Print all towns sorted by distance
        results = []
        for t, (lat, lon) in TOWNS.items():
            m = miles_from_office(lat, lon)
            results.append((m, t))
        for m, t in sorted(results):
            print(f"{m:5.1f} mi  {ring_label(m):15s}  {t}")
