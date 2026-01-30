# routes/chart_routes.py
from flask import Blueprint, jsonify, request
from utils.db_helpers import get_db_connection
from datetime import date
from datetime import datetime


chart_bp = Blueprint('chart_bp', __name__)


@chart_bp.route("/api/employee-metrics", methods=["POST"])
def employee_metrics():
    data = request.get_json()
    start, end = data["start"], data["end"]
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT SUM(bulk_leads_reach) AS bulk, SUM(incoming) AS incoming, SUM(interest) AS interest
        FROM entries
        JOIN transactions ON entries.trans_id = transactions.t_id
        WHERE DATE(transactions.Date) BETWEEN %s AND %s
    """, (start, end))
    result = cursor.fetchone()
    return jsonify(result)


@chart_bp.route("/api/project-metrics", methods=["POST"])
def project_metrics():
    data = request.get_json()
    start, end = data["start"], data["end"]
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT project.pro_name, 
               SUM(entries.bulk_leads_reach) AS bulk, 
               SUM(entries.incoming) AS incoming, 
               SUM(entries.interest) AS interest
        FROM entries
        JOIN transactions ON entries.trans_id = transactions.t_id
        JOIN project ON transactions.project_id = project.pro_id
        WHERE DATE(transactions.Date) BETWEEN %s AND %s
        GROUP BY project.pro_id
    """, (start, end))
    return jsonify(cursor.fetchall())


@chart_bp.route("/api/bookings-by-project")
def bookings_by_project():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT project.pro_name, COUNT(*) AS total_bookings
        FROM booking
        JOIN project ON booking.id_project = project.pro_id
        GROUP BY booking.id_project
    """)
    return jsonify(cursor.fetchall())



@chart_bp.route("/api/overall-analytics")
def overall_analytics():
    start = request.args.get('start')
    end = request.args.get('end')

    # If no dates provided, return error
    if not start or not end:
        return jsonify({'error': 'Missing date range'}), 400

    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    # Determine granularity
    delta = (end_date - start_date).days
    if delta == 0:
        group_by = "DATE(t.date)"
        label_format = "%Y-%m-%d"
    elif delta <= 30:
        group_by = "DATE(t.date)"
        label_format = "%Y-%m-%d"
    elif delta <= 90:
        group_by = "YEARWEEK(t.date)"
        label_format = "Week %u, %Y"
    else:
        group_by = "DATE_FORMAT(t.date, '%Y-%m')"
        label_format = "%Y-%m"

    query = f"""
        SELECT 
            {group_by} AS label,
            SUM(en.bulk_leads_reach) AS leads,
            SUM(en.incoming) AS incoming,
            SUM(en.interest) AS interest
        FROM entries en
        JOIN transactions t ON en.trans_id = t.t_id
        WHERE t.date BETWEEN %s AND %s
        GROUP BY label
        ORDER BY label;
    """

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (start, end))
    rows = cursor.fetchall()
    conn.close()

    labels = []
    leads = []
    incoming = []
    interest = []

    for row in rows:
        # For weekly/monthly data, keep as-is. For daily dates, format to dd-mm-yyyy
        raw_label = row['label']
        try:
            formatted = datetime.strptime(str(raw_label), "%Y-%m-%d").strftime("%d-%m-%Y")
        except:
            formatted = str(raw_label)  # For week or month formats
        labels.append(formatted)

        leads.append(row['leads'])
        incoming.append(row['incoming'])
        interest.append(row['interest'])

    return jsonify({
        'labels': labels,
        'leads': leads,
        'incoming': incoming,
        'interest': interest
    })




@chart_bp.route("/api/platform-analytics")
def platform_analytics():
    start = request.args.get('start')
    end = request.args.get('end')

    if not start or not end:
        return jsonify({'error': 'Missing date range'}), 400

    try:
        datetime.strptime(start, "%Y-%m-%d")
        datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    query = """
        SELECT pl.p_types AS platform,
               SUM(en.bulk_leads_reach) AS leads,
               SUM(en.incoming) AS incoming,
               SUM(en.interest) AS interest
        FROM entries en
        JOIN transactions t ON en.trans_id = t.t_id
        JOIN platform pl ON en.platform_id = pl.p_id
        WHERE t.date BETWEEN %s AND %s
        GROUP BY pl.p_types
        ORDER BY leads DESC;
    """

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (start, end))
    rows = cursor.fetchall()
    conn.close()

    labels = []
    leads = []
    incoming = []
    interest = []

    for row in rows:
        labels.append(row['platform'])
        leads.append(float(row['leads']) if row['leads'] is not None else 0.0)

        incoming.append(row['incoming'])
        interest.append(row['interest'])

    return jsonify({
        'labels': labels,
        'leads': leads,
        'incoming': incoming,
        'interest': interest
    })







@chart_bp.route("/api/employee-analytics")
def employee_analytics():
    start = request.args.get('start')
    end = request.args.get('end')

    if not start or not end:
        return jsonify({'error': 'Missing date range'}), 400

    try:
        datetime.strptime(start, "%Y-%m-%d")
        datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    query = """
        SELECT e.e_name AS employee,
               SUM(en.bulk_leads_reach) AS leads,
               SUM(en.incoming) AS incoming,
               SUM(en.interest) AS interest
        FROM entries en
        JOIN transactions t ON en.trans_id = t.t_id
        JOIN employee e ON t.emp_id = e.e_id
        WHERE t.date BETWEEN %s AND %s
        GROUP BY e.e_name
        ORDER BY leads DESC;
    """

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (start, end))
    rows = cursor.fetchall()
    conn.close()

    labels = []
    leads = []
    incoming = []
    interest = []

    for row in rows:
        labels.append(row['employee'])
        leads.append(row['leads'])
        incoming.append(row['incoming'])
        interest.append(row['interest'])

    return jsonify({
        'labels': labels,
        'leads': leads,
        'incoming': incoming,
        'interest': interest
    })




@chart_bp.route("/api/project-analytics")
def project_analytics():
    start = request.args.get('start')
    end = request.args.get('end')

    if not start or not end:
        return jsonify({'error': 'Missing date range'}), 400

    try:
        datetime.strptime(start, "%Y-%m-%d")
        datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    query = """
        SELECT p.pro_name AS project,
               SUM(en.bulk_leads_reach) AS leads,
               SUM(en.incoming) AS incoming,
               SUM(en.interest) AS interest
        FROM entries en
        JOIN transactions t ON en.trans_id = t.t_id
        JOIN project p ON t.project_id = p.pro_id
        WHERE t.date BETWEEN %s AND %s
        GROUP BY p.pro_name
        ORDER BY p.pro_name;
    """

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (start, end))
    rows = cursor.fetchall()
    conn.close()

    labels = []
    leads = []
    incoming = []
    interest = []

    for row in rows:
        labels.append(row['project'])
        leads.append(row['leads'])
        incoming.append(row['incoming'])
        interest.append(row['interest'])

    return jsonify({
        'labels': labels,
        'leads': leads,
        'incoming': incoming,
        'interest': interest
    })
