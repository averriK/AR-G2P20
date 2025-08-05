#!/usr/bin/env python
"""
Build an interactive earthquake map with Kashima/mapper
and export the filtered epicentres as CSV.
"""

from pathlib import Path
import logging


# ── Kashima imports ────────────────────────────────────────────────
from kashima.mapper.config import (
    MapConfig,
    EventConfig,
    FaultConfig,
    DEFAULT_FAULT_STYLE_META,
)
from kashima.mapper.usgs_catalog import USGSCatalog
from kashima.mapper.event_map import EventMap


# ── logging ────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# --- user‑side settings -------------------------------------------------
MAG_BINS = [4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0]

DOT_PALETTE = {  # per‑bin colors for the *dots* & heat‑map
    "4.5-5.0": "#ffffb2",
    "5.0-5.5": "#fed976",
    "5.5-6.0": "#feb24c",
    "6.0-6.5": "#fd8d3c",
    "6.5-7.0": "#fc4e2a",
    "7.0-7.5": "#e31a1c",
    "7.5-8.0": "#bd0026",
    "8.0-8.5": "#800026",
    "8.5-9.0": "#4d0026",
}


DOT_SIZES = {
    "4.5-5.0": 3,
    "5.0-5.5": 3,
    "5.5-6.0": 4,
    "6.0-6.5": 6,
    "6.5-7.0": 12,
    "7.0-7.5": 13,
    "7.5-8.0": 18,
    "8.0-8.5": 19,
    "≥8.5": 24,
}


BEACHBALL_SIZES = {
    "4.5-5.0": 18,
    "5.0-5.5": 24,
    "5.5-6.0": 26,
    "6.0-6.5": 30,
    "6.5-7.0": 34,
    "7.0-7.5": 38,
    "7.5-8.0": 42,
    "8.0-8.5": 46,
    ">=8.5": 54,
}
# ------------------------------------------------------------------
# 2. (Optional) override default labels / colours for fault styles
# ------------------------------------------------------------------
USER_FAULT_STYLE = {
    "N":   {"label": "Normal",                 "color": "#3182bd"},
    "R":   {"label": "Reverse",                "color": "#de2d26"},
    "SS":  {"label": "Strike-slip",            "color": "#31a354"},
    "NSS": {"label": "Normal-Strike-slip",     "color": "#6baed6"},
    "RSS": {"label": "Reverse-Strike-slip",    "color": "#fc9272"},
    "O":   {"label": "Oblique",                "color": "#bdbdbd"},
    "U":   {"label": "Undetermined",           "color": "#969696"},
}

FAULT_STYLE = {**DEFAULT_FAULT_STYLE_META, **USER_FAULT_STYLE}
# ── I/O paths ──────────────────────────────────────────────────────
INPUT_DIR = Path("data")
OUTPUT_DIR = Path("maps")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

USGS_PATH = INPUT_DIR / "usgs-events.csv"
ISC_PATH = INPUT_DIR / "isc-events.csv"  # optional
LEGEND_PATH = INPUT_DIR / "legend.csv"
FAULTS_PATH = INPUT_DIR / "gem_active_faults.geojson"

# ── 0) Auto‑download the USGS catalogue if missing ────────────────
if not USGS_PATH.exists():
    logger.info("USGS CSV missing - downloading full catalogue …")
    USGS_DATA = USGSCatalog().get_events(event_type="earthquake")
    USGS_DATA.to_csv(USGS_PATH, index=False)
    logger.info("Saved %d events → %s", len(USGS_DATA), USGS_PATH)

# ── 1)  Map & layer configuration objects ─────────────────────────
MAP_CFG = MapConfig(
    project_name="Kainantu Gold Mine",
    client="K92 Mining Ltd",
    latitude=-6.1085,
    longitude=145.8869,
    radius_km=1500,#1500: requires  min_zoom_level=7
    base_zoom_level=9,
    min_zoom_level=5,#7: requires radius_km=1500, 5 requires 4000?
    max_zoom_level=15,
    default_tile_layer="Esri.WorldImagery",
    auto_fit_bounds=True,
    lock_pan=True,
    epicentral_circles=10,  # number of blue distance rings
)

EVENT_CFG = EventConfig(
    mag_bins=MAG_BINS,
    dot_palette=DOT_PALETTE,
    dot_sizes=DOT_SIZES,
    beachball_sizes=BEACHBALL_SIZES,
    fault_style_meta=FAULT_STYLE,
    legend_title="Magnitude (Mw)",
    heatmap_radius=50,
    heatmap_blur=30,
    heatmap_min_opacity=0.50,
    event_radius_multiplier=1.0,
    vmin=6.0,
    vmax=9.0,
    show_events_default=True,
    show_cluster_default=False,
    show_heatmap_default=False,
    show_beachballs_default=False,
    show_epicentral_circles_default=True,
)

FAULT_CFG = FaultConfig(
    include_faults=True,
    faults_gem_file_path=str(FAULTS_PATH),
    regional_faults_color="darkgreen",
    regional_faults_weight=4,
)

# ── 2)  Build the map ──────────────────────────────────────────────
EVENTS_MAP = EventMap(
    map_config=MAP_CFG,
    event_config=EVENT_CFG,
    events_csv=str(USGS_PATH),
    isc_csv=str(ISC_PATH) if ISC_PATH.exists() else None,
    legend_csv=str(LEGEND_PATH),
    mandatory_mag_col="mag",
    calculate_distance=True,
    fault_config=FAULT_CFG,
)

EVENTS_MAP.load_data()
MAP = EVENTS_MAP.get_map()

# ── 3)  Save artefacts ─────────────────────────────────────────────
html_out = OUTPUT_DIR / "index.html"
csv_out = OUTPUT_DIR / "epicenters.csv"

MAP.save(html_out)
EVENTS_MAP.events_df.to_csv(csv_out, index=False)

logger.info("✔ Map  → %s", html_out)
logger.info("✔ Data → %s", csv_out)
