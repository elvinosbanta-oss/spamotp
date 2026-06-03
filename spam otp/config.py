# Konfigurasi - MODE REAL (Kirim beneran)
DEBUG_MODE = False  # False = kirim real ke nomor target

# Delay antar request (detik) - biar gak kena ban
DELAY_BETWEEN_REQUESTS = 2

# Timeout per request
REQUEST_TIMEOUT = 15

# User Agent untuk random
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-A536E) AppleWebKit/537.36",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36",
    "Mozilla/5.0 (Linux; Android 10; POCO F1) AppleWebKit/537.36",
]

# Warna untuk console log
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'