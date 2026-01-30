# routes/form_routes.py
from flask import Blueprint, request, render_template, jsonify, redirect, url_for, session, flash
from utils.db_helpers import get_db_connection
from flask import session
from datetime import datetime, timedelta
import random
import smtplib
import bcrypt



form_bp = Blueprint('form_bp', __name__)
@form_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admins WHERE username=%s", (username,))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()

        if admin and bcrypt.checkpw(password.encode('utf-8'), admin['admin_password'].encode('utf-8')):
            session['admin_id'] = admin['admin_id']
            return render_template("index.html")
        else:
            return render_template("login.html", error=True)

    return render_template("login.html", error=False)


@form_bp.route("/add-employee", methods=["GET", "POST"])
def add_employee():
    if request.method == "GET":
        return render_template("employee.html")

    elif request.method == "POST":
        e_id = request.form.get("e_id")
        e_name = request.form.get("e_name")
        p_no = request.form.get("p_no")
        email = request.form.get("email")

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO employee (e_id, e_name, p_no, email) VALUES (%s, %s, %s, %s)",
                           (e_id, e_name, p_no, email))
            conn.commit()
            cursor.close()
            conn.close()

            return jsonify({
                "success": True,
                "e_id": e_id,
                "e_name": e_name,
                "p_no": p_no,
                "email": email
            })

        except Exception as e:
            return jsonify({"success": False, "error": str(e)})


@form_bp.route("/add-project", methods=["POST"])
def add_project():
    form = request.form
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO project (pro_id, pro_name, area, status, total_plots, landmark, taluk, district, pincode)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            form.get('pro_id'), form.get('pro_name'), form.get('area'), form.get('status'),
            form.get('total_plots'), form.get('landmark'), form.get('taluk'),
            form.get('district'), form.get('pincode')
        ))
        conn.commit()
        return jsonify({"success": True, "pro_id": form.get('pro_id'), "pro_name": form.get('pro_name')})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        cursor.close()
        conn.close()


@form_bp.route("/add-plot", methods=["POST"])
def add_plot():
    form = request.form
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO plots (plot_no, pro_id, plot_size, plot_status)
            VALUES (%s, %s, %s, %s)
        """, (
            form.get('plot_no'), form.get('pro_id'),
            form.get('plot_size'), form.get('plot_status')
        ))
        conn.commit()
        return jsonify({"success": True, "plot_no": form.get('plot_no')})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        cursor.close()
        conn.close()


@form_bp.route("/add-customer", methods=["POST"])
def add_customer():
    form = request.form
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO customer (cust_name, phone_no, personal_id, cust_type)
            VALUES (%s, %s, %s, %s)
        """, (
            form.get('cust_name'), form.get('phone_no'),
            form.get('personal_id'), form.get('cust_type')
        ))
        conn.commit()
        return jsonify({"success": True, "cust_name": form.get('cust_name')})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        cursor.close()
        conn.close()


@form_bp.route("/add-transaction", methods=["POST"])
def add_transaction():
    form = request.form
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (t_id, date, emp_id, project_id) VALUES (%s, %s, %s, %s)",
            (form["t_id"], form["date"], form["emp_id"], form["project_id"])
        )
        conn.commit()
        return jsonify({"status": "success", "t_id": form["t_id"]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()


@form_bp.route("/add-entry", methods=["POST"])
def add_entry():
    form = request.form
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO entries (
                trans_id,
                platform_id,
                bulk_leads_reach,
                incoming,
                outgoing,
                interest,
                not_interest,
                not_pick_the_call,
                visit_set,
                site_visit,
                yesterday_visit_completed,
                unplanned_today_visit_completed,
                block,
                book, visit_cancel
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            form["trans_id"], form["platform_id"], form["bulk_leads_reach"], form["incoming"],
            form["outgoing"], form["interest"], form["not_interest"], form["not_pick_the_call"],
            form["visit_set"], form["site_visit"], form["yesterday_visit_completed"],
            form["unplanned_today_visit_completed"], form["block"], form["book"], form["visit_cancel"]
        ))
        conn.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message" : str(e)})
    finally:
        cursor.close()
        conn.close()


# --- In routes/form_routes.py ---



# --- Forgot Password Page ---
@form_bp.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')


# --- Helper: Send Email ---
def send_email(to_email, subject, body):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("bharathnaikpatil22@gmail.com", "wjbh mwuk iiqt fvkq")
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail('your_email@gmail.com', to_email, message)
        server.quit()
    except Exception as e:
        print("Failed to send email:", e)




# --- Send OTP ---
@form_bp.route('/send-otp', methods=['POST'])
def send_otp():
    email = request.form.get('email')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admins WHERE email=%s", (email,))
    admin = cursor.fetchone()

    if not admin:
        flash('Email not registered!', 'error')
        return redirect(url_for('form_bp.forgot_password'))

    otp = str(random.randint(100000, 999999))
    expiry = datetime.now() + timedelta(minutes=5)

    cursor.execute("UPDATE admins SET otp=%s, otp_expiry=%s WHERE email=%s", (otp, expiry, email))
    conn.commit()
    conn.close()

    # Send OTP via email
    send_email(email, "Your OTP Code", f"Your OTP is: {otp}")
    session['reset_email'] = email
    flash('OTP sent to your email.', 'info')
    return redirect(url_for('form_bp.verify_otp'))

# --- Verify OTP ---
@form_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        input_otp = request.form.get('otp')
        email = session.get('reset_email')
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT otp, otp_expiry FROM admins WHERE email=%s", (email,))
        data = cursor.fetchone()

        if data and data['otp'] == input_otp and datetime.now() <= data['otp_expiry']:
            return redirect(url_for('form_bp.reset_password'))
        else:
            flash('Invalid or expired OTP.', 'error')
            return redirect(url_for('form_bp.verify_otp'))

    return render_template('verify_otp.html')

# --- Reset Password ---
@form_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_pass = request.form.get('new_password')
        confirm = request.form.get('confirm_password')
        email = session.get('reset_email')

        if new_pass != confirm:
            flash("Passwords do not match.", 'error')
            return redirect(url_for('form_bp.reset_password'))

        hashed = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt())
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE admins SET admin_password=%s, otp=NULL, otp_expiry=NULL WHERE email=%s", (hashed, email))
        
# Fetch admin's name and email for notification
        cursor.execute("SELECT admin_name, email FROM admins WHERE email = %s", (email,))
        admin = cursor.fetchone()
        conn.commit()
        conn.close()


# Send notification email
        send_email(admin['email'],"Password Changed",f"Hi {admin['admin_name']}\n\nYour password was successfully changed using OTP. If this wasn't you, please contact support immediately.\n\nRegards: Admin Team")

        session.pop('reset_email', None)
        flash("Password reset successful. Please log in.", 'success')
        return redirect(url_for('form_bp.login'))

    return render_template('reset_password.html')


@form_bp.route("/change-password", methods=["GET", "POST"])
def change_password():
    if 'admin_id' not in session:
        return redirect(url_for('form_bp.login'))  # Not logged in

    if request.method == "POST":
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash("New passwords do not match.", "error")
            return render_template("change_password.html")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admins WHERE admin_id=%s", (session['admin_id'],))
        admin = cursor.fetchone()

        if admin and bcrypt.checkpw(current_password.encode(), admin['admin_password'].encode()):
            hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
            cursor.execute("UPDATE admins SET admin_password=%s WHERE admin_id=%s", (hashed_password, session['admin_id']))
            conn.commit()
            send_email(admin['email'], "Password Changed", f"Hi {admin['admin_name']}\n\nYour password was successfully changed. If this wasn't you, please contact support immediately.\n\nRegards: Admin Team")
            flash("Password changed successfully.", "success")
        else:
            flash("Incorrect current password.", "error")

        cursor.close()
        conn.close()
        return render_template("change_password.html")

    return render_template("change_password.html")


