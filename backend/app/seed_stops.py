import csv
from pathlib import Path

from .models import Stop
from .extensions import db

def seedStops():
    csv_path = Path(__file__).resolve().parents[1] / "data" / "stops.csv"
    with csv_path.open(newline="", encoding="utf-8") as csvfile:
        rows = csv.DictReader(csvfile)
        stops = []
        for row in rows:
            stops.append(
                Stop(
                    name = row["name"],
                    image_url = row["image_url"],
                    is_transfer = row["is_transfer"].lower() == "true",
                    x = float(row["x"]),
                    y = float(row["y"]),
                    wheelchair_accessible = row["wheelchair_accessible"].lower() == "true",
                    has_shelter = row["has_shelter"].lower() == "true",
                    has_bench = row["has_bench"].lower() == "true",
                    has_ticket_machine = row["has_ticket_machine"].lower() == "true",
                    has_display = row["has_display"].lower() == "true"
                )
            )
    db.session.execute(db.delete(Stop))
    db.session.add_all(stops)
    db.session.commit()
