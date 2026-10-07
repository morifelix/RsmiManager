from flask import Blueprint,render_template

bp_home =Blueprint("home",__name__)

@bp_home.route("/")
def home():
    return render_template("base.html")