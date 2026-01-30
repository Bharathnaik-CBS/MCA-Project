# routes/fetch_routes.py
from flask import Blueprint, jsonify
from utils.db_helpers import get_db_connection

fetch_bp = Blueprint('fetch_bp', __name__)


@fetch_bp.route("/get-projects")
def get_projects():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT pro_id, pro_name FROM project")
    projects = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(projects)



@fetch_bp.route("/get-latest-tid")
def get_latest_tid():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT MAX(t_id) AS max_id FROM transactions")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify({"t_id": (result["max_id"] or 0) + 1})



@fetch_bp.route("/get-employees")
def get_employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT e_id, e_name FROM employee")
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(employees)



@fetch_bp.route("/get-platforms")
def get_platforms():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT p_id, p_types FROM platform order by p_id")
    platforms = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(platforms)


