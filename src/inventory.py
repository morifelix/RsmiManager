from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import Items
from . import db
from sqlalchemy import select as SELECT

bp_inventory =Blueprint("inventory",__name__,template_folder="templates/inventory")

@bp_inventory.route("/")
def home():
    lista=Items.all_items()
    # lista=Items.query.order_by(Items.id).all()
    return render_template("inv.html",lamesa=lista,total_items=len(lista)) 


@bp_inventory.route("/enroll",methods=["GET","POST"])
def enroll(item_name="",item_id=""):
    status_errors={}
    flag=False
    if request.method == "POST":
        item_id=request.form.get("id")
        item_name=request.form.get("item_name")
        item_cost=request.form.get("unit_cost")
        item_type=request.form.get("unit_type")
        uacs_code=request.form.get("uacs_code")
        contents={"item_name":item_name,"id":item_id.upper(),"unit_cost":item_cost,"unit_type":item_type,"uacs_code":uacs_code}

        id_check=Items.query.filter_by(id=item_id.upper()).first()
        item_check=Items.query.filter_by(item_name=item_name).first()

        if id_check:
            status_errors.update({"error_id":f"❌Item ID already taken!!!! by {id_check.id} - {id_check.item_name}"})
            flag=True
        if item_check:
            status_errors.update({"error_name":f"❌Item ID already taken!!!! by {item_check.id} - {item_check.item_name}"})
            flag=True

        if flag:
            flash("We have encountered some errors","bad")
            return render_template("inv_enroll.html",**status_errors,**contents)
        new_item=Items(**contents)
        db.session.add(new_item)
        db.session.commit()
        flash(f'"{item_id}- {item_name}" has been successfully added!!',"good")
        return redirect(url_for("inventory.home"))
    return render_template("inv_enroll.html")


@bp_inventory.route("/edit/<id>",methods=["GET","POST"])
def edit(id):
    status_errors={}
    flag=False
    
    lista=db.session.get(Items,id)
    contents={"item_name":lista.item_name,"item_id":lista.id,"item_cost":lista.unit_cost,"item_type":lista.unit_type,"uacs_code":lista.uacs_code}
    if request.method == "POST":
        item_id=request.form.get("item_id")
        item_name=request.form.get("item_name")
        item_cost=request.form.get("item_cost")
        item_type=request.form.get("item_type")
        uacs_code=request.form.get("uacs_code")

        existing_id=db.session.scalar(SELECT(Items).where(Items.id==item_id.upper(),Items.id !=lista.id))
        existing_name=db.session.scalar(SELECT(Items).where(Items.item_name==item_name,Items.item_name !=lista.item_name))
        
        if existing_id:
            #[add feature in future] to specify which item id and name already exists in db
            status_errors.update({"error_id":f"❌Item ID already taken!!!! by {existing_id.id} - {existing_id.item_name}!!!"})
            flag=True
        if existing_name:
            status_errors.update({"error_name":f"❌Item Name already taken by {existing_name.id} - {existing_name.item_name}!!!!"})
            flag=True

        if flag:
            flash("We have encountered some error","bad")
            return render_template("inv_edit.html",**status_errors,**contents)
        lista.id=item_id
        lista.item_name=item_name
        lista.unit_cost=item_cost
        lista.unit_type=item_type
        lista.uacs_code=uacs_code
        db.session.commit()
        flash(f'Item "{item_id} - {item_name}" has been successfully updated!! ',"good")
        return redirect(url_for("inventory.home"))
    return render_template("inv_edit.html",**contents)


@bp_inventory.route("/delete/<id>",methods=["GET","POST"])
def delete(id):
    lista=db.session.get(Items,id)
    db.session.delete(lista)
    db.session.commit()
    flash(f"{lista.id}-{lista.item_name} has been deleted!!" )
    return redirect(url_for("inventory.home"))



