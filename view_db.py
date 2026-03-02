"""
HrVr Digital Solutions — MongoDB Database Viewer
Saari collections ka data print karta hai
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from mongo_models import (
    service_get_all, project_get_all, tech_get_all,
    stats_get_all, message_count, db
)
from pymongo import MongoClient

SEP = "─" * 55

print(f"\n{'═'*55}")
print(f"  🍃  MongoDB Database: {db.name}")
print(f"{'═'*55}")

# ── Collections list ──
cols = db.list_collection_names()
print(f"\n📂 Collections ({len(cols)} total): {', '.join(cols)}")

# ── Services ──
print(f"\n{SEP}")
print("📋  SERVICES COLLECTION  (8 documents)")
print(SEP)
for s in service_get_all():
    print(f"  [{s['_id'][:8]}...]  {s['icon']}  {s['title']}")
    print(f"                → {s['description'][:60]}...")

# ── Projects ──
print(f"\n{SEP}")
print("📁  PROJECTS COLLECTION  (6 documents)")
print(SEP)
for p in project_get_all():
    badge = "✅" if p['status'] == "Completed" else "🔄"
    print(f"  [{p['_id'][:8]}...]  {p['icon']}  {p['name']}")
    print(f"                → Tech: {p['tech']}  |  {badge} {p['status']}")

# ── Tech Stack ──
print(f"\n{SEP}")
print("🛠️   TECH_STACK COLLECTION  (4 documents)")
print(SEP)
for t in tech_get_all():
    print(f"  [{t['_id'][:8]}...]  {t['icon']}  {t['category']}")
    print(f"                → Skills: {', '.join(t['skills'])}")

# ── Stats ──
print(f"\n{SEP}")
print("📊  STATS COLLECTION  (4 documents)")
print(SEP)
for s in stats_get_all():
    print(f"  [{s['_id'][:8]}...]  {s['label']}: {s['stat_value']}")

# ── Messages ──
print(f"\n{SEP}")
cnt = message_count()
print(f"💬  MESSAGES COLLECTION  (Total: {cnt['total']} | Unread: {cnt['unread']})")
print(SEP)
print("  → Contact form se inquiries yahan save hongi")

# ── Indexes ──
print(f"\n{SEP}")
print("🔗  INDEXES")
print(SEP)
for col_name in cols:
    col = db[col_name]
    idxs = list(col.list_indexes())
    for idx in idxs:
        if idx['name'] != '_id_':
            print(f"  {col_name}: {idx['name']}  ({idx.get('unique', False) and 'UNIQUE' or 'INDEX'})")

print(f"\n{'═'*55}")
print("  ✅  HrVr Digital MongoDB — All Systems Go! 🚀")
print(f"{'═'*55}\n")
