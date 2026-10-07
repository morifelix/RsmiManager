from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for
from .models import Items,Transactions
from .tra_funcs import *
from . import db
from sqlalchemy import select as SELECT


from datetime import date,datetime


today_now=date.today()

bp_transactions =Blueprint("transactions",__name__,template_folder="templates/transactions")

@bp_transactions.route("/",methods=["GET","POST"])
def transactions(this_month=today_now.strftime("%Y-%m")):
    if request.method == "POST":
        fecha=request.form.get("buwan")
        return render_template("tra.html",lamesa=month_setter(fecha),fecha=fecha)
    return render_template("tra.html",lamesa=month_setter(this_month),fecha=this_month)


@bp_transactions.route("/add-items",methods=["GET","POST"])
def newadd():
    ts_now=datetime.now()
    if request.method == "POST":
        item_id= request.form.getlist("ids[]")
        quant=request.form.getlist("quantity[]")
        fecha= request.form.get("date")
        fecha2=date.fromisoformat(fecha)
        logs=list(zip(item_id,quant))

        batch_no=batch_setter(fecha2)

        for log in logs:
            new_log=Transactions(item_id=log[0],items_used=log[1],date_log=fecha2,user_id=3,
                                                    timestamp=ts_now,batch_no=batch_no[0],serial_no=batch_no[1])
            db.session.add(new_log)
            db.session.commit()
        flash(f"{len(item_id)} items successfully added!!","good")
        return  redirect(url_for("transactions.transactions"))
    return render_template("tra_enroll.html")

#EDIT THIS LATER AND IMPROVE THE EDIT FEATURE
@bp_transactions.route("/edit/<int:id>")
def edit(id):
    query=(SELECT(Transactions).join(Items)).where(Transactions.id==id)
    lista=db.session.scalars(query).one()
    contents={"item_name":lista.items.item_name,"tra_id":lista.id,"item_id":lista.items.id,
    "quantity":lista.items_used,"fecha":lista.date_log,"ris_no":lista.batch_no,"serial_no":lista.serial_no}
    return render_template("tra_edit.html",**contents)


@bp_transactions.route("/generate")
def writer():
    print(ris_sorter(month_setter("2026-07")))
    return "<H1>YELLOE THERE XD!!!</H1>"



#API
@bp_transactions.route("/edit/api/items")
@bp_transactions.route("/api/items")
def search_items():
    query=request.args.get("q","").strip()

    if not query:
        return jsonify([])

    item_list=(
        db.session.execute(SELECT(Items).where(db.or_(Items.id.ilike(f"%{query}%"),Items.item_name.ilike(f"%{query}%"))).limit(10)).scalars().all()
    )
    return jsonify([
        {
            "id": item.id,
            "item_name":item.item_name
        }
        for item in item_list
    ])




