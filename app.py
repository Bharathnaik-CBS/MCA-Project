from flask import Flask
from routes.form_routes import form_bp
from routes.chart_routes import chart_bp
from routes.fetch_routes import fetch_bp

app = Flask(__name__)
app.secret_key='ozfn upnh vcvj dccb'

# Register blueprints only ONCE
app.register_blueprint(form_bp)
app.register_blueprint(chart_bp)
app.register_blueprint(fetch_bp)

if __name__ == "__main__":
    app.run(debug=True)



# app password - ozfn upnh vcvj dccb
# app password - wjbh mwuk iiqt fvkq    