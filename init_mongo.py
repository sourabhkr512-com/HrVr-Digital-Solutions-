"""
HrVr Digital Solutions — MongoDB Seed Script
Existing data ko MongoDB mein insert karta hai
Run: python init_mongo.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from mongo_models import (
    create_indexes,
    service_insert, project_insert, tech_insert, stat_upsert,
    services_col, projects_col, tech_stack_col, stats_col,
    db
)

print("\n" + "=" * 55)
print("  🚀  HrVr Digital — MongoDB Database Init  🚀")
print("=" * 55)


# ── Step 1: Indexes ──────────────────────────────────
create_indexes()


# ── Step 2: Wipe existing seed data (idempotent run) ─
print("\n🗑️  Clearing old seed data (messages kept)...")
services_col.delete_many({})
projects_col.delete_many({})
tech_stack_col.delete_many({})
stats_col.delete_many({})


# ══════════════════════════════════════════════════════
# SERVICES
# ══════════════════════════════════════════════════════
SERVICES_DATA = [
    {"title": "Custom Business Websites",     "icon": "💼",
     "description": "Professional websites tailored to your brand & business needs."},
    {"title": "Personal Portfolio Websites",  "icon": "👤",
     "description": "Showcase your work with a stunning, modern portfolio site."},
    {"title": "Management Systems",           "icon": "🏥",
     "description": "School, Library, Hospital — complete management solutions."},
    {"title": "Database-driven Web Apps",     "icon": "🗄️",
     "description": "Full-stack applications powered by robust database backends."},
    {"title": "Python Automations & Scripts", "icon": "🐍",
     "description": "Automate repetitive tasks and build powerful Python tools."},
    {"title": "Android & iOS Mobile Apps",    "icon": "📱",
     "description": "Cross-platform mobile apps for your business idea."},
    {"title": "UI/UX Design in Figma",        "icon": "🎨",
     "description": "Beautiful, user-friendly designs crafted in Figma."},
    {"title": "API Integration",              "icon": "🔗",
     "description": "Seamless third-party API connections for your applications."},
]

print("\n📋 Inserting Services...")
for svc in SERVICES_DATA:
    result = service_insert(svc["title"], svc["icon"], svc["description"])
    status = "✅" if result else "⚠️ (duplicate)"
    print(f"  {status} {svc['icon']}  {svc['title']}")


# ══════════════════════════════════════════════════════
# PROJECTS
# ══════════════════════════════════════════════════════
PROJECTS_DATA = [
    {"name": "Hospital Management System",  "tech": "PHP, MySQL, HTML5",    "icon": "🏥", "status": "Completed"},
    {"name": "Library Management Portal",   "tech": "Python, Flask, SQLite", "icon": "📚", "status": "Completed"},
    {"name": "E-Commerce Website",          "tech": "HTML5, JS, PHP",        "icon": "🛒", "status": "Completed"},
    {"name": "Portfolio Builder App",       "tech": "Python, Flask",         "icon": "💼", "status": "Completed"},
    {"name": "School ERP System",           "tech": "PHP, MySQL, JS",        "icon": "🏫", "status": "In Progress"},
    {"name": "Automation Bot Suite",        "tech": "Python, Selenium",      "icon": "🤖", "status": "Completed"},
]

print("\n📁 Inserting Projects...")
for proj in PROJECTS_DATA:
    result = project_insert(proj["name"], proj["tech"], proj["icon"], proj["status"])
    status = "✅" if result else "⚠️ (duplicate)"
    print(f"  {status} {proj['icon']}  {proj['name']}  [{proj['status']}]")


# ══════════════════════════════════════════════════════
# TECH STACK
# ══════════════════════════════════════════════════════
TECH_DATA = {
    "Web Development": {
        "icon": "🌐",
        "skills": ["HTML5", "CSS3", "JavaScript", "PHP", "MySQL",
                   "Management Systems (Hospital, Library, School)"]
    },
    "UI/UX & Design": {
        "icon": "🎨",
        "skills": ["Figma UI/UX Design", "Web Design (Modern & Responsive)",
                   "App UI Design"]
    },
    "Backend & Database": {
        "icon": "🛢️",
        "skills": ["Core PHP & MySQL", "Database-Driven Web Apps",
                   "API Integration"]
    },
    "Mobile & Automation": {
        "icon": "📱",
        "skills": ["Android & iOS Mobile Apps", "Python Automations & Scripts",
                   "Custom Python Tools"]
    }
}

print("\n🛠️  Inserting Tech Stack...")
for category, data in TECH_DATA.items():
    result = tech_insert(category, data["icon"], data["skills"])
    status = "✅" if result else "⚠️ (duplicate)"
    print(f"  {status} {data['icon']}  {category}  ({len(data['skills'])} skills)")


# ══════════════════════════════════════════════════════
# STATS
# ══════════════════════════════════════════════════════
STATS_DATA = [
    ("projects_completed", 50, "Projects Completed"),
    ("happy_clients",      30, "Happy Clients"),
    ("tech_skills",        15, "Tech Skills"),
    ("years_experience",    3, "Years Experience"),
]

print("\n📊 Inserting Stats...")
for key, val, label in STATS_DATA:
    stat_upsert(key, val, label)
    print(f"  ✅  {label}: {val}")


# ══════════════════════════════════════════════════════
# Summary
# ══════════════════════════════════════════════════════
print("\n" + "=" * 55)
print("  📊  DATABASE SUMMARY")
print("=" * 55)
print(f"  🗄️  Database    : {db.name}")
print(f"  📋  Services    : {services_col.count_documents({})} documents")
print(f"  📁  Projects    : {projects_col.count_documents({})} documents")
print(f"  🛠️   Tech Stack  : {tech_stack_col.count_documents({})} documents")
print(f"  📊  Stats       : {stats_col.count_documents({})} documents")
print(f"  💬  Messages    : {db['messages'].count_documents({})} documents")
print("=" * 55)
print("  ✅  MongoDB Database Ready!")
print("=" * 55 + "\n")
