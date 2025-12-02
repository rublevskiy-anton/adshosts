#!/usr/bin/env python3
import re
import requests

# Источник: обычный ruadlist+easylist
SRC_URL = "https://easylist-downloads.adblockplus.org/ruadlist+easylist.txt"

# Куда писать результат
OUT_FILE = "russian-hosts.txt"

def extract_domains_from_abp(text: str) -> set[str]:
    """
    Берём Adblock Plus-правила (ruadlist+easylist.txt)
    и вытаскиваем домены вида ||domain.tld^
    """
    domains = set()

    # Простой паттерн для строк "||domain.tld^"
    abp_re = re.compile(r"^\|\|([a-zA-Z0-9._-]+\.[a-zA-Z]{2,})(\^|$)")

    for line in text.splitlines():
        line = line.strip()

        # Пропускаем пустое и комментарии / стили
        if not line or line.startswith(("!", "[", "@@", "/", "#")):
            continue

        # Ищем ||domain.tld^
        m = abp_re.match(line)
        if m:
            d = m.group(1).lower()
            # уберём ведущую точку, если есть
            d = d.lstrip(".")
            domains.add(d)

    return domains

def main():
    print(f"Downloading {SRC_URL} ...")
    resp = requests.get(SRC_URL, timeout=60)
    resp.raise_for_status()

    text = resp.text
    domains = extract_domains_from_abp(text)

    # Сортируем, чтобы diff был красивым
    sorted_domains = sorted(domains)

    print(f"Extracted {len(sorted_domains)} domains")

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        for d in sorted_domains:
            f.write(d + "\n")

    print(f"Wrote {OUT_FILE}")

if __name__ == "__main__":
    main()
