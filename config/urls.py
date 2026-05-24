# Базовые URL стендов. Переопределение через переменную окружения SCOOTER_BASE_URL.

import os
from urllib.parse import urlparse

BASE_URL = os.getenv("SCOOTER_BASE_URL", "https://qa-scooter.praktikum-services.ru/")
SITE_HOST = urlparse(BASE_URL).netloc
