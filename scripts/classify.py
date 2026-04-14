#!/usr/bin/env python3
"""Classify dotku repos into GICS sector > industry group > industry.

Follows the 2023 GICS structure:
  Sector (11) > Industry Group (25) > Industry (74) > Sub-Industry (163)

We show Sector + Industry Group everywhere, and drill one level deeper
(Industry / Sub-Industry) inside Information Technology, where repo density
is highest.
"""
import json
import re
from collections import defaultdict

import os
_HERE = os.path.dirname(os.path.abspath(__file__))
_src = os.path.join(_HERE, 'enriched.json')
with open(_src) as f:
    repos = json.load(f)
# Use enriched description if original is missing/boilerplate
for _r in repos:
    _d = (_r.get('d') or '').strip()
    if (not _d or _d == 'Created with StackBlitz ⚡️' or len(_d) < 20) and _r.get('d_enriched'):
        _r['d'] = _r['d_enriched']

# Rules: (sector, industry_group, industry_or_subindustry_or_None, keywords).
# First match wins.
RULES = [
    # ---------- Health Care ----------
    ("Health Care", "Pharmaceuticals, Biotechnology & Life Sciences", None, [
        "pharma", "pharmacy", "drug", "biotech", "biouhan", "biointellitech",
        "genomics", "vaccine", "therapeutic",
    ]),
    ("Health Care", "Health Care Equipment & Services", None, [
        "medical", "medic", "medicine", "health", "healthcare", "clinic",
        "hospital", "doctor", "patient", "dentist", "dental", "fitness",
        "workout", "yoga", "psychology", "psych", "tcm", "herbal", "mask",
        "readyrx", "medtravel", "ihealth", "bluejay", "mentalhealth",
        "therapy", "autism", "hipaa", "hippa",
    ]),

    # ---------- Financials ----------
    ("Financials", "Insurance", None, [
        "insurance", "insur", "reinsurance",
    ]),
    ("Financials", "Banks", None, [
        "bank", "banking", "atm", "mortgage", "loan", "credit-union",
    ]),
    ("Financials", "Financial Services", None, [
        "crypto", "bitcoin", "btc", "ethereum", "blockchain", "defi",
        "trading", "trader", "stocks", "stock", "exchange-ai",
        "finance", "financial", "fintech", "payment", "pay", "invoice",
        "accounting", "bookkeep", "bookkeeping", "gusto", "intuit", "xero",
        "givebutter", "paypal", "stripe", "billing", "tax", "budget",
        "wallet",
    ]),

    # ---------- Real Estate ----------
    ("Real Estate", "Real Estate Management & Development", None, [
        "realestate", "realtor", "property", "rental", "housing",
        "apartment", "landlord", "appraisal", "mls",
    ]),

    # ---------- Energy ----------
    ("Energy", "Energy", None, [
        "energy", "solar", "petroleum", "coal", "fuel", "carku",
        "oilfield", "refinery",
    ]),

    # ---------- Utilities ----------
    ("Utilities", "Utilities", None, [
        "powergrid", "electric-utility", "water-utility", "gas-utility",
        "renewable-energy-utility",
    ]),

    # ---------- Materials ----------
    ("Materials", "Materials", None, [
        "mining", "jinkuang", "zijin", "steel", "metal", "chemical",
        "plastic", "papermill",
    ]),

    # ---------- Consumer Staples ----------
    ("Consumer Staples", "Food, Beverage & Tobacco", None, [
        "beverage", "snack", "tobacco", "beer", "winery", "coffee-roaster",
    ]),
    ("Consumer Staples", "Household & Personal Products", None, [
        "toothpaste", "soap", "detergent", "shampoo", "diaper",
    ]),
    ("Consumer Staples", "Consumer Staples Distribution & Retail", None, [
        "grocery", "supermarket", "warehouse-club",
    ]),

    # ---------- Consumer Discretionary ----------
    ("Consumer Discretionary", "Automobiles & Components", None, [
        "automotive", "ouxi", "carpool", "rideshare", "share-car",
        "ev-", "tesla",
    ]),
    ("Consumer Discretionary", "Consumer Durables & Apparel", None, [
        "fashion", "wig", "wigs", "shoe", "shoes", "apparel", "clothing",
        "cosmetic", "cosmetics", "makeup", "furniture", "jewelry",
        "dongguan-houjie-yusheng",
    ]),
    ("Consumer Discretionary", "Consumer Services", None, [
        "drycleaning", "drycleaner", "dryclean", "cleaners", "laundry",
        "beauty", "barber", "salon", "nail", "nails", "massage",
        "wedding", "honeymoon", "tourism", "travel", "hotel", "airbnb",
        "hostel", "restaurant", "dining", "tap2eat", "kitchen", "foodie",
        "menu", "dine", "recipe", "cafe", "coffee",
        "education", "tutor", "tutoring", "course", "edtech",
        "franchise", "lounge", "gaming", "casino", "florist",
        "tcm", "coway", "aonebeauty", "abonebeauty", "beauty8",
    ]),
    ("Consumer Discretionary", "Consumer Discretionary Distribution & Retail", None, [
        "ecommerce", "shopify", "shopee", "amazon", "retail", "store",
        "shop", "mall", "wholesale", "ppewholesale", "dkwholesale",
        "kandi", "shopdine", "shopdineguide", "shopping", "gift",
        "christmas", "membership", "tklink",
    ]),

    # ---------- Industrials ----------
    ("Industrials", "Transportation", None, [
        "courier", "delivery", "logistic", "logistics", "shipping",
        "freight", "cargo", "supplychain", "supply-chain", "warehouse",
        "airline", "railway", "trucking", "fuying",
    ]),
    ("Industrials", "Commercial & Professional Services", None, [
        "recruit", "recruiting", "staffing", "hiring", "human-resource",
        "legal", "lawyer", "attorney", "law", "gpulaw", "guplaw",
        "consulting", "advisory", "marketing", "advertising", "agency",
        "crm", "sales", "b2b", "editorial", "committee", "mcn", "mlm",
        "translation", "translator", "translate", "scraper", "scraping",
        "autoclaw", "inspection", "sienovo",
    ]),
    ("Industrials", "Capital Goods", None, [
        "construction", "builder", "contractor", "electrician", "plumber",
        "printing", "printer", "3d-printing", "drone", "robot", "robotic",
        "robotics", "manufacture", "manufactures", "factory", "industrial",
        "pipeline", "electronic", "erp", "hri",
    ]),

    # ---------- Communication Services ----------
    ("Communication Services", "Telecommunication Services", None, [
        "telecom", "5g", "sms", "smtp", "brevo", "mailgun", "twilio",
    ]),
    ("Communication Services", "Media & Entertainment", "Interactive Media & Services", [
        "social", "sns", "chatbot", "chat", "messaging", "message",
        "telegram", "wechat", "discord", "forum", "community",
        "youtube", "tiktok", "twitter", "weibo", "douyin",
    ]),
    ("Communication Services", "Media & Entertainment", "Entertainment", [
        "film", "movie", "music", "podcast", "streaming", "gaming-studio",
    ]),
    ("Communication Services", "Media & Entertainment", "Media", [
        "news", "media", "broadcast", "tv", "radio", "blog", "cms",
        "publishing", "wordpress", "docsify", "newsletter",
    ]),

    # ---------- Information Technology (with Industry-level splits) ----------
    ("Information Technology", "Semiconductors & Semiconductor Equipment", None, [
        "chip", "semiconductor", "fpga", "asic", "gpu-",
    ]),
    ("Information Technology", "Technology Hardware & Equipment",
     "Technology Hardware, Storage & Peripherals", [
        "hardware", "iot", "firmware", "embedded", "raspberry", "arduino",
        "esp32", "electron-printer",
    ]),
    # --- IT Services group ---
    ("Information Technology", "Software & Services",
     "Internet Services & Infrastructure", [
        "aws", "gcp", "azure", "vercel", "render", "netlify", "cloudflare",
        "docker", "kubernetes", "k8s", "hosting", "cdn", "supabase",
        "firebase", "serverless", "lambda", "nginx", "proxy", "gateway",
        "cloud",
    ]),
    ("Information Technology", "Software & Services",
     "IT Consulting & Other Services", [
        "it-services", "it-consulting", "devops-consulting", "msp",
    ]),
    # --- Software group: systems software first (narrower), then application software (catch-all) ---
    ("Information Technology", "Software & Services", "Systems Software", [
        "database", "sql", "nosql", "mongodb", "postgres", "postgresql",
        "mysql", "redis", "elasticsearch", "kafka", "rabbitmq",
        "security", "cyber", "encryption", "privacy", "vpn", "firewall",
        "auth", "oauth", "jwt", "identity",
        "compiler", "kernel", "os-", "linux", "unix", "shell",
        "observability", "monitoring", "telemetry", "logging",
    ]),
    ("Information Technology", "Software & Services", "Application Software", [
        # AI / ML
        "ai", "ml", "llm", "gpt", "deepseek", "gemma", "ollama",
        "langchain", "mcp", "agent", "rag", "embedding", "embeddings",
        "transformer", "genai",
        # Web / mobile frameworks & general apps
        "software", "api", "sdk", "cli", "framework", "library",
        "javascript", "typescript", "python", "react", "vue",
        "next", "nextjs", "nuxt", "angular", "node", "nodejs", "deno",
        "dashboard", "analytics", "search", "crawler", "browser",
        "extension", "devtools", "app",
    ]),
]

# Final fallback
DEFAULT = ("Information Technology", "Software & Services", "Application Software")

def build_regex(keywords):
    parts = [re.escape(k) for k in keywords]
    return re.compile(r"(?<![a-z0-9])(?:" + "|".join(parts) + r")(?![a-z0-9])",
                      re.IGNORECASE)

COMPILED = [(s, g, i, build_regex(kws)) for s, g, i, kws in RULES]

def normalize(s):
    return re.sub(r"[-_./]+", " ", s or "")

def classify(repo):
    name = normalize(repo.get('n') or '')
    desc = normalize(repo.get('d') or '')
    topics = normalize(' '.join(repo.get('t') or []))
    hay = f"{name} {desc} {topics}".lower()
    for sector, group, industry, rx in COMPILED:
        if rx.search(hay):
            return sector, group, industry
    return DEFAULT

# Bucket: sector -> group -> industry(or '_') -> [repos]
buckets = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
sector_counts = defaultdict(int)
group_counts = defaultdict(lambda: defaultdict(int))
for r in repos:
    sector, group, industry = classify(r)
    buckets[sector][group][industry or "_"].append(r)
    sector_counts[sector] += 1
    group_counts[sector][group] += 1

SECTOR_ORDER = [
    "Energy", "Materials", "Industrials", "Consumer Discretionary",
    "Consumer Staples", "Health Care", "Financials",
    "Information Technology", "Communication Services",
    "Utilities", "Real Estate",
]
GROUP_ORDER = {
    "Energy": ["Energy"],
    "Materials": ["Materials"],
    "Industrials": ["Capital Goods", "Commercial & Professional Services", "Transportation"],
    "Consumer Discretionary": [
        "Automobiles & Components", "Consumer Durables & Apparel",
        "Consumer Services", "Consumer Discretionary Distribution & Retail",
    ],
    "Consumer Staples": [
        "Consumer Staples Distribution & Retail",
        "Food, Beverage & Tobacco", "Household & Personal Products",
    ],
    "Health Care": [
        "Health Care Equipment & Services",
        "Pharmaceuticals, Biotechnology & Life Sciences",
    ],
    "Financials": ["Banks", "Financial Services", "Insurance"],
    "Information Technology": [
        "Software & Services", "Technology Hardware & Equipment",
        "Semiconductors & Semiconductor Equipment",
    ],
    "Communication Services": [
        "Telecommunication Services", "Media & Entertainment",
    ],
    "Utilities": ["Utilities"],
    "Real Estate": [
        "Equity Real Estate Investment Trusts (REITs)",
        "Real Estate Management & Development",
    ],
}
# Order for Industry/Sub-Industry within a group (only where used)
INDUSTRY_ORDER = {
    ("Information Technology", "Software & Services"): [
        "IT Consulting & Other Services",
        "Internet Services & Infrastructure",
        "Application Software",
        "Systems Software",
    ],
    ("Information Technology", "Technology Hardware & Equipment"): [
        "Technology Hardware, Storage & Peripherals",
        "Communications Equipment",
        "Electronic Equipment, Instruments & Components",
    ],
    ("Communication Services", "Media & Entertainment"): [
        "Media", "Entertainment", "Interactive Media & Services",
    ],
}

SECTOR_DESC = {
    "Energy": "Oil, gas, renewables, and energy equipment.",
    "Materials": "Mining, metals, chemicals, and construction materials.",
    "Industrials": "Capital goods, transportation & logistics, commercial and professional services.",
    "Consumer Discretionary": "Automobiles, retail, apparel, restaurants, hotels, leisure and education services.",
    "Consumer Staples": "Food, beverage, household and personal products.",
    "Health Care": "Medical devices, providers, pharma and biotech.",
    "Financials": "Banks, capital markets, insurance, fintech and crypto.",
    "Information Technology": "Software, IT services, hardware and semiconductors.",
    "Communication Services": "Media, entertainment, telecom, interactive media and social.",
    "Utilities": "Electric, water, gas and renewable utilities.",
    "Real Estate": "REITs, property management and real-estate services.",
}

# Console summary
print("GICS distribution:")
total = 0
for s in SECTOR_ORDER:
    n = sector_counts[s]
    total += n
    if n == 0:
        continue
    print(f"  {s}: {n}")
    for g in GROUP_ORDER[s]:
        gn = group_counts[s][g]
        if not gn:
            continue
        print(f"    {g}: {gn}")
        industry_list = buckets[s][g]
        if (s, g) in INDUSTRY_ORDER:
            for ind in INDUSTRY_ORDER[(s, g)]:
                if ind in industry_list:
                    print(f"      - {ind}: {len(industry_list[ind])}")
print(f"  TOTAL: {total}")

# Markdown output
lines = []
lines.append("## GitHub Repositories by GICS Classification\n")
lines.append(
    "Below are my open-source projects under "
    "[github.com/dotku](https://github.com/dotku), categorized using the "
    "[Global Industry Classification Standard (GICS)](https://www.msci.com/our-solutions/indexes/gics) "
    "— the taxonomy MSCI and S&P use for global equity markets. "
    "The hierarchy is **Sector (11) → Industry Group (25) → Industry (74)**; "
    "the third level is shown inside Information Technology and Media & Entertainment "
    "where repo density warrants it. "
    f"Auto-generated from {total} public repositories. "
    f"Forks of upstream open-source projects are marked with 🔀 and listed last within each group.\n"
)

# Overview table
lines.append("### Overview\n")
lines.append("| Sector | Industry Group | # Repos |")
lines.append("| --- | --- | ---: |")
for s in SECTOR_ORDER:
    n = sector_counts[s]
    if n == 0:
        continue
    first = True
    for g in GROUP_ORDER[s]:
        gn = group_counts[s][g]
        if not gn:
            continue
        sec_cell = f"**{s}** ({n})" if first else ""
        first = False
        lines.append(f"| {sec_cell} | {g} | {gn} |")
lines.append(f"| **Total** | | **{total}** |")
lines.append("")

for s in SECTOR_ORDER:
    n = sector_counts[s]
    if n == 0:
        continue
    lines.append(f"### {s} ({n})")
    lines.append(f"_{SECTOR_DESC[s]}_\n")
    for g in GROUP_ORDER[s]:
        gn = group_counts[s][g]
        if not gn:
            continue
        lines.append(f"#### {g} ({gn})\n")
        industry_map = buckets[s][g]
        industry_keys = list(industry_map.keys())
        ordered = INDUSTRY_ORDER.get((s, g))
        if ordered:
            industry_keys = [k for k in ordered if k in industry_map] + [
                k for k in industry_keys if k not in ordered]
        for ind in industry_keys:
            items = industry_map[ind]
            if not items:
                continue
            # Non-forks first, forks last; within each group alphabetically
            items_sorted = sorted(items,
                                  key=lambda r: (bool(r.get('fork')), r['n'].lower()))
            if ind != "_":
                lines.append(f"##### {ind} ({len(items)})\n")
            for r in items_sorted:
                name = r['n']
                desc = (r.get('d') or '').strip()
                desc = re.sub(r"\s+", " ", desc)
                desc_md = f" — {desc}" if desc else ""
                fork_mark = " 🔀" if r.get('fork') else ""
                lines.append(f"- [{name}](https://github.com/dotku/{name}){fork_mark}{desc_md}")
            lines.append("")

_out = os.path.join(_HERE, 'gics_section.md')
with open(_out, 'w') as f:
    f.write("\n".join(lines))
print(f"\nWrote {_out}")
