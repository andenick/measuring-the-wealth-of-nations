"""NAICS sector classification: productive, unproductive, trading, government.

Based on Shaikh & Tonak (1994) Appendix B classification principles
(HDARP chunk_27) adapted for NAICS summary IO codes.

Classification principles:
- Productive: Creates or transforms use values (goods + productive services)
- Trading: Circulates use values (wholesale/retail + rental)
- Unproductive: FIRE, legal, management, admin services
- Government: Government enterprises (productive proxy) and general government (excluded)

Reference: IO_METHODOLOGY_EXTRACTION.md, DEC-009
"""

from __future__ import annotations

import pandas as pd
from pathlib import Path

# NAICS summary IO code → classification
# Source: Book Appendix B (85 SIC sectors) mapped to NAICS summary codes
NAICS_CLASSIFICATION: dict[str, str] = {
    # ═══ PRODUCTIVE (goods-producing + productive services) ═══
    # Agriculture
    "111CA": "productive",    # Farms
    "113FF": "productive",    # Forestry, fishing, and related activities
    # Mining
    "211": "productive",      # Oil and gas extraction
    "212": "productive",      # Mining, except oil and gas
    "213": "productive",      # Support activities for mining
    # Utilities
    "22": "productive",       # Utilities
    # Construction
    "23": "productive",       # Construction
    # Manufacturing — ALL productive
    "311FT": "productive",    # Food and beverage and tobacco products
    "313TT": "productive",    # Textile mills and textile product mills
    "315AL": "productive",    # Apparel and leather and allied products
    "321": "productive",      # Wood products
    "322": "productive",      # Paper products
    "323": "productive",      # Printing and related support activities
    "324": "productive",      # Petroleum and coal products
    "325": "productive",      # Chemical products
    "326": "productive",      # Plastics and rubber products
    "327": "productive",      # Nonmetallic mineral products
    "331": "productive",      # Primary metals
    "332": "productive",      # Fabricated metal products
    "333": "productive",      # Machinery
    "334": "productive",      # Computer and electronic products
    "335": "productive",      # Electrical equipment, appliances, and components
    "3361MV": "productive",   # Motor vehicles, bodies and trailers, and parts
    "3364OT": "productive",   # Other transportation equipment
    "337": "productive",      # Furniture and related products
    "339": "productive",      # Miscellaneous manufacturing
    # Transportation — productive (freight + passenger)
    "481": "productive",      # Air transportation
    "482": "productive",      # Rail transportation
    "483": "productive",      # Water transportation
    "484": "productive",      # Truck transportation
    "485": "productive",      # Transit and ground passenger transportation
    "486": "productive",      # Pipeline transportation
    "487OS": "productive",    # Other transportation and support activities
    "493": "productive",      # Warehousing and storage
    # Productive services
    "512": "productive",      # Motion picture and sound recording industries
    "711AS": "productive",    # Performing arts, spectator sports, museums
    "713": "productive",      # Amusements, gambling, and recreation industries
    "721": "productive",      # Accommodation
    "722": "productive",      # Food services and drinking places
    "81": "productive",       # Other services, except government (repair, personal, etc.)

    # ═══ TRADING (wholesale/retail + rental) ═══
    "42": "trading",          # Wholesale trade
    "441": "trading",         # Motor vehicle and parts dealers
    "445": "trading",         # Food and beverage stores
    "452": "trading",         # General merchandise stores
    "4A0": "trading",         # Other retail
    "532RL": "trading",       # Rental and leasing services

    # ═══ UNPRODUCTIVE (FIRE, business services) ═══
    "521CI": "unproductive",  # Federal Reserve banks, credit intermediation
    "523": "unproductive",    # Securities, commodity contracts, and investments
    "524": "unproductive",    # Insurance carriers and related activities
    "525": "unproductive",    # Funds, trusts, and other financial vehicles
    "HS": "unproductive",     # Housing services (owner-occupied imputed rent)
    "ORE": "unproductive",    # Other real estate
    "5411": "unproductive",   # Legal services
    "55": "unproductive",     # Management of companies and enterprises
    "561": "unproductive",    # Administrative and support services
    "562": "unproductive",    # Waste management and remediation services

    # ═══ MIXED/DEBATABLE (classified per book principles) ═══
    # Information sector — split: broadcasting/telecom = productive infrastructure,
    # publishing/software/data processing = mixed. Classify as productive per book's
    # treatment of communications (SIC sectors in productive NIPA group 7).
    "511": "productive",      # Publishing industries (includes software)
    "513": "productive",      # Broadcasting and telecommunications
    "514": "productive",      # Data processing, internet, other information

    # Professional services — Shaikh classifies R&D and technical services as
    # unproductive (royalties sector). Computer systems design is modern equivalent.
    "5412OP": "unproductive", # Misc professional, scientific, technical services
    "5415": "unproductive",   # Computer systems design and related services

    # Education and health — book treats as productive services when producing
    # use values. Fee-for-service health care is productive; education is productive.
    "61": "productive",       # Educational services
    "621": "productive",      # Ambulatory health care services
    "622": "productive",      # Hospitals
    "623": "productive",      # Nursing and residential care facilities
    "624": "productive",      # Social assistance

    # ═══ GOVERNMENT ═══
    "GFE": "govt_enterprise",   # Federal government enterprises (productive proxy)
    "GSLE": "govt_enterprise",  # State and local government enterprises
    "GFGD": "govt_admin",       # Federal general government (defense)
    "GFGN": "govt_admin",       # Federal general government (nondefense)
    "GSLG": "govt_admin",       # State and local general government
}


def classify_naics_sectors(sector_codes: list[str]) -> dict[str, list[str]]:
    """Classify NAICS sector codes into productive/unproductive/trading/government.

    Returns dict with keys: productive, trading, unproductive, govt_enterprise, govt_admin, unclassified
    """
    groups: dict[str, list[str]] = {
        "productive": [],
        "trading": [],
        "unproductive": [],
        "govt_enterprise": [],
        "govt_admin": [],
        "unclassified": [],
    }

    for code in sector_codes:
        cls = NAICS_CLASSIFICATION.get(code, "unclassified")
        groups[cls].append(code)

    return groups


def get_productive_sector_codes() -> list[str]:
    """Return list of all productive NAICS codes."""
    return [k for k, v in NAICS_CLASSIFICATION.items() if v == "productive"]


def get_trading_sector_codes() -> list[str]:
    """Return list of all trading NAICS codes."""
    return [k for k, v in NAICS_CLASSIFICATION.items() if v == "trading"]


def get_unproductive_sector_codes() -> list[str]:
    """Return list of all unproductive NAICS codes."""
    return [k for k, v in NAICS_CLASSIFICATION.items() if v == "unproductive"]


def save_classification_csv(output_path: Path | str) -> None:
    """Save the classification to a CSV file."""
    records = []
    for code, cls in sorted(NAICS_CLASSIFICATION.items()):
        records.append({"naics_code": code, "classification": cls})
    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
