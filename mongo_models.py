"""
HrVr Digital Solutions — MongoDB Models & Helpers
PyMongo ke saath MongoDB Collections define karta hai
"""

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError
from bson.errors import InvalidId
from bson import ObjectId
from datetime import datetime
import os

# ──────────────────────────────────────────────
# Connection
# ──────────────────────────────────────────────
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME   = os.environ.get("MONGO_DB",  "hrvr_digital")

client = MongoClient(MONGO_URI)
db     = client[DB_NAME]

# ──────────────────────────────────────────────
# Collections
# ──────────────────────────────────────────────
messages_col   = db["messages"]
services_col   = db["services"]
projects_col   = db["projects"]
tech_stack_col = db["tech_stack"]
stats_col      = db["stats"]


# ──────────────────────────────────────────────
# Index Setup (call once at startup)
# ──────────────────────────────────────────────
def create_indexes():
    # messages: email pe index + timestamp descending
    messages_col.create_index([("email", ASCENDING)])
    messages_col.create_index([("timestamp", DESCENDING)])
    messages_col.create_index([("is_read", ASCENDING)])

    # services: title unique
    services_col.create_index([("title", ASCENDING)], unique=True)

    # projects: name unique
    projects_col.create_index([("name", ASCENDING)], unique=True)
    projects_col.create_index([("status", ASCENDING)])

    # tech_stack: category unique
    tech_stack_col.create_index([("category", ASCENDING)], unique=True)

    # stats: stat_key unique
    stats_col.create_index([("stat_key", ASCENDING)], unique=True)

    print("✅ MongoDB Indexes Created Successfully!")


# ──────────────────────────────────────────────
# Helper: ObjectId → string
# ──────────────────────────────────────────────
def serialize(doc):
    """MongoDB document ko JSON-serializable dict mein convert karo."""
    if doc is None:
        return None
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


def serialize_many(docs):
    return [serialize(d) for d in docs]


def validate_object_id(doc_id):
    """Validate if string is valid MongoDB ObjectId."""
    try:
        return ObjectId(doc_id)
    except InvalidId:
        return None


# ══════════════════════════════════════════════
# MESSAGES COLLECTION
# ══════════════════════════════════════════════

"""
Schema:
{
  _id:       ObjectId,
  name:      string,
  email:     string,
  project:   string,
  message:   string,
  timestamp: datetime,
  is_read:   bool
}
"""

def message_insert(name, email, project, message_text):
    doc = {
        "name":      name,
        "email":     email,
        "project":   project or "Not specified",
        "message":   message_text,
        "timestamp": datetime.utcnow(),
        "is_read":   False
    }
    result = messages_col.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return doc


def message_get_all(only_unread=False):
    query = {"is_read": False} if only_unread else {}
    docs  = messages_col.find(query).sort("timestamp", DESCENDING)
    return serialize_many(list(docs))


def message_get_by_id(msg_id):
    obj_id = validate_object_id(msg_id)
    if not obj_id:
        return None
    doc = messages_col.find_one({"_id": obj_id})
    return serialize(doc)


def message_mark_read(msg_id):
    obj_id = validate_object_id(msg_id)
    if not obj_id:
        return False
    result = messages_col.update_one(
        {"_id": obj_id},
        {"$set": {"is_read": True}}
    )
    return result.modified_count > 0


def message_delete(msg_id):
    obj_id = validate_object_id(msg_id)
    if not obj_id:
        return False
    result = messages_col.delete_one({"_id": obj_id})
    return result.deleted_count > 0


def message_count():
    return {
        "total":  messages_col.count_documents({}),
        "unread": messages_col.count_documents({"is_read": False})
    }


# ══════════════════════════════════════════════
# SERVICES COLLECTION
# ══════════════════════════════════════════════

"""
Schema:
{
  _id:         ObjectId,
  title:       string,
  icon:        string,
  description: string,
  is_active:   bool
}
"""

def service_insert(title, icon, description):
    doc = {
        "title":       title,
        "icon":        icon,
        "description": description,
        "is_active":   True
    }
    try:
        result = services_col.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return doc
    except DuplicateKeyError:
        return None


def service_get_all(active_only=True):
    query = {"is_active": True} if active_only else {}
    docs  = services_col.find(query)
    return serialize_many(list(docs))


def service_update(service_id, updates):
    obj_id = validate_object_id(service_id)
    if not obj_id:
        return False
    result = services_col.update_one(
        {"_id": obj_id},
        {"$set": updates}
    )
    return result.modified_count > 0


def service_delete(service_id):
    obj_id = validate_object_id(service_id)
    if not obj_id:
        return False
    result = services_col.delete_one({"_id": obj_id})
    return result.deleted_count > 0


# ══════════════════════════════════════════════
# PROJECTS COLLECTION
# ══════════════════════════════════════════════

"""
Schema:
{
  _id:        ObjectId,
  name:       string,
  tech:       string,
  icon:       string,
  status:     string  ("Completed" | "In Progress"),
  created_at: datetime
}
"""

def project_insert(name, tech, icon, status="Completed"):
    doc = {
        "name":       name,
        "tech":       tech,
        "icon":       icon,
        "status":     status,
        "created_at": datetime.utcnow()
    }
    try:
        result = projects_col.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return doc
    except DuplicateKeyError:
        return None


def project_get_all():
    docs = projects_col.find().sort("created_at", DESCENDING)
    return serialize_many(list(docs))


def project_get_by_status(status):
    docs = projects_col.find({"status": status})
    return serialize_many(list(docs))


def project_update(project_id, updates):
    obj_id = validate_object_id(project_id)
    if not obj_id:
        return False
    result = projects_col.update_one(
        {"_id": obj_id},
        {"$set": updates}
    )
    return result.modified_count > 0


def project_delete(project_id):
    obj_id = validate_object_id(project_id)
    if not obj_id:
        return False
    result = projects_col.delete_one({"_id": obj_id})
    return result.deleted_count > 0


# ══════════════════════════════════════════════
# TECH STACK COLLECTION
# ══════════════════════════════════════════════

"""
Schema:
{
  _id:      ObjectId,
  category: string,
  icon:     string,
  skills:   [string, ...]
}
"""

def tech_insert(category, icon, skills_list):
    doc = {
        "category": category,
        "icon":     icon,
        "skills":   skills_list   # list of strings
    }
    try:
        result = tech_stack_col.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return doc
    except DuplicateKeyError:
        return None


def tech_get_all():
    docs = tech_stack_col.find()
    return serialize_many(list(docs))


def tech_add_skill(category, skill):
    result = tech_stack_col.update_one(
        {"category": category},
        {"$addToSet": {"skills": skill}}
    )
    return result.modified_count > 0


def tech_remove_skill(category, skill):
    result = tech_stack_col.update_one(
        {"category": category},
        {"$pull": {"skills": skill}}
    )
    return result.modified_count > 0


# ══════════════════════════════════════════════
# STATS COLLECTION
# ══════════════════════════════════════════════

"""
Schema:
{
  _id:        ObjectId,
  stat_key:   string  (unique),
  stat_value: int,
  label:      string
}
"""

def stat_upsert(stat_key, stat_value, label=""):
    stats_col.update_one(
        {"stat_key": stat_key},
        {"$set": {"stat_value": stat_value, "label": label}},
        upsert=True
    )


def stat_increment(stat_key, amount=1):
    stats_col.update_one(
        {"stat_key": stat_key},
        {"$inc": {"stat_value": amount}},
        upsert=True
    )


def stat_get(stat_key):
    doc = stats_col.find_one({"stat_key": stat_key})
    return serialize(doc)


def stats_get_all():
    docs = stats_col.find()
    return serialize_many(list(docs))
