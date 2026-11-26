#!/usr/bin/env python3
"""Export recipe XML + sample meal plans to JSON for the Fluffy Spoon PWA."""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from pathlib import Path

NS = {"r": "http://www.example.com/recipe"}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Rotation templates keyed by weekday index 0=Mon
WEEKDAY_THEMES = [
    ("Crockpot", "crockpot"),
    ("Leftovers / Easy", "easy"),
    ("Crockpot", "crockpot"),
    ("Meal Prep Lunch + Easy", "meal-prep"),
    ("Crockpot", "crockpot"),
    ("Large Batch / BBQ", "bbq-friendly"),
    ("Batch Cook / Prep", "weekend-batch"),
]

HOLIDAYS = {
    (7, 4): "Independence Day BBQ — pulled chicken or grilled adobo, corn, salads",
    (11, 26): "Thanksgiving — turkey or large roast chicken, festive sides",
    (12, 25): "Christmas — ham or special main, festive sides",
}


def text(el: ET.Element | None, default: str = "") -> str:
    if el is None or el.text is None:
        return default
    return re.sub(r"\s+", " ", el.text).strip()


def parse_recipe(path: Path) -> dict:
    tree = ET.parse(path)
    root = tree.getroot()
    rid = root.attrib.get("id") or path.stem
    title = text(root.find("r:title", NS), path.stem)
    summary = text(root.find("r:description/r:summary", NS))
    tags = [text(t) for t in root.findall("r:description/r:tags/r:tag", NS) if text(t)]
    meta = root.find("r:metadata", NS)
    metadata = {}
    if meta is not None:
        for key in ("servings", "prepTime", "cookTime", "totalTime", "difficulty"):
            metadata[key] = text(meta.find(f"r:{key}", NS))
    source_el = root.find("r:source", NS)
    source = {
        "name": text(source_el),
        "url": source_el.attrib.get("url", "") if source_el is not None else "",
    }
    ingredients = []
    for ing in root.findall("r:ingredients/r:ingredient", NS):
        ingredients.append(
            {
                "text": text(ing),
                "quantity": ing.attrib.get("quantity", ""),
                "unit": ing.attrib.get("unit", ""),
            }
        )
    steps = []
    for step in root.findall("r:preparation/r:step", NS):
        steps.append(
            {
                "number": int(step.attrib.get("number", len(steps) + 1)),
                "text": text(step),
            }
        )
    return {
        "id": rid,
        "title": title,
        "summary": summary,
        "tags": tags,
        "metadata": metadata,
        "source": source,
        "ingredients": ingredients,
        "steps": steps,
        "image": None,
    }


def pick_recipe(recipes: list[dict], tag: str, week: int, day_idx: int) -> dict | None:
    tagged = [r for r in recipes if tag in r["tags"]] or recipes
    if not tagged:
        return None
    return tagged[(week + day_idx) % len(tagged)]


def monday_of_iso_week(year: int, week: int) -> date:
    return date.fromisocalendar(year, week, 1)


def build_weeks(recipes: list[dict], year: int) -> list[dict]:
    weeks = []
    for week in range(1, 53):
        try:
            start = monday_of_iso_week(year, week)
        except ValueError:
            continue
        days = []
        bbq_prep: list[dict] = []
        for i, day_name in enumerate(DAYS):
            theme, tag = WEEKDAY_THEMES[i]
            recipe = pick_recipe(recipes, tag, week, i)
            day_date = start + timedelta(days=i)
            holiday = HOLIDAYS.get((day_date.month, day_date.day))
            entry = {
                "day": day_name,
                "date": day_date.isoformat(),
                "theme": theme,
                "recipeId": recipe["id"] if recipe else None,
                "recipeTitle": recipe["title"] if recipe else "Flexible",
                "notes": holiday or "",
            }
            days.append(entry)
            if tag in ("bbq-friendly", "weekend-batch") and recipe:
                bbq_prep.append(
                    {
                        "day": day_name,
                        "recipeId": recipe["id"],
                        "recipeTitle": recipe["title"],
                        "tasks": [
                            "Thaw protein night before if frozen",
                            "Set crockpot / prep rub or salsa in the morning",
                            "Portion leftovers for weekday lunches",
                            "Optional grill finish for BBQ flavor",
                        ],
                    }
                )
        weeks.append(
            {
                "week": week,
                "year": year,
                "label": f"Week {week}, {year}",
                "startDate": start.isoformat(),
                "days": days,
                "bbqPrep": bbq_prep,
            }
        )
    return weeks


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--recipes-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "recipes",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "pwa" / "public" / "data" / "seed.json",
    )
    parser.add_argument("--year", type=int, default=2026)
    args = parser.parse_args()

    recipes = [parse_recipe(p) for p in sorted(args.recipes_dir.glob("*.xml"))]
    seed = {
        "version": 1,
        "generatedForYear": args.year,
        "appName": "Fluffy Spoon",
        "recipes": recipes,
        "weeks": build_weeks(recipes, args.year),
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(seed, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(recipes)} recipes and {len(seed['weeks'])} weeks → {args.out}")


if __name__ == "__main__":
    main()
