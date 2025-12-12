
from flask import Blueprint, current_app, jsonify
from ..pipelines.ingest_openaq import run as run_openaq
from ..pipelines.ingest_osm import run as run_osm
from ..pipelines.ingest_gtfs import run as run_gtfs

ingest_bp = Blueprint("ingest", __name__)

@ingest_bp.post("/openaq")
def ingest_openaq():
    settings = current_app.config["SETTINGS"]
    # Example bbox (change for your city)
    run_openaq([-79.6, 43.6, -79.2, 43.8])  # Toronto-ish bbox
    return jsonify({"status": "ok"}), 200

@ingest_bp.post("/osm")
def ingest_osm():
    run_osm(city="Toronto")
    return jsonify({"status": "ok"}), 200

@ingest_bp.post("/gtfs")
def ingest_gtfs():
    run_gtfs(path="data/raw/gtfs.zip")
    return jsonify({"status": "ok"}), 200
