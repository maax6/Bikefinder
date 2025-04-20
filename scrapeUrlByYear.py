#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
import argparse
import os

BASE_URL = "https://bikez.com"
MIN_YEAR = 1894
MAX_YEAR = 2025

def get_motorcycles_by_year(year):
    url = f"{BASE_URL}/year/{year}-motorcycle-models.php"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        table = soup.find_all("table")[1]
    except IndexError:
        print(f"❌ Aucun tableau trouvé pour l'année {year}")
        return {}

    rows = table.find_all("tr")[1:]
    data = {}

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 4:
            link_tag = cols[0].find("a")
            if not link_tag:
                continue

            name = link_tag.text.strip()
            relative_url = link_tag.get("href")
            relative_url = relative_url.replace("../", "")  # Clean ../
            full_url = f"{BASE_URL}/{relative_url.lstrip('/')}"
            category = cols[2].text.strip()
            engine = cols[3].text.strip()

            # Séparer marque et modèle
            if " " in name:
                brand, model = name.split(" ", 1)
            else:
                brand = name
                model = ""

            key_name = f"{brand} {model} ({year})"

            data[key_name] = {
                "brand": brand,
                "model": model,
                "year": year,
                "category": category,
                "engine": engine,
                "url": full_url
            }

    return data


def save_json(data, year):
    output_dir = "json_motorcycles"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"motorcycles_{year}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(data)} modèles sauvegardés dans {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape les URL des motos Bikez par année")

    parser.add_argument("--year", type=int, help="Année unique à scrapper")
    parser.add_argument("--from", dest="from_year", type=int, help="Année de début (inclus)")
    parser.add_argument("--to", dest="to_year", type=int, help="Année de fin (inclus)")

    args = parser.parse_args()

    years = []

    if args.year:
        if MIN_YEAR <= args.year <= MAX_YEAR:
            years = [args.year]
        else:
            print(f"❌ L'année doit être entre {MIN_YEAR} et {MAX_YEAR}")
            exit(1)
    elif args.from_year and args.to_year:
        if args.from_year > args.to_year:
            print("❌ L'année de début doit être inférieure ou égale à l'année de fin.")
            exit(1)
        if args.from_year < MIN_YEAR or args.to_year > MAX_YEAR:
            print(f"❌ Les années doivent être comprises entre {MIN_YEAR} et {MAX_YEAR}")
            exit(1)
        years = list(range(args.from_year, args.to_year + 1))
    else:
        print("❌ Veuillez fournir soit --year, soit --from et --to")
        exit(1)

    for year in years:
        print(f"📦 Récupération des motos pour l'année {year}...")
        motos = get_motorcycles_by_year(year)
        if motos:
            save_json(motos, year)