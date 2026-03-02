"""
HrVr Digital Solutions — Flask Web Application
Fixed & Complete Version — Contact Form Working + MongoDB Storage
"""

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from mongo_models import create_indexes, message_insert, service_get_all, stats_get_all
from flask_mail import Mail, Message

load_dotenv()  # .env file se password load karo
from datetime import datetime
import os

# MongoDB helpers
from mongo_models import (
    create_indexes,
    message_insert, message_get_all, message_count,
    service_get_all, project_get_all, tech_get_all, stats_get_all,
    stat_increment
)

app = Flask(__name__)
app.secret_key = "hrvr_digital_solutions_2026"

# ─────────────────────────────────────────────
# Flask-Mail Config
# Gmail App Password yahan daalo:
#   1. Google Account → Security → 2-Step Verification ON karo
#   2. phir "App Passwords" mein jaao → "Mail" select karo → Password copy karo
#   3. MAIL_PASSWORD mein woh 16-digit password daalo
# ─────────────────────────────────────────────
app.config['MAIL_SERVER']         = 'smtp.gmail.com'
app.config['MAIL_PORT']           = 587
app.config['MAIL_USE_TLS']        = True
app.config['MAIL_USERNAME']       = 'hrvrdigitalsolutions@gmail.com'        # ← Tera Gmail
app.config['MAIL_PASSWORD']       = os.environ.get('Digitalbotservices@255', 'jwoy ynop yedt bxwg')  # ← App Password yahan
app.config['MAIL_DEFAULT_SENDER'] = ('HrVr Digital Solutions', 'hrvrdigitalsolutions@gmail.com')

mail = Mail(app)

# Indexes on startup
with app.app_context():
    try:
        create_indexes()
        print("✅ MongoDB Indexes Ready!")
    except Exception as e:
        print(f"⚠️ Index creation: {e}")
        

# ─────────────────────────────────────────────
# Portfolio / Services Data
# ─────────────────────────────────────────────
TECH_STACK = {
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

SERVICES = [
    {"title": "Custom Business Websites",     "icon": "💼", "desc": "Professional websites tailored to your brand & business needs."},
    {"title": "Personal Portfolio Websites",  "icon": "👤", "desc": "Showcase your work with a stunning, modern portfolio site."},
    {"title": "Management Systems",           "icon": "🏥", "desc": "School, Library, Hospital — complete management solutions."},
    {"title": "Database-driven Web Apps",     "icon": "🗄️", "desc": "Full-stack applications powered by robust database backends."},
    {"title": "Python Automations & Scripts", "icon": "🐍", "desc": "Automate repetitive tasks and build powerful Python tools."},
    {"title": "Android & iOS Mobile Apps",    "icon": "📱", "desc": "Cross-platform mobile apps for your business idea."},
    {"title": "UI/UX Design in Figma",        "icon": "🎨", "desc": "Beautiful, user-friendly designs crafted in Figma."},
    {"title": "API Integration",              "icon": "🔗", "desc": "Seamless third-party API connections for your applications."},
]

PROJECTS = [
    {"name": "Hospital Management System",  "tech": "PHP, MySQL, HTML5",    "icon": "🏥", "status": "Completed"},
    {"name": "Library Management Portal",   "tech": "Python, Flask, SQLite", "icon": "📚", "status": "Completed"},
    {"name": "E-Commerce Website",          "tech": "HTML5, JS, PHP",        "icon": "🛒", "status": "Completed"},
    {"name": "Portfolio Builder App",       "tech": "Python, Flask",         "icon": "💼", "status": "Completed"},
    {"name": "School ERP System",           "tech": "PHP, MySQL, JS",        "icon": "🏫", "status": "In Progress"},
    {"name": "Automation Bot Suite",        "tech": "Python, Selenium",      "icon": "🤖", "status": "Completed"},
]

MESSAGES = []

# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html",
                           tech_stack=TECH_STACK,
                           services=SERVICES,
                           projects=PROJECTS,
                           year=datetime.now().year)

@app.route("/services")
def services():
    return render_template("services.html", services=SERVICES, year=datetime.now().year)

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html", projects=PROJECTS, year=datetime.now().year)

@app.route("/contact")
def contact():
    return render_template("contact.html", year=datetime.now().year)


# ─────────────────────────────────────────────
# Contact Form API — Mail jaayegi hrvrdigitalsolutions@gmail.com pe
# ─────────────────────────────────────────────
@app.route("/api/contact", methods=["POST"])
def api_contact():
    data    = request.get_json()
    name    = data.get("name",    "").strip()
    email   = data.get("email",   "").strip()
    project = data.get("project", "").strip()
    message = data.get("message", "").strip()

    if not all([name, email, message]):
        return jsonify({"success": False, "error": "Please fill all required fields."}), 400

    # ── Save to MongoDB ──────────────────────
    entry = message_insert(name, email, project, message)
    MESSAGES.append(entry)

    # ─── HTML Mail Body ───
    mail_body_html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0f0f1a; color: #ffffff; border-radius: 12px; overflow: hidden;">
      <div style="background: linear-gradient(135deg, #7c3aed, #06b6d4); padding: 30px; text-align: center;">
        <h1 style="margin:0; font-size: 24px;">🚀 New Project Inquiry</h1>
        <p style="margin:5px 0 0; opacity:0.9;">HrVr Digital Solutions</p>
      </div>
      <div style="padding: 30px;">
        <table style="width:100%; border-collapse: collapse;">
          <tr>
            <td style="padding: 10px; color:#06b6d4; font-weight:bold; width:140px;">👤 Name</td>
            <td style="padding: 10px; color:#ffffff;">{name}</td>
          </tr>
          <tr style="background:rgba(255,255,255,0.05);">
            <td style="padding: 10px; color:#06b6d4; font-weight:bold;">📧 Client Email</td>
            <td style="padding: 10px;"><a href="mailto:{email}" style="color:#7c3aed;">{email}</a></td>
          </tr>
          <tr>
            <td style="padding: 10px; color:#06b6d4; font-weight:bold;">🚀 Project Type</td>
            <td style="padding: 10px; color:#ffffff;">{project if project else 'Not specified'}</td>
          </tr>
          <tr style="background:rgba(255,255,255,0.05);">
            <td style="padding: 10px; color:#06b6d4; font-weight:bold;">🕐 Time</td>
            <td style="padding: 10px; color:#ffffff;">{entry['timestamp']}</td>
          </tr>
        </table>
        <div style="margin-top:20px; padding:20px; background:rgba(255,255,255,0.05); border-radius:8px; border-left:4px solid #7c3aed;">
          <p style="color:#06b6d4; font-weight:bold; margin:0 0 10px;">💬 Message:</p>
          <p style="color:#ffffff; margin:0; line-height:1.6;">{message}</p>
        </div>
        <div style="margin-top:25px; text-align:center;">
          <a href="mailto:{email}" style="background: linear-gradient(135deg, #7c3aed, #06b6d4); color:#ffffff; padding:12px 30px; border-radius:8px; text-decoration:none; font-weight:bold;">
            ↩️ Reply to {name}
          </a>
        </div>
      </div>
      <div style="padding: 15px; text-align:center; color:rgba(255,255,255,0.4); font-size:12px; border-top:1px solid rgba(255,255,255,0.1);">
        HrVr Digital Solutions — "You Imagine It, I Develop It." 🚀
      </div>
    </div>
    """

    # Plain text fallback
    mail_body_plain = f"""
New Project Inquiry — HrVr Digital Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Name         : {name}
Client Email : {email}
Project Type : {project if project else 'Not specified'}
Time         : {entry['timestamp']}

Message:
{message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply directly to client: {email}
    """

    try:
        msg = Message(
            subject   = f"🚀 New Inquiry from {name} — HrVr Digital",
            recipients= ["hrvrdigitalsolutions@gmail.com"],   # ← Tera inbox
            body      = mail_body_plain,
            html      = mail_body_html,
            reply_to  = email                                  # ← Reply seedha client ko jaayegi
        )
        mail.send(msg)
        print(f"[✅ MAIL SENT] To: hrvrdigitalsolutions@gmail.com | From: {name} <{email}>")

    except Exception as e:
        print(f"[❌ MAIL ERROR] {e}")
        return jsonify({
            "success": False,
            "error": "Mail server error. Please check MAIL_PASSWORD in app.py or contact hrvrdigitalsolutions@gmail.com directly."
        }), 500

    print(f"[📬 NEW INQUIRY] {name} <{email}> | Project: {project}")
    return jsonify({
        "success": True,
        "message": "Message sent successfully! I'll get back to you within 2-4 hours. 🚀"
    })

# ─────────────────────────────────────────────
# Stats API — MongoDB se live data
# ─────────────────────────────────────────────
@app.route("/api/stats")
def api_stats():
    stats_list = stats_get_all()
    result = {s["stat_key"]: s["stat_value"] for s in stats_list}
    return jsonify(result)

# ─────────────────────────────────────────────
# Stats API
# ─────────────────────────────────────────────
@app.route("/api/services")
def api_services():
    services = service_get_all()
    stats = {
        "projects_completed": 50,
        "happy_clients":      30,
        "tech_skills":        15,
        "years_experience":    3
    }
    return jsonify({**services, **stats})


# ─────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  🚀  HrVr Digital Solutions — MongoDB Server  🚀")
    print("=" * 55)
    print("  Open: http://127.0.0.1:5001")
    print("  📧  Mail → hrvrdigitalsolutions@gmail.com")
    print("  🍃  MongoDB → hrvr_digital database")
    print("=" * 55)
    app.run(debug=True, host="0.0.0.0", port=5001)
