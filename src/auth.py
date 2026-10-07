from flask import Blueprint,render_template

bp_auth =Blueprint("auth",__name__,template_folder="templates/auth")

@bp_auth.route("/login")
def login():
    return render_template("log-in.html")
