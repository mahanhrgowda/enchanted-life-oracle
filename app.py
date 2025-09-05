import streamlit as st
from datetime import date, time, timedelta, datetime
from math import sin, cos, tan, atan2, radians, degrees, floor, sqrt, fmod
import random
import pandas as pd

PI = 3.14159265358979323846
RADEG = 180.0 / PI
DEGRAD = PI / 180.0

def rev(x):
    return x - floor(x / 360.0) * 360.0

def calculate_d(year, month, day, ut):
    return 367 * year - floor(7 * (year + floor((month + 9) / 12)) / 4) + floor(275 * month / 9) + day - 730530 + ut / 24.0

def calculate_oblecl(d):
    return 23.4393 - 3.563E-7 * d

def calculate_sun(d):
    w = 282.9404 + 4.70935E-5 * d
    e = 0.016709 - 1.151E-9 * d
    M = rev(356.0470 + 0.9856002585 * d)
    E = M + degrees(e * sin(radians(M)) * (1 + e * cos(radians(M))))
    x = cos(radians(E)) - e
    y = sin(radians(E)) * sqrt(1 - e**2)
    r = sqrt(x**2 + y**2)
    v = degrees(atan2(y, x))
    lon = rev(v + w)
    lat = 0
    return lon, lat, r

def calculate_moon(d):
    N = rev(125.1228 - 0.0529538083 * d)
    i = 5.1454
    w = rev(318.0634 + 0.1643573223 * d)
    e = 0.054900
    M = rev(115.3654 + 13.0649929509 * d)
    Msun = rev(356.0470 + 0.9856002585 * d)
    Ls = rev(280.4665 + 0.98564736 * d)
    Lm = rev(N + w + M)
    D = rev(Lm - Ls)
    F = rev(Lm - N)
    lon = Lm + (-1.274 * sin(radians(M - 2*D)) + 0.658 * sin(radians(2*D)) - 0.186 * sin(radians(Msun)) - 0.059 * sin(radians(2*M - 2*D)) - 0.057 * sin(radians(M - 2*D + Msun)) + 0.053 * sin(radians(M + 2*D)) + 0.046 * sin(radians(2*D - Msun)) + 0.041 * sin(radians(M - Msun)) - 0.034 * sin(radians(D)) - 0.031 * sin(radians(M + Msun)) - 0.015 * sin(radians(2*F - 2*D)) - 0.011 * sin(radians(M - 4*D)))
    lon = rev(lon)
    lat = 5.128 * sin(radians(F)) + 0.281 * sin(radians(M + F)) + 0.278 * sin(radians(M - F)) + 0.173 * sin(radians(2*F - 2*D)) + 0.055 * sin(radians(M - D + F)) + 0.046 * sin(radians(M - D - F)) + 0.033 * sin(radians(D + F)) + 0.017 * sin(radians(2*M + F))
    return lon, lat

def get_planet_params(planet):
    if planet == 'mercury':
        return {'N': 48.3313, 'N1': 3.24587E-5, 'i': 7.0047, 'i1': 5.00E-8, 'w': 29.1241, 'w1': 1.01444E-5, 'a': 0.387098, 'e': 0.205635, 'e1': 5.59E-10, 'M': 168.6562, 'M1': 4.0923344368, 'pert': lambda mj, ms, mu, mn: 0}
    elif planet == 'venus':
        return {'N': 76.6799, 'N1': 2.46590E-5, 'i': 3.3946, 'i1': 2.75E-8, 'w': 54.8910, 'w1': 1.38374E-5, 'a': 0.723330, 'e': 0.006773, 'e1': -1.302E-9, 'M': 48.0052, 'M1': 1.6021302244, 'pert': lambda mj, ms, mu, mn: 0}
    elif planet == 'mars':
        return {'N': 49.5574, 'N1': 2.11081E-5, 'i': 1.8497, 'i1': -1.78E-8, 'w': 286.5016, 'w1': 2.92961E-5, 'a': 1.523688, 'e': 0.093405, 'e1': 2.516E-9, 'M': 18.6021, 'M1': 0.5240207766, 'pert': lambda mj, ms, mu, mn: 0}
    elif planet == 'jupiter':
        return {'N': 100.4542, 'N1': 2.76854E-5, 'i': 1.3030, 'i1': -1.557E-7, 'w': 273.8777, 'w1': 1.64505E-5, 'a': 5.20256, 'e': 0.048498, 'e1': 4.469E-9, 'M': 19.8950, 'M1': 0.0830853001, 'pert': lambda mj, ms, mu, mn: -0.332 * sin(radians(2*mj - 5*ms - 67.6)) - 0.056 * sin(radians(2*mj - 2*ms + 21)) + 0.042 * sin(radians(3*mj - 5*ms + 21)) - 0.036 * sin(radians(mj - 2*ms)) + 0.022 * cos(radians(mj - ms)) + 0.023 * sin(radians(2*mj - 3*ms + 52)) - 0.016 * sin(radians(mj - 5*ms - 69))}
    elif planet == 'saturn':
        return {'N': 113.6634, 'N1': 2.38980E-5, 'i': 2.4886, 'i1': -1.081E-7, 'w': 339.3939, 'w1': 2.97661E-5, 'a': 9.55475, 'e': 0.055546, 'e1': -9.499E-9, 'M': 316.9670, 'M1': 0.0334442282, 'pert': lambda mj, ms, mu, mn: 0.812 * sin(radians(2*mj - 5*ms - 67.6)) - 0.229 * cos(radians(2*mj - 4*ms - 2)) + 0.119 * sin(radians(mj - 2*ms - 3)) + 0.046 * sin(radians(2*mj - 6*ms - 69)) + 0.014 * sin(radians(mj - 3*ms + 32))}
    elif planet == 'uranus':
        return {'N': 74.0005, 'N1': 1.3978E-5, 'i': 0.7733, 'i1': 1.9E-8, 'w': 96.6612, 'w1': 3.0565E-5, 'a': 19.18171, 'e': 0.047318, 'e1': 7.45E-9, 'M': 142.5905, 'M1': 0.011725806, 'pert': lambda mj, ms, mu, mn: -0.0426 * sin(radians(ms - 2*mu + 6)) + 0.0313 * sin(radians(2*ms - 2*mu + 21)) - 0.0125 * sin(radians(ms - 2*mu - 8)) + 0.0111 * sin(radians(2*ms - 3*mu + 33)) - 0.0094 * sin(radians(ms - mu + 20))}
    elif planet == 'neptune':
        return {'N': 131.7806, 'N1': 3.0173E-5, 'i': 1.7700, 'i1': -2.55E-7, 'w': 272.8461, 'w1': -6.027E-6, 'a': 30.05826, 'e': 0.008606, 'e1': 2.15E-9, 'M': 260.2471, 'M1': 0.005995147, 'pert': lambda mj, ms, mu, mn: 0.030 * sin(radians(mu - 2*mn + 6)) + 0.011 * sin(radians(mu - mn + 35)) + 0.010 * sin(radians(mu - 3*mn + 33)) + 0.008 * sin(radians(mu - mn + 20))}
    elif planet == 'pluto':
        return {'N': 110.3035, 'N1': -0.01183482 / 36525, 'i': 17.14001, 'i1': 11.07E-6 / 36525, 'w': 224.0689, 'w1': -0.00008234 / 36525, 'a': 39.482116, 'e': 0.2488273, 'e1': 60.30E-6 / 36525, 'M': 238.92881, 'M1': 0.003076325, 'pert': lambda mj, ms, mu, mn: 0}

def calculate_planet_position(d, planet, x_earth, y_earth, z_earth, mj, ms, mu, mn):
    params = get_planet_params(planet)
    N = params['N'] + params['N1'] * d
    i = params['i'] + params['i1'] * d
    w = params['w'] + params['w1'] * d
    a = params['a']
    e = params['e'] + params['e1'] * d
    M = rev(params['M'] + params['M1'] * d)
    pert = params['pert'](mj, ms, mu, mn)
    M = rev(M + pert)
    E = M
    for _ in range(20):
        delta = E - degrees(e * sin(radians(E))) - M
        E -= delta / (1 - e * cos(radians(E)))
        if abs(delta) < 0.0001:
            break
    xv = a * (cos(radians(E)) - e)
    yv = a * sqrt(1 - e**2) * sin(radians(E))
    r = sqrt(xv**2 + yv**2)
    v = degrees(atan2(yv, xv))
    vrad = radians(v + w)
    Nr = radians(N)
    ir = radians(i)
    xh = r * (cos(Nr) * cos(vrad) - sin(Nr) * sin(vrad) * cos(ir))
    yh = r * (sin(Nr) * cos(vrad) + cos(Nr) * sin(vrad) * cos(ir))
    zh = r * sin(vrad) * sin(ir)
    xg = xh + x_earth
    yg = yh + y_earth
    zg = zh + z_earth
    lon = rev(degrees(atan2(yg, xg)))
    lat = degrees(atan2(zg, sqrt(xg**2 + yg**2)))
    return lon, lat, sqrt(xg**2 + yg**2 + zg**2)

def calculate_north_node(d):
    node = rev(125.04452 - 0.05295377 * d)
    return node

def calculate_ascendant(d, lat, lon_deg):
    oblecl = calculate_oblecl(d)
    t = d / 36525
    gmst0 = rev(280.46061837 + 360.98564736629 * d + 0.000387933 * t**2 - t**3 / 38710000)
    gmst = rev(gmst0 + lon_deg)
    ramc = gmst
    sin_e = sin(radians(oblecl))
    cos_e = cos(radians(oblecl))
    tan_gl = tan(radians(lat))
    sin_ramc = sin(radians(ramc))
    cos_ramc = cos(radians(ramc))
    denominator = cos_ramc * cos_e - sin_e * tan_gl * sin_ramc
    if denominator == 0:
        denominator = 1e-10
    asc_lon = degrees(atan2(sin_ramc, denominator))
    if asc_lon < 0:
        asc_lon += 360
    asc_lon = fmod(asc_lon, 360)
    return asc_lon

def get_zodiac_sign(lon):
    signs = ["Aries ♈", "Taurus ♉", "Gemini ♊", "Cancer ♋", "Leo ♌", "Virgo ♍", "Libra ♎", "Scorpio ♏", "Sagittarius ♐", "Capricorn ♑", "Aquarius ♒", "Pisces ♓"]
    return signs[int(lon // 30)]

# New functions for Enchanted Life Oracle

# Simulated Tarot-like deck with emojis
tarot_cards = [
    "The Fool: Embark on a new journey with childlike wonder. 🃏🌟",
    "The Magician: Manifest your desires through will and skill. 🎩✨",
    "The High Priestess: Trust your intuition and inner wisdom. 🌙🔮",
    "The Empress: Nurture creativity and abundance. 👑🌸",
    "The Emperor: Establish structure and authority. 🏰🛡️",
    "The Hierophant: Seek traditional knowledge and guidance. 📜🙏",
    "The Lovers: Embrace choices in relationships and harmony. 💕❤️",
    "The Chariot: Achieve victory through determination. 🏇🏆",
    "Strength: Harness inner courage and patience. 🦁💪",
    "The Hermit: Find solitude for introspection. 🏞️🔦",
    "Wheel of Fortune: Embrace cycles of change. 🎡🔄",
    "Justice: Seek balance and fairness. ⚖️📏",
    "The Hanged Man: Surrender to gain new perspectives. 🙃🌳",
    "Death: Transform and release the old. 💀🦋",
    "Temperance: Find moderation and harmony. 😇🍷",
    "The Devil: Confront shadows and addictions. 😈🔥",
    "The Tower: Face sudden upheaval for renewal. 🏰⚡",
    "The Star: Inspire hope and healing. ⭐💧",
    "The Moon: Navigate illusions and subconscious. 🌕🐺",
    "The Sun: Radiate joy and success. ☀️😊",
    "Judgement: Awaken to rebirth and calling. 📯🌹",
    "The World: Complete cycles with fulfillment. 🌍🏅"
]

# I Ching hexagrams (simplified) with emojis
i_ching_hexagrams = [
    "1: The Creative - Pure yang, initiative and power. 💥🔥",
    "2: The Receptive - Pure yin, devotion and adaptability. 🌏🤲",
    "3: Difficulty at the Beginning - Perseverance through chaos. 🌱⚡",
    "4: Youthful Folly - Learning from inexperience. 👶📚",
    "5: Waiting - Patience in anticipation. ⏳☔",
    "6: Conflict - Seek resolution through compromise. ⚔️🤝",
    "7: The Army - Discipline and organization. 🛡️👥",
    "8: Holding Together - Unity and solidarity. 🤝🌐",
    "9: The Taming Power of the Small - Gentle influence. 🌬️🐦",
    "10: Treading - Careful conduct. 👣🐅",
    "11: Peace - Harmony and prosperity. ☮️🌸",
    "12: Standstill - Stagnation, wait for change. 🛑⏱️",
    "13: Fellowship - Community and cooperation. 👫🔥",
    "14: Possession in Great Measure - Abundance. 💰🌟",
    "15: Modesty - Humility brings success. 🙇🌳",
    "16: Enthusiasm - Inspiration and joy. 🎉⚡",
    "17: Following - Adaptability and guidance. 🐟🌊",
    "18: Work on What Has Been Spoiled - Repair and renewal. 🛠️🍄",
    "19: Approach - Nearing success. 🏞️🌞",
    "20: Contemplation - Observation and insight. 👀🏔️",
    "21: Biting Through - Decisive action. 🦷⚡",
    "22: Grace - Beauty and elegance. 🌸🦋",
    "23: Splitting Apart - Disintegration, yield. 🏔️🍂",
    "24: Return - Renewal after decline. 🔄🌱",
    "25: Innocence - Natural spontaneity. 🐦☁️",
    "26: The Taming Power of the Great - Controlled power. 🏔️🐂",
    "27: Nourishment - Care for self and others. 🍲🗣️",
    "28: Preponderance of the Great - Excess, transition. 🏞️🌊",
    "29: The Abysmal - Danger, repeat perseverance. 🌊🌊",
    "30: The Clinging - Dependence and clarity. 🔥🔥",
    "31: Influence - Attraction and wooing. 🏞️🌊",
    "32: Duration - Endurance and constancy. ⚡🌬️",
    "33: Retreat - Strategic withdrawal. ☁️🏔️",
    "34: The Power of the Great - Vigorous advance. ⚡⚡",
    "35: Progress - Steady advancement. 🔥🌏",
    "36: Darkening of the Light - Concealment. 🌏🔥",
    "37: The Family - Roles and harmony. 🌬️🔥",
    "38: Opposition - Polarity and reconciliation. 🔥🌊",
    "39: Obstruction - Turn inward during difficulty. 🌊🏔️",
    "40: Deliverance - Release from tension. ⚡🌊",
    "41: Decrease - Simplification. 🏔️🌊",
    "42: Increase - Expansion and generosity. 🌬️⚡",
    "43: Breakthrough - Resoluteness. 🌊☁️",
    "44: Coming to Meet - Temptation, caution. ☁️🌬️",
    "45: Gathering Together - Unity in groups. 🌊🌏",
    "46: Pushing Upward - Gradual ascent. 🌏🌬️",
    "47: Oppression - Exhaustion, inner strength. 🌊☁️",
    "48: The Well - Source of sustenance. 🌬️🌊",
    "49: Revolution - Change and renewal. 🌊🔥",
    "50: The Cauldron - Transformation. 🔥🌬️",
    "51: The Arousing - Shock and awakening. ⚡⚡",
    "52: Keeping Still - Meditation and calm. 🏔️🏔️",
    "53: Development - Gradual progress. 🌬️🏔️",
    "54: The Marrying Maiden - Subordination. ⚡🌊",
    "55: Abundance - Peak prosperity. ⚡🔥",
    "56: The Wanderer - Transience. 🔥🏔️",
    "57: The Gentle - Penetration and influence. 🌬️🌬️",
    "58: The Joyous - Encouragement and pleasure. 🌊🌊",
    "59: Dispersion - Dissolving barriers. 🌬️🌊",
    "60: Limitation - Moderation and boundaries. 🌊🌊",
    "61: Inner Truth - Sincerity. 🌬️🌊",
    "62: Preponderance of the Small - Attention to detail. ⚡🏔️",
    "63: After Completion - Order achieved. 🌊🔥",
    "64: Before Completion - Transition. 🔥🌊"
]

# Chakras mapped to planets (simplified) with emojis
chakra_map = {
    'sun': 'Solar Plexus - Personal power 💛🔥',
    'moon': 'Sacral - Emotions 🧡🌊',
    'mercury': 'Throat - Communication 💙🗣️',
    'venus': 'Heart - Love 💚❤️',
    'mars': 'Root - Survival ❤️🌱',
    'jupiter': 'Third Eye - Wisdom 💜👁️',
    'saturn': 'Crown - Spirituality 🤍👑',
    'uranus': 'Third Eye - Intuition 💜🌌',
    'neptune': 'Crown - Transcendence 🤍🌠',
    'pluto': 'Root - Transformation ❤️🦋',
    'ascendant': 'All - Life path 🌈🛤️',
    'north_node': 'All - Destiny 🌟🎯'
}

# Gematria calculation (simple English gematria)
def gematria(name):
    name = name.upper().replace(" ", "")
    value = sum(ord(c) - ord('A') + 1 for c in name if c.isalpha())
    while value > 9:
        value = sum(int(d) for d in str(value))
    return value

# Geomantic flavor based on location (simple hash) with emojis
def geomantic_flavor(lat, lon):
    seed = int(abs(lat) + abs(lon)) % 16
    geomantic_figures = [
        "Via: Path of change. 🛤️🔄",
        "Populus: People and crowds. 👥🌆",
        "Fortuna Major: Greater fortune. 🍀🏆",
        "Fortuna Minor: Lesser fortune. 🌟🥈",
        "Acquisitio: Gain. 💰📈",
        "Amissio: Loss. 😔📉",
        "Albus: White, purity. 🤍🕊️",
        "Rubeus: Red, passion. ❤️🔥",
        "Puer: Boy, impulsiveness. 👦💨",
        "Puella: Girl, harmony. 👧🎶",
        "Conjunctio: Union. 🤝💍",
        "Carcer: Prison, restriction. 🔒🚫",
        "Tristitia: Sorrow. 😢🌧️",
        "Laetitia: Joy. 😄🌈",
        "Caput Draconis: Dragon's head, entry. 🐉🚪",
        "Cauda Draconis: Dragon's tail, exit. 🐲🚪"
    ]
    return geomantic_figures[seed]

# Planetary hour calculation (simplified)
def planetary_hour(birth_time):
    hour = birth_time.hour
    planets = ['saturn', 'jupiter', 'mars', 'sun', 'venus', 'mercury', 'moon'] * 3  # Repeating cycle
    day_planet = planets[(datetime.combine(date.today(), birth_time).weekday() + 1) % 7]
    start_idx = planets.index(day_planet)
    current_planet = planets[(start_idx + hour) % 7]
    return current_planet

# Affirmation generator with emojis
def generate_affirmation(gematria_val, i_ching, chakra):
    colors = ['red ❤️', 'orange 🧡', 'yellow 💛', 'green 💚', 'blue 💙', 'indigo 💜', 'violet 🤍']
    color = colors[(gematria_val - 1) % 7]
    i_ching_desc = i_ching.split('-')[1].strip().lower()
    chakra_name = chakra.split('-')[0].strip().lower()
    return f"Repeat daily: I am a vortex of {color} light, embracing {i_ching_desc} from my {chakra_name} chakra, spinning fortunes from my birth stars. 🌌✨🔮"

# Luck wave generator
def generate_luck_waves(birth_date, lon):
    today = datetime.now().date()
    dates = [today + timedelta(days=i) for i in range(30)]
    echo = int(abs(lon)) % 30
    waves = [sin(radians((i + echo) * 12)) * 50 + 50 for i in range(30)]  # Simple sine wave
    df = pd.DataFrame({'Date': dates, 'Luck Level (%)': waves})
    return df

st.title("Enchanted Life Oracle 🔮✨🌟")

with st.expander("About the Oracle 📖"):
    st.write("""
    This digital oracle fuses cartomancy (tarot-like readings) 🃏, I Ching hexagrams 📜, chakra astrology ⚕️, gematria (numerical values of words) 🔢, and geomancy (earth divination) 🌍 for personalized insights.
    Enter your details to reveal your custom spread, affirmation, and luck timeline! It's designed for fun, self-reflection, and spiritual exploration. Remember, these are symbolic interpretations to inspire you! 🧘💖
    """)

st.header("Enter Your Details 📝✨")
name = st.text_input("Full Name 👤", value="Mahan Ravindra")
birth_date = st.date_input("Birth Date 📅", value=date(1993, 7, 12), min_value=date(1900,1,1), max_value=date(2100,12,31))
birth_time = st.time_input("Birth Time (optional, default noon) ⏰", value=time(12, 26), step=timedelta(minutes=1))
tz_options = [
    "UTC (UTC+0:00)", "IST (UTC+5:30)", "EST (UTC-5:00)", "CST (UTC-6:00)",
    "PST (UTC-8:00)", "MST (UTC-7:00)", "CET (UTC+1:00)", "EET (UTC+2:00)",
    "MSK (UTC+3:00)", "GST (UTC+4:00)", "PKT (UTC+5:00)", "BST (UTC+6:00)",
    "ICT (UTC+7:00)", "CST (UTC+8:00)", "JST (UTC+9:00)", "AEST (UTC+10:00)",
    "BRT (UTC-3:00)", "AST (UTC-4:00)", "AKST (UTC-9:00)", "HST (UTC-10:00)"
]
tz = st.selectbox("Timezone 🌐", options=tz_options, index=1)
lat = st.number_input("Latitude (decimal degrees) 📍", value=13.3159)
lon = st.number_input("Longitude (decimal degrees) 📍", value=75.7730)

def get_tz_offset(tz_str):
    if '(' not in tz_str:
        return 0.0
    offset_part = tz_str.split('(')[1].split(')')[0].replace('UTC', '')
    sign = 1 if '+' in offset_part else -1
    offset_str = offset_part.lstrip('+-')
    parts = offset_str.split(':')
    hours = float(parts[0])
    minutes = float(parts[1]) if len(parts) > 1 else 0.0
    return sign * (hours + minutes / 60)

if st.button("Consult the Oracle 🌟🔍"):
    offset = get_tz_offset(tz)
    ut = birth_time.hour + birth_time.minute / 60 - offset
    d = calculate_d(birth_date.year, birth_date.month, birth_date.day, ut)
    
    mj = rev(19.8950 + 0.0830853001 * d)
    ms = rev(316.9670 + 0.0334442282 * d)
    mu = rev(142.5905 + 0.011725806 * d)
    mn = rev(260.2471 + 0.005995147 * d)
    
    sun_lon, sun_lat, sun_r = calculate_sun(d)
    x_earth = sun_r * cos(radians(sun_lon)) * cos(radians(sun_lat))
    y_earth = sun_r * sin(radians(sun_lon)) * cos(radians(sun_lat))
    z_earth = sun_r * sin(radians(sun_lat))
    
    positions = {}
    positions['sun'] = sun_lon
    moon_lon, moon_lat = calculate_moon(d)
    positions['moon'] = moon_lon
    for p in ['mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']:
        plon, plat, pr = calculate_planet_position(d, p, x_earth, y_earth, z_earth, mj, ms, mu, mn)
        positions[p] = plon
    positions['ascendant'] = calculate_ascendant(d, lat, lon)
    positions['north_node'] = calculate_north_node(d)
    
    # Planetary hour
    ph_planet = planetary_hour(birth_time)
    
    # Gematria
    gem_val = gematria(name)
    
    # Geomantic
    geo_flavor = geomantic_flavor(lat, lon)
    
    # Chakra from planetary hour
    chakra = chakra_map.get(ph_planet, 'Solar Plexus - Power 💛🔥')
    
    # Seed random with gem_val + planetary position
    random.seed(gem_val + int(positions[ph_planet] % 360))
    
    # Draw 3-5 cards
    num_cards = random.randint(3, 5)
    drawn_cards = random.sample(tarot_cards, num_cards)
    
    # Draw I Ching
    i_ching = random.choice(i_ching_hexagrams)
    
    st.subheader("Your Oracle Spread 🃏✨")
    st.write(f"**Geomantic Flavor 🌍🧭:** {geo_flavor}")
    st.write("   *Explanation:* This is derived from your location's latitude and longitude, symbolizing the earth's energy influencing your path. It adds a grounded, divinatory layer to your reading! 🌏🔮")
    
    st.write(f"**Guiding Chakra ⚕️🌈:** {chakra}")
    st.write("   *Explanation:* Based on the planetary hour of your birth time, this chakra highlights the energy center most active for you today. Focus on it for balance and empowerment! 🧘‍♀️💫")
    
    st.write(f"**I Ching Hexagram 📜🀄:** {i_ching}")
    st.write("   *Explanation:* This ancient Chinese oracle provides wisdom on your current situation or future path. Reflect on its message for guidance in decision-making! 🌿🤔")
    
    for i, card in enumerate(drawn_cards):
        reversed = random.choice([True, False])
        orientation = "reversed 🔄" if reversed else "upright ⬆️"
        fun_twist = random.choice([
            "Your life path involves chaotic tea parties with interdimensional beings. 🍵👽😄",
            "Expect unexpected portals to open in your daily routine. 🚪✨🌌",
            "Whispers from ancient stars guide your next coffee choice. ☕🌟🔮",
            "Dance with shadows to unlock hidden treasures. 💃🗝️🕺",
            "A cosmic joke awaits; laugh to ascend! 😂🚀🌠"
        ])
        st.write(f"**Card {i+1} ({orientation}):** {card} - {fun_twist}")
        st.write("   *Explanation:* This card represents a key theme in your life right now. If reversed, it may indicate blocked energy or an internal focus. The fun twist adds a light-hearted, imaginative interpretation to inspire creativity! 🎨🤩")
    
    st.subheader("Personalized Affirmation 🧘‍♂️💬")
    affirmation = generate_affirmation(gem_val, i_ching, chakra)
    st.write(affirmation)
    st.write("   *Explanation:* This affirmation is tailored using your name's gematria value (numerical essence 🔢), I Ching wisdom 📜, and guiding chakra ⚕️. Use it in meditation or daily routines to align your energies and manifest positive changes! 🌈🕊️")
    
    st.subheader("Luck Waves Timeline 📈🍀")
    df = generate_luck_waves(birth_date, lon)
    st.line_chart(df.set_index('Date'))
    st.write("   *Explanation:* This chart predicts 'luck waves' based on your birth date and longitude, using a sinusoidal pattern to simulate cosmic echoes. Peaks indicate favorable times for new ventures; dips suggest caution and reflection. It's symbolic—use it as a fun guide! 📊🔮😊")
    
    st.write("**Final Note:** Remember, this oracle is for entertainment, inspiration, and self-reflection. Balance these insights with your own intuition and critical thinking. May your journey be enchanted! 🧠💖🌟")
